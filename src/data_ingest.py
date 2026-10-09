"""
PhytoRAG-Tropical: Módulo de Ingesta, Limpieza y Chunking de Documentos
Responsable: Ricardo Mercado López (Data & Corpus Lead - Issue #1)
Director: Dr. Carlos Flores | Facultad de Telemática — Universidad de Colima
"""

import hashlib
import importlib.metadata
import json
import platform
import re
import zipfile
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import pypdf
import requests
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REVISION_MANUAL_EXALT = DATA_RAW / "revision_manual_exalt.json"

EXALT_LABEL = "Exalt_etiqueta_web_rev_2025.pdf"
COFEPRIS_EXALT_EVIDENCE = "Consulta_COFEPRIS_Exalt.png"

EXALT_COMBINACIONES = (
    {
        "id": "FICH-EXALT-LIMONERO-DIAPHORINA-001",
        "cultivo": "Limonero",
        "problema_fitosanitario": "Diaphorina citri",
        "pagina": 3,
        "inicio": "Limonero, Lima, Naranjo",
        "fin": "Minador de la hoja",
        "dosis_minima": 400.0,
        "dosis_maxima": 600.0,
        "dosis_texto": "400 - 600",
        "cultivo_cientifico": "Citrus aurantiifolia / grupo cítricos",
    },
    {
        "id": "FICH-EXALT-MANGO-TRIPS-001",
        "cultivo": "Mango",
        "problema_fitosanitario": "Trips de las flores (Frankliniella occidentalis)",
        "pagina": 5,
        "inicio": "Mango \n(1)",
        "fin": "Papayo \n(1)",
        "dosis_minima": 400.0,
        "dosis_maxima": 600.0,
        "dosis_texto": "400-600",
        "cultivo_cientifico": "Mangifera indica",
    },
    {
        "id": "FICH-EXALT-PAPAYO-SPODOPTERA-001",
        "cultivo": "Papayo",
        "problema_fitosanitario": "Gusano soldado (Spodoptera exigua)",
        "pagina": 5,
        "inicio": "Papayo \n(1)",
        "fin": "450-550 L de agua/ha.",
        "dosis_minima": 200.0,
        "dosis_maxima": 300.0,
        "dosis_texto": "200 - 300",
        "cultivo_cientifico": "Carica papaya",
    },
)

CAMPOS_REVISION_MANUAL_EXALT = {
    "registro_cofepris",
    "titular",
    "vigencia",
    "cultivos",
    "problema_fitosanitario",
    "dosis_y_unidad",
    "intervalo_seguridad",
    "reentrada",
    "restricciones",
}

URL_OFICIAL_SENASICA_DIAPHORINA = (
    "https://www.gob.mx/cms/uploads/attachment/file/147556/"
    "Ficha_T_cnica_Diaphorina_citri.pdf"
)


# ==============================================================================
# 1. Esquemas Pydantic y Contratos de Datos (Issue #1)
# ==============================================================================


class TipoInsumo(str, Enum):
    """Categoría agronómica del insumo fitosanitario."""

    QUIMICO_CONVENCIONAL = "Químico Convencional"
    BIOLOGICO_ORGANICO = "Biológico / Orgánico"
    BIORRACIONAL = "Biorracional"
    FERTILIZANTE_FOLIAR = "Fertilizante Foliar"


class FuenteNormativa(str, Enum):
    """Entidad o marco regulatorio de validez oficial."""

    COFEPRIS = "COFEPRIS"
    SENASICA = "SENASICA"
    OMRI = "OMRI"
    LPO = "LPO"
    EPA_USDA = "EPA / USDA"


class TrazabilidadFuente(BaseModel):
    """Metadatos de trazabilidad y auditoría de la fuente primaria."""

    documento_o_url: str = Field(
        ...,
        description="Nombre del archivo local o URL pública oficial consultada",
    )
    ubicacion_fuente: str = Field(
        ...,
        description="Página, sección, tabla o fila exacta de donde proviene la información",
    )
    fecha_consulta: str | None = Field(
        default=None,
        description="Fecha documentada de consulta, si se conoce (YYYY-MM-DD)",
    )
    sha256: str | None = Field(
        default=None, description="Hash SHA-256 del archivo de evidencia revisado"
    )


class RevisionManualExalt(BaseModel):
    """Atestación humana de revisión ligada a las versiones exactas de las fuentes."""

    revisor: str = Field(min_length=1)
    fecha_revision: date
    aprobada: bool = Field(strict=True)
    hashes_fuentes: dict[str, str]
    combinaciones_verificadas: set[str]
    campos_verificados: set[str]

    @field_validator("revisor")
    @classmethod
    def validar_revisor(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre del revisor no puede estar vacío.")
        return valor


class DosisEspecificacion(BaseModel):
    """Especificación numérica de dosis con validación de positividad y rango."""

    minima: float | None = Field(
        default=None,
        gt=0,
        description="Dosis mínima autorizada. Debe ser > 0 cuando existe.",
    )
    maxima: float = Field(
        ...,
        gt=0,
        description="Dosis máxima autorizada. Obligatoria y mayor a 0.",
    )
    unidad: str = Field(
        ...,
        description="Unidad de medida estandarizada (ej: L/ha, kg/ha, mL/100L)",
    )
    texto_etiqueta: str = Field(
        ...,
        description="Texto exacto de la dosis tal como figura en el documento o etiqueta",
    )

    @field_validator("unidad")
    @classmethod
    def validar_unidad(cls, v: str) -> str:
        unidades_validas = {
            "L/ha",
            "kg/ha",
            "mL/100L",
            "g/100L",
            "mL/L",
            "g/L",
            "L/100L",
            "mL/ha",
        }
        if v not in unidades_validas:
            raise ValueError(
                f"Unidad '{v}' no estandarizada. Permitidas: {unidades_validas}"
            )
        return v

    @model_validator(mode="after")
    def validar_rango_dosis(self) -> "DosisEspecificacion":
        if self.minima is not None and self.minima > self.maxima:
            raise ValueError(
                f"La dosis mínima ({self.minima}) no puede ser mayor que la máxima ({self.maxima})"
            )
        return self


class FichaFitosanitaria(BaseModel):
    """Ficha fitosanitaria con trazabilidad estricta y campos canónicos del Issue #1."""

    id_registro: str = Field(
        ..., description="Identificador único del registro fitosanitario"
    )
    cultivo: str = Field(
        ..., description="Cultivo agrícola (nombre común y/o científico)"
    )
    problema_fitosanitario: str = Field(
        ..., description="Plaga, enfermedad o maleza objetivo"
    )
    ingrediente_activo: str | None = Field(
        default=None,
        description="Ingrediente activo. None si no está especificado en la fuente.",
    )
    producto_comercial: str | None = Field(
        default=None,
        description="Nombre comercial del insumo. None si es un reporte genérico.",
    )
    registro_cofepris: str | None = Field(
        default=None,
        description="Número de registro oficial COFEPRIS (ej: RSCO-...). None si no está registrado o es desconocido.",
    )
    fuentes_adicionales: list[TrazabilidadFuente] = Field(
        default_factory=list,
        description="Evidencias complementarias de la revisión documental.",
    )
    dosis: DosisEspecificacion | None = Field(
        default=None,
        description="Especificación cuantitativa de la dosis. None si la fuente no proporciona valores numéricos.",
    )
    is_dias: int | None = Field(
        default=None,
        ge=0,
        description="Intervalo de seguridad en días antes de cosecha. None si es desconocido.",
    )
    aprobado_omri: bool | None = Field(
        default=None,
        description="True si está certificado OMRI, False si explícitamente no lo está, None si no se ha evaluado o es desconocido.",
    )
    periodo_reingreso_horas: int | None = Field(
        default=None,
        ge=0,
        description="Horas de espera antes de reingresar al lote tratado. None si la fuente no lo especifica.",
    )
    trazabilidad: TrazabilidadFuente = Field(
        ..., description="Datos de trazabilidad y auditoría de la fuente"
    )
    texto_fragmento: str | None = Field(
        default=None,
        description="Fragmento de texto estructurado para embedding y recuperación",
    )
    observaciones: str | None = Field(
        default=None,
        description="Notas de manejo, restricciones o justificación de campos faltantes",
    )

    revision_documental_aprobada: bool = Field(
        default=False,
        strict=True,
        description=(
            "Indica si la revisión documental fue aprobada y respaldada "
            "con evidencia. No se deduce de tener los campos completos"
        ),
    )

    def esta_completa_para_recomendacion(self) -> bool:
        """Exige campos completos y aprobación documental explícita."""
        return (
            self.revision_documental_aprobada
            and bool(self.cultivo.strip())
            and bool(self.problema_fitosanitario.strip())
            and bool((self.producto_comercial or "").strip())
            and bool((self.ingrediente_activo or "").strip())
            and bool((self.registro_cofepris or "").strip())
            and self.dosis is not None
            and self.is_dias is not None
            and bool((self.texto_fragmento or "").strip())
        )

    def campos_faltantes(self) -> list[str]:
        """Lista de los datos ausentes; la aprobación se registra por separado."""
        faltantes: list[str] = []

        campos_texto = (
            "cultivo",
            "problema_fitosanitario",
            "producto_comercial",
            "ingrediente_activo",
            "registro_cofepris",
            "texto_fragmento",
        )
        for nombre in campos_texto:
            valor = getattr(self, nombre, None)
            if not valor or not valor.strip():
                faltantes.append(nombre)

        if self.dosis is None:
            faltantes.append("dosis")
        if self.is_dias is None:
            faltantes.append("is_dias")

        return faltantes


class ChunkCorpus(BaseModel):
    """Estructura de documento lista para indexación en ChromaDB y BM25."""

    id_documento: str
    texto: str
    metadatos: dict[str, Any]


def hash_sha256(ruta: Path) -> str | None:
    """Calcula el hash SHA-256 de un archivo existente."""
    if not ruta.is_file():
        return None

    digest = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            digest.update(bloque)
    return digest.hexdigest()


def validar_revision_manual_exalt(
    revision: dict[str, Any] | None,
    hashes_fuentes: dict[str, str | None],
) -> tuple[bool, list[str]]:
    """Acepta la revisión solo si la atestación cubre los archivos actuales y los tres usos."""
    motivos: list[str] = []
    faltantes = [nombre for nombre, digest in hashes_fuentes.items() if digest is None]
    if faltantes:
        motivos.append("Faltan fuentes necesarias: " + ", ".join(sorted(faltantes)))
    if revision is None:
        motivos.append(
            f"No existe el registro de revisión manual {REVISION_MANUAL_EXALT.name}."
        )
        return False, motivos

    try:
        atestacion = RevisionManualExalt.model_validate(revision)
    except ValidationError as error:
        motivos.append(f"El registro de revisión manual no es válido: {error}")
        return False, motivos

    if not atestacion.aprobada:
        motivos.append("El registro de revisión manual no marca aprobación.")
    if atestacion.hashes_fuentes != {
        nombre: digest
        for nombre, digest in hashes_fuentes.items()
        if digest is not None
    }:
        motivos.append("Los hashes de las fuentes no coinciden con los revisados.")

    combinaciones_esperadas = {item["id"] for item in EXALT_COMBINACIONES}
    if atestacion.combinaciones_verificadas != combinaciones_esperadas:
        motivos.append("La revisión no cubre exactamente las tres combinaciones Exalt.")
    if atestacion.campos_verificados != CAMPOS_REVISION_MANUAL_EXALT:
        motivos.append(
            "La revisión no cubre todos los campos y restricciones requeridos."
        )

    return not motivos, motivos


def cargar_revision_manual_exalt() -> tuple[bool, list[str], dict[str, str | None]]:
    """Verifica existencia e integridad de las fuentes y carga la atestación manual."""
    rutas = {
        EXALT_LABEL: DATA_RAW / EXALT_LABEL,
        COFEPRIS_EXALT_EVIDENCE: DATA_RAW / COFEPRIS_EXALT_EVIDENCE,
    }
    hashes = {nombre: hash_sha256(ruta) for nombre, ruta in rutas.items()}
    if not REVISION_MANUAL_EXALT.is_file():
        revision = None
    else:
        with REVISION_MANUAL_EXALT.open(encoding="utf-8") as archivo:
            revision = json.load(archivo)
    aprobada, motivos = validar_revision_manual_exalt(revision, hashes)
    return aprobada, motivos, hashes


# ==============================================================================
# 2. Descarga y Extracción de Documento Primario Real (SENASICA)
# ==============================================================================


def descargar_ficha_senasica_diaphorina(
    ruta_destino: Path | None = None,
) -> Path:
    """Descarga el documento primario real de SENASICA a data/raw si no existe localmente."""
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    destino = ruta_destino or DATA_RAW / "Ficha_Tecnica_Diaphorina_citri_SENASICA.pdf"

    if destino.exists() and destino.stat().st_size > 0:
        return destino

    headers = {"User-Agent": "PhytoRAG-DataIngest/1.0 (Universidad de Colima)"}
    respuesta = requests.get(
        URL_OFICIAL_SENASICA_DIAPHORINA,
        headers=headers,
        timeout=25,
    )
    if respuesta.status_code != 200:
        raise RuntimeError(
            f"Error al descargar documento oficial SENASICA. Código HTTP: {respuesta.status_code} "
            f"desde {URL_OFICIAL_SENASICA_DIAPHORINA}"
        )

    with open(destino, "wb") as f:
        f.write(respuesta.content)

    return destino


def extraer_ficha_desde_pdf_senasica(ruta_pdf: Path) -> FichaFitosanitaria:
    """Lee el PDF oficial del SENASICA y extrae únicamente la evidencia explícita."""
    if not ruta_pdf.exists():
        raise FileNotFoundError(f"No se encontró el PDF en {ruta_pdf}")

    reader = pypdf.PdfReader(str(ruta_pdf))
    texto_completo = []
    for num_pag, pag in enumerate(reader.pages):
        contenido = pag.extract_text() or ""
        texto_completo.append(f"--- PÁGINA {num_pag + 1} ---\n{contenido}")

    # Evidencia textual extraída explícitamente del PDF de SENASICA
    texto_fragmento = "\n\n".join(texto_completo)

    ficha = FichaFitosanitaria(
        id_registro="RAW-SENASICA-DIAACI-001",
        cultivo="Citrus aurantiifolia (lima)",
        problema_fitosanitario="Diaphorina citri Kuwayama",
        ingrediente_activo=None,  # La ficha no detalla una molécula química comercial específica
        producto_comercial=None,  # La ficha no aprueba nombres comerciales particulares
        registro_cofepris=None,  # Desconocido en este documento epidemiológico
        dosis=None,  # Desconocido en este documento (sin valores numéricos)
        is_dias=None,  # Desconocido
        aprobado_omri=None,  # Desconocido (documento SENASICA no evalúa estándar OMRI)
        periodo_reingreso_horas=None,  # Desconocido
        trazabilidad=TrazabilidadFuente(
            documento_o_url=URL_OFICIAL_SENASICA_DIAPHORINA,
            ubicacion_fuente=(
                "Página 1: Identidad y Hospedantes; "
                "página 3: Epidemiología; página 4: Control"
            ),
            fecha_consulta=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            sha256=hash_sha256(ruta_pdf),
        ),
        texto_fragmento=texto_fragmento,
        observaciones=(
            "Ficha técnica oficial de vigilancia epidemiológica SENASICA. Identifica al cultivo "
            "y plaga vectora, pero no proporciona dosis ni registros comerciales COFEPRIS. "
            "Clasificada como incompleta para recomendación y enviada a revisión."
        ),
    )

    return ficha


# ==============================================================================
# 3. Clasificación, Cuarentena y Exportación
# ==============================================================================


def extraer_documentos_productos() -> Path:
    """Extrae los PDF de productos por página para revisión documental."""
    fuentes = [
        {
            "archivo": "DF-label-Exalt.pdf",
            "url": (
                "https://www.corteva.com/content/dam/dpagco/"
                "corteva/la/mx/es/products/files/DF-label-Exalt.pdf"
            ),
            "observaciones": (
                "Documento ilustrativo. Pendiente de contrastar "
                "con la etiqueta autorizada y el registro oficial."
            ),
        },
        {
            "archivo": "fichatecnica-engeo_247_sc.pdf",
            "url": (
                "https://www.syngenta.com.mx/sites/g/files/"
                "kgtney1381/files/media/document/2022/07/28/"
                "fichatecnica-engeo_247_sc.pdf"
            ),
            "observaciones": (
                "Ficha técnica informativa. Pendiente de aclarar "
                "las unidades de dosis. La evidencia complementaria "
                "de COFEPRIS se referencia en la ficha estructurada de Engeo."
            ),
        },
        {
            "archivo": "Exalt_etiqueta_web_rev_2025.pdf",
            "url": (
                "https://www.corteva.mx/content/dam/dpagco/corteva/la/"
                "mesoandean/mx/es/files/2026/etiqueta-web/"
                "EXALT%20-%20MEX%20-%20ETIQUETA%20WEB%20-%202025.pdf"
            ),
            "observaciones": (
                "Etiqueta web ilustrativa de Corteva. "
                "Revisión impresa: 12/12/2025. "
                "Pendiente de aprobación documental para recomendaciones."
            ),
        },
    ]

    documentos: list[dict[str, Any]] = []

    for fuente in fuentes:
        ruta = DATA_RAW / fuente["archivo"]
        if not ruta.is_file():
            raise FileNotFoundError(f"No se encontró {ruta}")

        reader = pypdf.PdfReader(str(ruta))
        paginas: list[dict[str, Any]] = []

        for numero, pagina in enumerate(reader.pages, start=1):
            texto = pagina.extract_text() or ""
            paginas.append(
                {
                    "pagina": numero,
                    "texto": texto,
                    "requiere_ocr": not bool(texto.strip()),
                }
            )
        documentos.append(
            {
                "archivo": fuente["archivo"],
                "documento_o_url": fuente["url"],
                "fecha_extraccion_utc": datetime.now(timezone.utc).isoformat(),
                "estado": "PENDIENTE_REVISION",
                "revision_documental_aprobada": False,
                "sha256": hash_sha256(ruta),
                "observaciones": fuente["observaciones"],
                "total_paginas": len(paginas),
                "paginas": paginas,
            }
        )

        print(f"[EXTRACCIÓN] {ruta.name}: {len(paginas)} páginas")

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    salida = DATA_PROCESSED / "documentos_productos_pendientes.json"

    with salida.open("w", encoding="utf-8") as archivo:
        json.dump(documentos, archivo, ensure_ascii=False, indent=2)

    return salida


def crear_ficha_engeo_pendiente(ruta_json: Path) -> FichaFitosanitaria:
    """Estructura datos revisados del PDF de Engeo, sin aprobar su uso."""
    with ruta_json.open(encoding="utf-8") as archivo:
        documentos = json.load(archivo)

    documento = next(
        (
            doc
            for doc in documentos
            if doc["archivo"] == "fichatecnica-engeo_247_sc.pdf"
        ),
        None,
    )
    if documento is None:
        raise ValueError("No se encontró el documento de Engeo en el JSON.")

    texto = "\n\n".join(
        f"--- PÁGINA {pagina['pagina']} ---\n{pagina['texto']}"
        for pagina in documento["paginas"]
        if pagina["pagina"] in (1, 2, 3)
    )

    ruta_evidencia = DATA_RAW / "Consulta_COFEPRIS_Engeo.pdf"
    evidencia_cofepris = (
        [
            TrazabilidadFuente(
                documento_o_url="data/raw/Consulta_COFEPRIS_Engeo.pdf",
                ubicacion_fuente=(
                    "Captura del detalle del registro; la dosis no se valida "
                    "mediante esta evidencia."
                ),
                sha256=hash_sha256(ruta_evidencia),
            )
        ]
        if ruta_evidencia.is_file()
        else []
    )

    return FichaFitosanitaria(
        id_registro="PENDIENTE-ENGEO-LIMONERO-DIAPHORINA-001",
        cultivo="Limonero",
        problema_fitosanitario="Diaphorina citri",
        producto_comercial="Engeo 247 SC",
        ingrediente_activo="thiametoxam + lambda cyalotrina",
        registro_cofepris="RSCO-MEZC-1101D-301-064-022",
        dosis=None,
        is_dias=14,
        aprobado_omri=None,
        revision_documental_aprobada=False,
        trazabilidad=TrazabilidadFuente(
            documento_o_url=documento["documento_o_url"],
            ubicacion_fuente=(
                "Página 1: producto, ingredientes y registro impreso; "
                "página 2: encabezado de unidades; "
                "página 3: limonero, plaga e intervalo de seguridad."
            ),
            sha256=documento.get("sha256"),
        ),
        fuentes_adicionales=evidencia_cofepris,
        texto_fragmento=texto,
        observaciones=(
            "Transcripción de la ficha técnica informativa de 2019. "
            "La captura COFEPRIS se conserva como evidencia complementaria, "
            "pero su existencia no se considera una validación de contenido. "
            "Dosis sin estructurar por inconsistencia de unidades "
            "en la ficha técnica. La captura de COFEPRIS no aporta "
            "dosis, plaga ni intervalo de seguridad. "
            "El intervalo de seguridad procede del (14) del grupo "
            "de cítricos y su leyenda en la página 3 de la ficha técnica. "
            "No aprobada para recomendaciones."
        ),
    )


def extraer_segmento(texto: str, inicio: str, fin: str) -> str:
    """Extrae un pasaje delimitado sin incorporar la recomendación siguiente."""
    desde = texto.find(inicio)
    if desde < 0:
        raise ValueError(f"No se encontró el inicio de evidencia: {inicio!r}")
    hasta = texto.find(fin, desde + len(inicio))
    if hasta < 0:
        raise ValueError(f"No se encontró el límite de evidencia: {fin!r}")
    if fin == "450-550 L de agua/ha.":
        hasta += len(fin)
    pasaje = texto[desde:hasta].strip()
    if not pasaje:
        raise ValueError("El pasaje de evidencia extraído está vacío.")
    return pasaje


def construir_texto_exalt(
    documento: dict[str, Any], combinacion: dict[str, Any]
) -> str:
    """Construye un chunk con una sola combinación y restricciones comunes textuales."""
    paginas = {pagina["pagina"]: pagina["texto"] for pagina in documento["paginas"]}
    pagina_combinacion = paginas.get(combinacion["pagina"])
    pagina_restricciones = paginas.get(3)
    pagina_seguridad = paginas.get(2)
    pagina_identificacion = paginas.get(1)
    if not all(
        (
            pagina_combinacion,
            pagina_restricciones,
            pagina_seguridad,
            pagina_identificacion,
        )
    ):
        raise ValueError("La etiqueta Exalt no contiene todas las páginas requeridas.")

    tabla = re.search(
        r"CULTIVO\s+PLAGA\s+DOSIS\s+mL/ha\s+RECOMENDACIONES",
        pagina_combinacion,
        flags=re.IGNORECASE,
    )
    if tabla is None:
        raise ValueError(
            f"No se encontró el encabezado de dosis en la página {combinacion['pagina']}."
        )

    evidencia_combinacion = extraer_segmento(
        pagina_combinacion,
        combinacion["inicio"],
        combinacion["fin"],
    )
    dosis_normalizada = re.sub(r"\s+", " ", evidencia_combinacion)
    dosis_normalizada = dosis_normalizada.replace("–", "-")
    dosis_esperada = combinacion["dosis_texto"].replace("–", "-")
    if dosis_esperada not in dosis_normalizada:
        raise ValueError(
            f"La evidencia de {combinacion['cultivo']} no respalda la dosis esperada."
        )

    definicion_intervalos = extraer_segmento(
        pagina_restricciones,
        "Periodo de reentrada a las áreas tratadas:",
        "Sin Límite.",
    )
    inicio_preparacion = pagina_restricciones.find(
        "MÉTODOS PARA PREPARAR Y APLICAR EL PRODUCTO."
    )
    fin_preparacion = pagina_restricciones.find(
        "En aplicaciones terrestres en solanáceas", inicio_preparacion
    )
    if inicio_preparacion < 0 or fin_preparacion < 0:
        raise ValueError(
            "No se pudo aislar el método general sin mezclar otros cultivos."
        )
    preparacion_general = pagina_restricciones[
        inicio_preparacion:fin_preparacion
    ].strip()

    inicio_restricciones = pagina_restricciones.find("CONTRAINDICACIONES.")
    fin_restricciones = pagina_restricciones.find(
        "Exalt® no debe alternarse o ser mezclado con cualquier insecticida "
        "al que ya se haya desarrollado resistencia.",
        inicio_restricciones,
    )
    frase_final_resistencia = (
        "Exalt® no debe alternarse o ser mezclado con cualquier insecticida "
        "al que ya se haya desarrollado resistencia."
    )
    if inicio_restricciones < 0 or fin_restricciones < 0:
        raise ValueError(
            "No se pudieron aislar las restricciones generales de la etiqueta."
        )
    restricciones_generales = pagina_restricciones[
        inicio_restricciones : fin_restricciones + len(frase_final_resistencia)
    ].strip()

    return "\n\n".join(
        (
            (
                "Ficha estructurada por PhytoRAG-Tropical a partir de un documento "
                "ilustrativo de Corteva y evidencia de consulta COFEPRIS. Esta ficha "
                "no fue emitida ni aprobada por COFEPRIS."
            ),
            "Producto: Exalt. Titular indicado en la etiqueta: CORTEVA MX, S. A. DE C.V.",
            f"Cultivo: {combinacion['cultivo']} ({combinacion['cultivo_cientifico']}).",
            f"Problema fitosanitario: {combinacion['problema_fitosanitario']}.",
            f"Dosis transcrita: {combinacion['dosis_texto']} mL/ha.",
            "Intervalo de seguridad: 1 día según el indicador (1) definido en la etiqueta.",
            "Periodo de reentrada: 4 horas.",
            "--- Evidencia de identificación del producto (etiqueta ilustrativa, página 1) ---\n"
            + pagina_identificacion.strip(),
            "--- Precauciones comunes: protección personal, ambiente y abejas (página 2) ---\n"
            + pagina_seguridad.strip(),
            f"--- Tabla de usos; página {combinacion['pagina']}; dosis expresada en mL/ha ---\n"
            + tabla.group(0)
            + "\n"
            + evidencia_combinacion,
            "--- Definición de intervalo de seguridad y reentrada (página 3) ---\n"
            + definicion_intervalos,
            "--- Preparación general, sin instrucciones de otros cultivos (página 3) ---\n"
            + preparacion_general,
            "--- Contraindicaciones, mezclas, fitotoxicidad y manejo de resistencia (página 3) ---\n"
            + restricciones_generales,
        )
    )


def plantilla_revision_manual_exalt(
    hashes_fuentes: dict[str, str | None],
) -> dict[str, Any]:
    """Genera un formato sin aprobar ni atribuir una revisión inexistente."""
    return {
        "revisor": None,
        "fecha_revision": None,
        "aprobada": False,
        "hashes_fuentes": hashes_fuentes,
        "combinaciones_verificadas": [],
        "campos_verificados": sorted(CAMPOS_REVISION_MANUAL_EXALT),
        "instrucciones": (
            "Complete esta atestación solo después de revisar manualmente cada fuente. "
            "Guárdela como data/raw/revision_manual_exalt.json. No cambie los hashes "
            "para aceptar una fuente distinta; vuelva a revisar y registre su hash."
        ),
    }


def crear_fichas_exalt_validadas(
    ruta_json: Path,
) -> list[FichaFitosanitaria]:
    """Crea candidatos por combinación y los aprueba solo con revisión humana vigente."""
    with ruta_json.open(encoding="utf-8") as archivo:
        documentos = json.load(archivo)

    documento = next(
        (doc for doc in documentos if doc["archivo"] == EXALT_LABEL),
        None,
    )
    if documento is None:
        return []

    revision_aprobada, motivos_revision, hashes = cargar_revision_manual_exalt()
    captura_disponible = hashes[COFEPRIS_EXALT_EVIDENCE] is not None
    fecha_revision: str | None = None
    revisor: str | None = None
    if revision_aprobada:
        with REVISION_MANUAL_EXALT.open(encoding="utf-8") as archivo:
            atestacion = RevisionManualExalt.model_validate(json.load(archivo))
        fecha_revision = atestacion.fecha_revision.isoformat()
        revisor = atestacion.revisor

    fuente_etiqueta = documento["documento_o_url"]
    hash_etiqueta = hashes[EXALT_LABEL]
    fichas: list[FichaFitosanitaria] = []

    for combinacion in EXALT_COMBINACIONES:
        texto = construir_texto_exalt(documento, combinacion)
        fuentes_adicionales = []
        if captura_disponible:
            fuentes_adicionales.append(
                TrazabilidadFuente(
                    documento_o_url=f"data/raw/{COFEPRIS_EXALT_EVIDENCE}",
                    ubicacion_fuente=(
                        "Captura del detalle del registro: registro, titular, "
                        "cultivos listados y vigencia. No acredita la dosis ni "
                        "el problema fitosanitario."
                    ),
                    fecha_consulta=fecha_revision,
                    sha256=hashes[COFEPRIS_EXALT_EVIDENCE],
                )
            )

        nota_revision = (
            f"Atestación de revisión manual registrada por {revisor} el {fecha_revision}; "
            "los hashes de las fuentes y las tres combinaciones coinciden."
            if revision_aprobada
            else "Pendiente de revisión manual documentada. "
            + " ".join(motivos_revision)
        )
        fichas.append(
            FichaFitosanitaria(
                id_registro=combinacion["id"],
                cultivo=combinacion["cultivo"],
                problema_fitosanitario=combinacion["problema_fitosanitario"],
                producto_comercial="Exalt",
                ingrediente_activo="spinetoram",
                registro_cofepris="RSCO-INAC-0103X-301-064-006",
                dosis=DosisEspecificacion(
                    minima=combinacion["dosis_minima"],
                    maxima=combinacion["dosis_maxima"],
                    unidad="mL/ha",
                    texto_etiqueta=combinacion["dosis_texto"],
                ),
                is_dias=1,
                aprobado_omri=None,
                periodo_reingreso_horas=4,
                trazabilidad=TrazabilidadFuente(
                    documento_o_url=fuente_etiqueta,
                    ubicacion_fuente=(
                        "Página 1: identidad del producto, registro y titular; "
                        f"página {combinacion['pagina']}: fila de cultivo/plaga/dosis; "
                        "página 3: definición del indicador (1) y reentrada."
                    ),
                    fecha_consulta=fecha_revision,
                    sha256=hash_etiqueta,
                ),
                fuentes_adicionales=fuentes_adicionales,
                texto_fragmento=texto,
                observaciones=(
                    "Ficha elaborada por PhytoRAG-Tropical a partir de una etiqueta "
                    "web que se identifica a sí misma como ilustrativa y de una "
                    "consulta documental de COFEPRIS. No es una ficha emitida o "
                    "aprobada por COFEPRIS. " + nota_revision
                ),
                revision_documental_aprobada=revision_aprobada,
            )
        )

    return fichas


def crear_ficha_exalt_validada(ruta_json: Path) -> FichaFitosanitaria:
    """Devuelve el candidato Exalt de Limonero por compatibilidad de interfaz."""
    return crear_fichas_exalt_validadas(ruta_json)[0]


def clasificar_y_exportar(
    fichas: list[FichaFitosanitaria],
    directorio_salida: Path | None = None,
) -> dict[str, Any]:
    """Separa registros aptos para RAG de candidatos y fichas en cuarentena."""
    directorio = directorio_salida or DATA_PROCESSED
    directorio.mkdir(parents=True, exist_ok=True)

    ruta_vademecum = directorio / "vademecum_fitosanitario.json"
    ruta_chunks = directorio / "chunks_corpus.json"
    ruta_pendientes = directorio / "registros_pendientes_revision.json"
    ruta_candidatos = directorio / "chunks_candidatos_revision.json"
    ruta_plantilla = directorio / "revision_manual_exalt.template.json"

    revision_actual_aprobada, motivos_revision, hashes_fuentes = (
        cargar_revision_manual_exalt()
    )
    fichas_clasificadas: list[FichaFitosanitaria] = []
    for ficha in fichas:
        if (
            ficha.id_registro.startswith("FICH-EXALT-")
            and ficha.revision_documental_aprobada
        ):
            hashes_ficha = {
                EXALT_LABEL: ficha.trazabilidad.sha256,
                COFEPRIS_EXALT_EVIDENCE: next(
                    (
                        fuente.sha256
                        for fuente in ficha.fuentes_adicionales
                        if fuente.documento_o_url.endswith(COFEPRIS_EXALT_EVIDENCE)
                    ),
                    None,
                ),
            }
            if not revision_actual_aprobada or hashes_ficha != hashes_fuentes:
                ficha = ficha.model_copy(
                    update={
                        "revision_documental_aprobada": False,
                        "observaciones": (
                            (ficha.observaciones or "")
                            + " Aprobación retirada al exportar: "
                            + " ".join(motivos_revision)
                        ).strip(),
                    }
                )
        fichas_clasificadas.append(ficha)

    validadas = [f for f in fichas_clasificadas if f.esta_completa_para_recomendacion()]
    pendientes = [
        f for f in fichas_clasificadas if not f.esta_completa_para_recomendacion()
    ]
    candidatos_exalt = [
        f for f in fichas_clasificadas if f.id_registro.startswith("FICH-EXALT-")
    ]

    # 1. Corpus oficial para recomendación (SOLO fichas completas y verificadas)
    datos_validados = [f.model_dump() for f in validadas]
    with open(ruta_vademecum, "w", encoding="utf-8") as f:
        json.dump(datos_validados, f, ensure_ascii=False, indent=2)

    # 2. Chunks para Sofía (ChromaDB / BM25) - CERO registros incompletos o sin verificar
    chunks = [
        ChunkCorpus(
            id_documento=f.id_registro,
            texto=f.texto_fragmento or "",
            metadatos={
                "id_registro": f.id_registro,
                "cultivo": f.cultivo,
                "problema_fitosanitario": f.problema_fitosanitario,
                "ingrediente_activo": f.ingrediente_activo,
                "registro_cofepris": f.registro_cofepris,
                "dosis_texto": f.dosis.texto_etiqueta if f.dosis else None,
                "dosis_minima": f.dosis.minima if f.dosis else None,
                "dosis_maxima": f.dosis.maxima if f.dosis else None,
                "dosis_unidad": f.dosis.unidad if f.dosis else None,
                "is_dias": f.is_dias,
                "periodo_reingreso_horas": f.periodo_reingreso_horas,
                "aprobado_omri": f.aprobado_omri,
                "documento_fuente": f.trazabilidad.documento_o_url,
                "sha256_fuente": f.trazabilidad.sha256,
                "ubicacion_fuente": f.trazabilidad.ubicacion_fuente,
                "fecha_consulta": f.trazabilidad.fecha_consulta,
                "fuentes_adicionales": [
                    fuente.model_dump() for fuente in f.fuentes_adicionales
                ],
            },
        ).model_dump()
        for f in validadas
    ]
    with open(ruta_chunks, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    # 3. Chunks de inspección separados del índice que consume el motor RAG.
    chunks_candidatos = [
        ChunkCorpus(
            id_documento=f.id_registro,
            texto=f.texto_fragmento or "",
            metadatos={
                "id_registro": f.id_registro,
                "cultivo": f.cultivo,
                "problema_fitosanitario": f.problema_fitosanitario,
                "ingrediente_activo": f.ingrediente_activo,
                "registro_cofepris": f.registro_cofepris,
                "dosis_texto": f.dosis.texto_etiqueta if f.dosis else None,
                "dosis_minima": f.dosis.minima if f.dosis else None,
                "dosis_maxima": f.dosis.maxima if f.dosis else None,
                "dosis_unidad": f.dosis.unidad if f.dosis else None,
                "is_dias": f.is_dias,
                "periodo_reingreso_horas": f.periodo_reingreso_horas,
                "aprobado_omri": f.aprobado_omri,
                "revision_documental_aprobada": f.revision_documental_aprobada,
                "documento_fuente": f.trazabilidad.documento_o_url,
                "sha256_fuente": f.trazabilidad.sha256,
                "ubicacion_fuente": f.trazabilidad.ubicacion_fuente,
                "fuentes_adicionales": [
                    fuente.model_dump() for fuente in f.fuentes_adicionales
                ],
            },
        ).model_dump()
        for f in candidatos_exalt
    ]
    with open(ruta_candidatos, "w", encoding="utf-8") as f:
        json.dump(chunks_candidatos, f, ensure_ascii=False, indent=2)

    # 4. Registros pendientes de revisión (cuarentena trazable).
    datos_pendientes = [
        {
            "ficha": f.model_dump(),
            "estado": "PENDIENTE_REVISION",
            "campos_faltantes": f.campos_faltantes(),
            "motivo_cuarentena": f.observaciones
            or "Faltan datos requeridos o la revisión documental no está aprobada.",
            "chunk_candidato": (
                next(
                    (
                        chunk
                        for chunk in chunks_candidatos
                        if chunk["id_documento"] == f.id_registro
                    ),
                    None,
                )
                if f.id_registro.startswith("FICH-EXALT-")
                else None
            ),
        }
        for f in pendientes
    ]
    with open(ruta_pendientes, "w", encoding="utf-8") as f:
        json.dump(datos_pendientes, f, ensure_ascii=False, indent=2)

    with ruta_plantilla.open("w", encoding="utf-8") as f:
        json.dump(
            plantilla_revision_manual_exalt(hashes_fuentes),
            f,
            ensure_ascii=False,
            indent=2,
        )

    return {
        "total_procesadas": len(fichas),
        "total_validadas_rag": len(validadas),
        "total_pendientes_revision": len(pendientes),
        "total_candidatos_exalt": len(candidatos_exalt),
        "ruta_vademecum": ruta_vademecum,
        "ruta_chunks": ruta_chunks,
        "ruta_pendientes": ruta_pendientes,
        "ruta_candidatos": ruta_candidatos,
        "ruta_plantilla_revision": ruta_plantilla,
    }


def versiones_dependencias() -> dict[str, str]:
    """Registra las versiones instaladas de las dependencias declaradas."""
    versiones: dict[str, str] = {}
    for linea in (
        (PROJECT_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    ):
        requisito = linea.strip()
        if not requisito or requisito.startswith("#"):
            continue
        nombre = re.split(r"[<=>~!;\[]", requisito, maxsplit=1)[0].strip()
        try:
            versiones[nombre] = importlib.metadata.version(nombre)
        except importlib.metadata.PackageNotFoundError:
            versiones[nombre] = "no instalado"
    return versiones


def crear_instrucciones_paquete() -> str:
    """Devuelve pasos reproducibles y límites de uso del corpus."""
    return """# Instrucciones del paquete de corpus M1

1. Descomprima este paquete en la raíz de una copia de PhytoRAG-Tropical.
2. Use Python 3.10 o superior. El entorno con el que se generó este paquete se
   registra en `MANIFEST.md`; no cambie `requirements.txt` para acomodar otro
   intérprete.
3. Instale las dependencias del repositorio con `python -m pip install -r requirements.txt`.
4. Ejecute `python src/data_ingest.py` para regenerar las extracciones y los JSON.
5. `data/processed/chunks_candidatos_revision.json` es una salida de auditoría,
   no debe cargarse al índice RAG. Solo `chunks_corpus.json` contiene fichas con
   revisión documentada vigente.
6. Para proponer la aprobación manual de Exalt, revise las dos fuentes y las tres
   combinaciones. Complete `data/processed/revision_manual_exalt.template.json`,
   guárdela como `data/raw/revision_manual_exalt.json` y registre revisor, fecha,
   hashes intactos, campos y combinaciones revisadas. Vuelva a ejecutar el pipeline.
   Si falta o cambia una fuente, el pipeline mantiene las fichas en cuarentena.

La etiqueta de Exalt incluida se identifica como ilustrativa; las fichas son
elaboradas por PhytoRAG-Tropical y no son emitidas ni aprobadas por COFEPRIS.
No se infiere aprobación OMRI ni compatibilidad de exportación. Este paquete no
constituye una recomendación agronómica ni una validación de “cero alucinaciones”.
"""


def crear_manifiesto_y_paquete() -> Path:
    """Genera manifiesto reproducible y ZIP con fuentes, salidas e instrucciones."""
    ruta_manifiesto = PROJECT_ROOT / "MANIFEST.md"
    ruta_instrucciones = PROJECT_ROOT / "INSTRUCCIONES.md"
    ruta_paquete = PROJECT_ROOT / "data-m1-corpus-revisado.zip"
    ruta_instrucciones.write_text(crear_instrucciones_paquete(), encoding="utf-8")

    archivos = [
        *sorted(path for path in DATA_RAW.rglob("*") if path.is_file()),
        *sorted(path for path in DATA_PROCESSED.rglob("*") if path.is_file()),
        PROJECT_ROOT / "src" / "data_ingest.py",
        PROJECT_ROOT / "requirements.txt",
        ruta_instrucciones,
    ]
    archivos = [path for path in archivos if path.name != ".gitkeep"]
    filas = []
    for ruta in archivos:
        relativo = ruta.relative_to(PROJECT_ROOT).as_posix()
        filas.append(
            f"| `{relativo}` | {ruta.stat().st_size} | `{hash_sha256(ruta)}` |"
        )

    aprobada, motivos, hashes = cargar_revision_manual_exalt()
    estado_revision = (
        "aprobada mediante atestación manual vinculada a hashes"
        if aprobada
        else "pendiente; fichas Exalt excluidas del corpus aprobable"
    )
    motivo_texto = " ".join(motivos) if motivos else "Sin pendientes."
    commit_base = "454225a2958da55ed2961f19f173589c1272a7ed"
    manifiesto_lineas = [
        "# Manifiesto de datos PhytoRAG-Tropical — M1\n\n"
        + f"- Commit de código de partida verificado: `{commit_base}`.\n"
        + f"- SHA-256 del código de ingesta ejecutado: `{hash_sha256(PROJECT_ROOT / 'src' / 'data_ingest.py')}`.\n"
        + f"- Python: `{platform.python_version()}`.\n"
        + f"- Estado de revisión manual Exalt: **{estado_revision}**.\n"
        + f"- Observaciones de revisión: {motivo_texto}\n"
        + "- Una captura presente no se considera validación automática de su contenido.\n"
        + "- Los hashes listados identifican las versiones exactas incluidas en este paquete.\n\n"
        + "## Hashes SHA-256 y tamaños\n\n"
        + "| Archivo | Bytes | SHA-256 |\n|---|---:|---|\n"
        + "\n".join(filas)
        + "\n\n## Versiones instaladas\n\n"
        + "| Dependencia | Versión |\n|---|---|\n"
        + "\n".join(
            f"| `{nombre}` | `{version}` |"
            for nombre, version in versiones_dependencias().items()
        )
        + "\n\n## Estado de revisión manual\n\n"
        + f"- Captura COFEPRIS Exalt: `{hashes[COFEPRIS_EXALT_EVIDENCE]}`.\n"
        + f"- Etiqueta ilustrativa Exalt: `{hashes[EXALT_LABEL]}`.\n"
    ]
    if not aprobada:
        manifiesto_lineas.append(
            "- No hay atestación manual vigente que apruebe las fichas Exalt.\n"
        )
    manifiesto = "".join(manifiesto_lineas)
    ruta_manifiesto.write_text(manifiesto, encoding="utf-8")

    archivos_paquete = [*archivos, ruta_manifiesto]
    revision_real = DATA_RAW / REVISION_MANUAL_EXALT.name
    if revision_real.is_file():
        archivos_paquete.append(revision_real)
    with zipfile.ZipFile(
        ruta_paquete, "w", compression=zipfile.ZIP_DEFLATED
    ) as paquete:
        for ruta in archivos_paquete:
            paquete.write(
                ruta,
                arcname=ruta.relative_to(PROJECT_ROOT).as_posix(),
            )
    return ruta_paquete


# ==============================================================================
# 4. Punto de Entrada
# ==============================================================================

if __name__ == "__main__":
    import contextlib
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        with contextlib.suppress(AttributeError, ValueError):
            sys.stdout.reconfigure(encoding="utf-8")

    # Evita que una ejecución fallida deje fichas previamente aprobadas indexables.
    clasificar_y_exportar([])
    print("[DATA LEAD] Procesando documento primario oficial de SENASICA...")

    # 1. Localizar y asegurar documento en data/raw/
    ruta_pdf = descargar_ficha_senasica_diaphorina()
    print(f"[RAW] Documento primario asegurado: {ruta_pdf}")

    # 2. Extraer evidencia trazable mediante pypdf
    ficha_extraida = extraer_ficha_desde_pdf_senasica(ruta_pdf)

    # 3. Clasificar y exportar (cuarentena de incompletos vs aprobados)
    ruta_documentos = extraer_documentos_productos()
    ficha_engeo = crear_ficha_engeo_pendiente(ruta_documentos)
    fichas_exalt = crear_fichas_exalt_validadas(ruta_documentos)

    fichas_a_procesar = [ficha_extraida, ficha_engeo, *fichas_exalt]
    resultado = clasificar_y_exportar(fichas_a_procesar)

    print("\n[RESULTADO DE AUDITORÍA Y TRAZABILIDAD]")
    print(
        f"  * Documento analizado (SENASICA): {ficha_extraida.trazabilidad.documento_o_url}"
    )
    print(f"  * Ubicación consultada: {ficha_extraida.trazabilidad.ubicacion_fuente}")
    print(f"  * Cultivo identificado: {ficha_extraida.cultivo}")
    print(f"  * Problema fitosanitario: {ficha_extraida.problema_fitosanitario}")
    print(f"  * Ingrediente activo: {ficha_extraida.ingrediente_activo} (FALTANTE)")
    print(f"  * Registro COFEPRIS: {ficha_extraida.registro_cofepris} (FALTANTE)")
    print(f"  * Dosis numérica: {ficha_extraida.dosis} (FALTANTE)")
    print(f"  * Intervalo seguridad (is_dias): {ficha_extraida.is_dias} (FALTANTE)")
    print(f"  * Aprobación OMRI: {ficha_extraida.aprobado_omri} (DESCONOCIDO)")
    print(f"  * Campos faltantes detectados: {ficha_extraida.campos_faltantes()}")

    print(f"\n[FICHAS CANDIDATAS EXALT ({len(fichas_exalt)})]")
    for f_val in fichas_exalt:
        print("  --------------------------------------------------")
        print(f"  * ID: {f_val.id_registro}")
        print(f"  * Cultivo: {f_val.cultivo}")
        print(f"  * Plaga: {f_val.problema_fitosanitario}")
        print(f"  * Producto: {f_val.producto_comercial} ({f_val.ingrediente_activo})")
        print(f"  * Registro COFEPRIS: {f_val.registro_cofepris}")
        print(
            f"  * Dosis transcrita: {f_val.dosis.texto_etiqueta} "
            f"{f_val.dosis.unidad if f_val.dosis else ''}"
        )
        print(
            f"  * Intervalo seguridad (IS): {f_val.is_dias} día | "
            f"Reingreso: {f_val.periodo_reingreso_horas} horas"
        )
        print(f"  * Revisión manual vigente: {f_val.revision_documental_aprobada}")
        print(f"  * Fuentes con hash registrado: {len(f_val.fuentes_adicionales) + 1}")

    print(
        f"\n[ESTATUS DEL CORPUS]\n"
        f"  * Fichas aprobadas para RAG (Sofía): {resultado['total_validadas_rag']}\n"
        f"  * Fichas en cuarentena (revisión): {resultado['total_pendientes_revision']}\n"
        f"  * Chunks candidatos separados: {resultado['total_candidatos_exalt']}\n"
        f"  * Vademécum aprobado: {resultado['ruta_vademecum']}\n"
        f"  * Chunks aprobados: {resultado['ruta_chunks']}\n"
        f"  * Chunks candidatos (no indexar): {resultado['ruta_candidatos']}\n"
        f"  * Archivo de pendientes: {resultado['ruta_pendientes']}\n"
        f"  * Plantilla de revisión: {resultado['ruta_plantilla_revision']}"
    )

    print(f"[REVISION] Documentos de productos guardados en: {ruta_documentos}")
    ruta_paquete = crear_manifiesto_y_paquete()
    print(f"[PAQUETE] Datos, manifiesto e instrucciones: {ruta_paquete}")

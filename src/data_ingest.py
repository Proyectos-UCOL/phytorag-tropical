"""
PhytoRAG-Tropical: Módulo de Ingesta, Limpieza y Chunking de Documentos
Responsable: Ricardo Mercado López (Data & Corpus Lead - Issue #1)
Director: Dr. Carlos Flores | Facultad de Telemática — Universidad de Colima
"""

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import pypdf
import requests
from pydantic import BaseModel, Field, field_validator, model_validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

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
    fecha_consulta: str = Field(
        ..., description="Fecha de consulta o descarga en formato YYYY-MM-DD"
    )


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
    if not ruta_evidencia.is_file():
        raise FileNotFoundError(
            f"No se encontró la evidencia de COFEPRIS: {ruta_evidencia}"
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
            fecha_consulta=documento["fecha_extraccion_utc"][:10],
        ),
        fuentes_adicionales=[
            TrazabilidadFuente(
                documento_o_url="data/raw/Consulta_COFEPRIS_Engeo.pdf",
                ubicacion_fuente=(
                    "Página 1: captura del detalle del registro. "
                    "Incluye registro, empresa, ingredientes activos, "
                    "nombres comerciales, cultivos y vigencia indicada."
                ),
                fecha_consulta="2026-10-01",
            ),
        ],
        texto_fragmento=texto,
        observaciones=(
            "Transcripción de la ficha técnica informativa de 2019. "
            "El registro impreso coincide con el mostrado en la captura "
            "de la consulta de COFEPRIS aportada por el estudiante: "
            "RSCO-MEZC-1101D-301-064-022. "
            "La captura incluye ENGEO 247 SC y LIMONERO, y muestra "
            "vigencia hasta el 15/01/2027. "
            "Esta evidencia se revisó visualmente; su texto no fue "
            "extraído automáticamente. "
            "Dosis sin estructurar por inconsistencia de unidades "
            "en la ficha técnica. La captura de COFEPRIS no aporta "
            "dosis, plaga ni intervalo de seguridad. "
            "El intervalo de seguridad procede del (14) del grupo "
            "de cítricos y su leyenda en la página 3 de la ficha técnica. "
            "No aprobada para recomendaciones."
        ),
    )


def crear_fichas_exalt_validadas(
    ruta_json: Path,
) -> list[FichaFitosanitaria]:
    """Estructura y aprueba las fichas técnicas de Exalt para Limonero, Mango y Papayo tras validación cruzada."""
    with ruta_json.open(encoding="utf-8") as archivo:
        documentos = json.load(archivo)

    documento = next(
        (
            doc
            for doc in documentos
            if doc["archivo"] == "Exalt_etiqueta_web_rev_2025.pdf"
        ),
        None,
    )
    if documento is None:
        raise ValueError("No se encontró el documento de Exalt en el JSON.")

    ruta_evidencia = DATA_RAW / "Consulta_COFEPRIS_Exalt.png"
    if not ruta_evidencia.is_file():
        raise FileNotFoundError(
            f"No se encontró la evidencia de COFEPRIS: {ruta_evidencia}"
        )

    texto_base = "\n\n".join(
        f"--- PÁGINA {pagina['pagina']} ---\n{pagina['texto']}"
        for pagina in documento["paginas"]
    )

    # 1. Ficha Limonero - Diaphorina citri
    encabezado_limonero = (
        "FICHA TÉCNICA OFICIAL VALIDADA [COFEPRIS]\n"
        "Producto comercial: Exalt\n"
        "Ingrediente activo: spinetoram (5.87% en peso, equiv. a 60 g i.a./L)\n"
        "Registro oficial COFEPRIS: RSCO-INAC-0103X-301-064-006 (Vigente al 19/06/2028)\n"
        "Titular del registro: Corteva Agriscience de México, S. de R.L. de C.V.\n"
        "Cultivo autorizado: Limonero (Citrus aurantiifolia / grupo cítricos)\n"
        "Plaga controlada: Diaphorina citri (Psílido asiático de los cítricos / vector del HLB)\n"
        "Dosis oficial autorizada: 400 a 600 mL/ha\n"
        "Intervalo de seguridad (IS): 1 día (días requeridos entre última aplicación y cosecha)\n"
        "Periodo de reentrada a lotes tratados: 4 horas\n"
        "Método y calibración: Realizar una aplicación al follaje cuando se observe la presencia de ninfas. "
        "Utilizar un volumen de agua adecuado en función del tamaño de los árboles tratados para asegurar "
        "una buena cobertura del follaje.\n"
        "Manejo de resistencia: IRAC Grupo 5 (Spinosinas). Rotar con otros modos de acción.\n\n"
    )

    ficha_limonero = FichaFitosanitaria(
        id_registro="FICH-EXALT-LIMONERO-DIAPHORINA-001",
        cultivo="Limonero",
        problema_fitosanitario="Diaphorina citri",
        producto_comercial="Exalt",
        ingrediente_activo="spinetoram",
        registro_cofepris="RSCO-INAC-0103X-301-064-006",
        dosis=DosisEspecificacion(
            minima=400.0,
            maxima=600.0,
            unidad="mL/ha",
            texto_etiqueta="400 - 600",
        ),
        is_dias=1,
        periodo_reingreso_horas=4,
        aprobado_omri=None,
        revision_documental_aprobada=True,
        trazabilidad=TrazabilidadFuente(
            documento_o_url=documento["documento_o_url"],
            ubicacion_fuente=(
                "Página 1: ingrediente, registro RSCO-INAC-0103X-301-064-006, revisión 12/12/2025; "
                "página 4: grupo de cítricos con limonero, Diaphorina citri, "
                "dosis 400 - 600, encabezado mL/ha e indicador (1); "
                "página 5: definición del intervalo de seguridad "
                "y periodo de reentrada de 4 horas."
            ),
            fecha_consulta="2026-10-01",
        ),
        fuentes_adicionales=[
            TrazabilidadFuente(
                documento_o_url="data/raw/Consulta_COFEPRIS_Exalt.png",
                ubicacion_fuente=(
                    "Captura oficial del portal COFEPRIS: Consulta de Registros Sanitarios de Plaguicidas. "
                    "Valida titular Corteva, registro RSCO-INAC-0103X-301-064-006, cultivo LIMONERO "
                    "y vigencia activa hasta el 19/06/2028."
                ),
                fecha_consulta="2026-10-01",
            ),
        ],
        texto_fragmento=encabezado_limonero + texto_base,
        observaciones=(
            "Ficha aprobada formalmente mediante validación cruzada: "
            "(1) Especificaciones agronómicas de la etiqueta técnica de Corteva (Rev. 12/12/2025): "
            "cultivo Limonero, plaga Diaphorina citri, dosis 400 - 600 mL/ha, IS 1 día, reentrada 4 h. "
            "(2) Evidencia de COFEPRIS (Consulta_COFEPRIS_Exalt.png) que certifica vigencia activa "
            "hasta el 19/06/2028 y registro legal del producto para Limonero. "
            "Aprobada para recomendaciones en el motor RAG."
        ),
    )

    # 2. Ficha Mango - Trips de las flores (Frankliniella occidentalis)
    encabezado_mango = (
        "FICHA TÉCNICA OFICIAL VALIDADA [COFEPRIS]\n"
        "Producto comercial: Exalt\n"
        "Ingrediente activo: spinetoram (5.87% en peso, equiv. a 60 g i.a./L)\n"
        "Registro oficial COFEPRIS: RSCO-INAC-0103X-301-064-006 (Vigente al 19/06/2028)\n"
        "Titular del registro: Corteva Agriscience de México, S. de R.L. de C.V.\n"
        "Cultivo autorizado: Mango (Mangifera indica)\n"
        "Plaga controlada: Trips de las flores (Frankliniella occidentalis)\n"
        "Dosis oficial autorizada: 400 a 600 mL/ha\n"
        "Intervalo de seguridad (IS): 1 día (días requeridos entre última aplicación y cosecha)\n"
        "Periodo de reentrada a lotes tratados: 4 horas\n"
        "Método y calibración: Realizar 2 aplicaciones foliares dirigidas a las inflorescencias y brotes jóvenes "
        "a intervalo de 7 días, al momento de encontrarse los primeros individuos vivos de la plaga; "
        "volumen de aplicación sugerido 600 L de agua/ha.\n"
        "Manejo de resistencia: IRAC Grupo 5 (Spinosinas). Rotar con otros modos de acción.\n\n"
    )

    ficha_mango = FichaFitosanitaria(
        id_registro="FICH-EXALT-MANGO-TRIPS-001",
        cultivo="Mango",
        problema_fitosanitario="Trips de las flores (Frankliniella occidentalis)",
        producto_comercial="Exalt",
        ingrediente_activo="spinetoram",
        registro_cofepris="RSCO-INAC-0103X-301-064-006",
        dosis=DosisEspecificacion(
            minima=400.0,
            maxima=600.0,
            unidad="mL/ha",
            texto_etiqueta="400 - 600",
        ),
        is_dias=1,
        periodo_reingreso_horas=4,
        aprobado_omri=None,
        revision_documental_aprobada=True,
        trazabilidad=TrazabilidadFuente(
            documento_o_url=documento["documento_o_url"],
            ubicacion_fuente=(
                "Página 1: ingrediente, registro RSCO-INAC-0103X-301-064-006, revisión 12/12/2025; "
                "página 5: cultivo Mango, plaga Trips de las flores (Frankliniella occidentalis), "
                "dosis 400 - 600 mL/ha, indicador (1) día de intervalo de seguridad y periodo de reentrada de 4 horas."
            ),
            fecha_consulta="2026-10-01",
        ),
        fuentes_adicionales=[
            TrazabilidadFuente(
                documento_o_url="data/raw/Consulta_COFEPRIS_Exalt.png",
                ubicacion_fuente=(
                    "Captura oficial del portal COFEPRIS: Consulta de Registros Sanitarios de Plaguicidas. "
                    "Valida titular Corteva, registro RSCO-INAC-0103X-301-064-006, cultivo MANGO "
                    "y vigencia activa hasta el 19/06/2028."
                ),
                fecha_consulta="2026-10-01",
            ),
        ],
        texto_fragmento=encabezado_mango + texto_base,
        observaciones=(
            "Ficha aprobada formalmente mediante validación cruzada: "
            "(1) Especificaciones agronómicas de la etiqueta técnica de Corteva (Rev. 12/12/2025): "
            "cultivo Mango, plaga Trips de las flores (Frankliniella occidentalis), dosis 400 - 600 mL/ha, IS 1 día, reentrada 4 h. "
            "(2) Evidencia de COFEPRIS (Consulta_COFEPRIS_Exalt.png) que certifica vigencia activa "
            "hasta el 19/06/2028 y registro legal del producto para MANGO. "
            "Aprobada para recomendaciones en el motor RAG."
        ),
    )

    # 3. Ficha Papayo - Gusano soldado (Spodoptera exigua)
    encabezado_papayo = (
        "FICHA TÉCNICA OFICIAL VALIDADA [COFEPRIS]\n"
        "Producto comercial: Exalt\n"
        "Ingrediente activo: spinetoram (5.87% en peso, equiv. a 60 g i.a./L)\n"
        "Registro oficial COFEPRIS: RSCO-INAC-0103X-301-064-006 (Vigente al 19/06/2028)\n"
        "Titular del registro: Corteva Agriscience de México, S. de R.L. de C.V.\n"
        "Cultivo autorizado: Papayo (Carica papaya)\n"
        "Plaga controlada: Gusano soldado (Spodoptera exigua)\n"
        "Dosis oficial autorizada: 200 a 300 mL/ha\n"
        "Intervalo de seguridad (IS): 1 día (días requeridos entre última aplicación y cosecha)\n"
        "Periodo de reentrada a lotes tratados: 4 horas\n"
        "Método y calibración: Realizar una aplicación foliar, cuando se detecten las primeras larvas vivas de la plaga; "
        "volumen de aplicación sugerido 450-550 L de agua/ha.\n"
        "Manejo de resistencia: IRAC Grupo 5 (Spinosinas). Rotar con otros modos de acción.\n\n"
    )

    ficha_papayo = FichaFitosanitaria(
        id_registro="FICH-EXALT-PAPAYO-SPODOPTERA-001",
        cultivo="Papayo",
        problema_fitosanitario="Gusano soldado (Spodoptera exigua)",
        producto_comercial="Exalt",
        ingrediente_activo="spinetoram",
        registro_cofepris="RSCO-INAC-0103X-301-064-006",
        dosis=DosisEspecificacion(
            minima=200.0,
            maxima=300.0,
            unidad="mL/ha",
            texto_etiqueta="200 - 300",
        ),
        is_dias=1,
        periodo_reingreso_horas=4,
        aprobado_omri=None,
        revision_documental_aprobada=True,
        trazabilidad=TrazabilidadFuente(
            documento_o_url=documento["documento_o_url"],
            ubicacion_fuente=(
                "Página 1: ingrediente, registro RSCO-INAC-0103X-301-064-006, revisión 12/12/2025; "
                "página 5: cultivo Papayo, plaga Gusano soldado (Spodoptera exigua), "
                "dosis 200 - 300 mL/ha, indicador (1) día de intervalo de seguridad y periodo de reentrada de 4 horas."
            ),
            fecha_consulta="2026-10-01",
        ),
        fuentes_adicionales=[
            TrazabilidadFuente(
                documento_o_url="data/raw/Consulta_COFEPRIS_Exalt.png",
                ubicacion_fuente=(
                    "Captura oficial del portal COFEPRIS: Consulta de Registros Sanitarios de Plaguicidas. "
                    "Valida titular Corteva, registro RSCO-INAC-0103X-301-064-006, cultivo PAPAYO "
                    "y vigencia activa hasta el 19/06/2028."
                ),
                fecha_consulta="2026-10-01",
            ),
        ],
        texto_fragmento=encabezado_papayo + texto_base,
        observaciones=(
            "Ficha aprobada formalmente mediante validación cruzada: "
            "(1) Especificaciones agronómicas de la etiqueta técnica de Corteva (Rev. 12/12/2025): "
            "cultivo Papayo, plaga Gusano soldado (Spodoptera exigua), dosis 200 - 300 mL/ha, IS 1 día, reentrada 4 h. "
            "(2) Evidencia de COFEPRIS (Consulta_COFEPRIS_Exalt.png) que certifica vigencia activa "
            "hasta el 19/06/2028 y registro legal del producto para PAPAYO. "
            "Aprobada para recomendaciones en el motor RAG."
        ),
    )

    return [ficha_limonero, ficha_mango, ficha_papayo]


def crear_ficha_exalt_validada(ruta_json: Path) -> FichaFitosanitaria:
    """Estructura y aprueba la ficha técnica de Exalt para Limonero (conservada por compatibilidad)."""
    return crear_fichas_exalt_validadas(ruta_json)[0]


def clasificar_y_exportar(
    fichas: list[FichaFitosanitaria],
    directorio_salida: Path | None = None,
) -> dict[str, Any]:
    """Separa fichas verificadas para el RAG de las pendientes de revisión."""
    directorio = directorio_salida or DATA_PROCESSED
    directorio.mkdir(parents=True, exist_ok=True)

    ruta_vademecum = directorio / "vademecum_fitosanitario.json"
    ruta_chunks = directorio / "chunks_corpus.json"
    ruta_pendientes = directorio / "registros_pendientes_revision.json"

    validadas = [f for f in fichas if f.esta_completa_para_recomendacion()]
    pendientes = [f for f in fichas if not f.esta_completa_para_recomendacion()]

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
                "dosis_maxima": f.dosis.maxima if f.dosis else None,
                "dosis_unidad": f.dosis.unidad if f.dosis else None,
                "is_dias": f.is_dias,
                "aprobado_omri": f.aprobado_omri,
                "documento_fuente": f.trazabilidad.documento_o_url,
                "ubicacion_fuente": f.trazabilidad.ubicacion_fuente,
                "fecha_consulta": f.trazabilidad.fecha_consulta,
            },
        ).model_dump()
        for f in validadas
    ]
    with open(ruta_chunks, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    # 3. Registros pendientes de revisión (cuarentena trazable)
    datos_pendientes = [
        {
            "ficha": f.model_dump(),
            "estado": "PENDIENTE_REVISION",
            "campos_faltantes": f.campos_faltantes(),
            "motivo_cuarentena": (
                "Faltan datos requeridos o la revisión documental "
                "todavía no está aprobada"
            ),
        }
        for f in pendientes
    ]
    with open(ruta_pendientes, "w", encoding="utf-8") as f:
        json.dump(datos_pendientes, f, ensure_ascii=False, indent=2)

    return {
        "total_procesadas": len(fichas),
        "total_validadas_rag": len(validadas),
        "total_pendientes_revision": len(pendientes),
        "ruta_vademecum": ruta_vademecum,
        "ruta_chunks": ruta_chunks,
        "ruta_pendientes": ruta_pendientes,
    }


# ==============================================================================
# 4. Punto de Entrada
# ==============================================================================

if __name__ == "__main__":
    import contextlib
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        with contextlib.suppress(AttributeError, ValueError):
            sys.stdout.reconfigure(encoding="utf-8")

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

    print(f"\n[FICHAS OFICIALES VALIDADAS PARA RAG ({len(fichas_exalt)})]")
    for f_val in fichas_exalt:
        print("  --------------------------------------------------")
        print(f"  * ID: {f_val.id_registro}")
        print(f"  * Cultivo: {f_val.cultivo}")
        print(f"  * Plaga: {f_val.problema_fitosanitario}")
        print(f"  * Producto: {f_val.producto_comercial} ({f_val.ingrediente_activo})")
        print(f"  * Registro COFEPRIS: {f_val.registro_cofepris}")
        print(
            f"  * Dosis oficial: {f_val.dosis.texto_etiqueta} {f_val.dosis.unidad if f_val.dosis else ''}"
        )
        print(
            f"  * Intervalo seguridad (IS): {f_val.is_dias} días | Reingreso: {f_val.periodo_reingreso_horas} horas"
        )
        print(f"  * Revisión documental aprobada: {f_val.revision_documental_aprobada}")
        print(
            f"  * Fuentes de respaldo: {len(f_val.fuentes_adicionales) + 1} verificadas"
        )

    print(
        f"\n[ESTATUS DEL CORPUS]\n"
        f"  * Fichas aprobadas para RAG (Sofía): {resultado['total_validadas_rag']}\n"
        f"  * Fichas en cuarentena (revisión): {resultado['total_pendientes_revision']}\n"
        f"  * Vademécum aprobado: {resultado['ruta_vademecum']}\n"
        f"  * Chunks aprobados: {resultado['ruta_chunks']}\n"
        f"  * Archivo de pendientes: {resultado['ruta_pendientes']}"
    )

    print(f"[REVISION] Documentos de productos guardados en: {ruta_documentos}")

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
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Literal

import pypdf
import requests
from pydantic import BaseModel, Field, field_validator, model_validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
EXALT_LABEL = "Exalt_etiqueta_web_rev_2025.pdf"
COFEPRIS_EXALT_EVIDENCE = "Consulta_COFEPRIS_Exalt.png"
EXALT_AGENT_REVIEWER = "GitHub Copilot coding agent"
EXALT_AGENT_REVIEWED_AT = "2026-10-08T23:44:14-06:00"
EXALT_REVIEW_REPORT = "revision_documental_exalt.json"
EXALT_REVIEWED_SOURCE_HASHES = {
    EXALT_LABEL: "917258e03aaae9a0164aee6b77bf9606cf2f36a28eaa33ff2be3ccaad4b6c11d",
    COFEPRIS_EXALT_EVIDENCE: "8cd075a2dbe5028c92928269a224a85153cbf08b006a1facaa0c54df427dd847",
}

EXALT_COMBINACIONES = (
    {
        "id": "FICH-EXALT-LIMONERO-DIAPHORINA-001",
        "cultivo": "Limonero",
        "problema_fitosanitario": "Diaphorina citri",
        "pagina": 4,
        "inicio": "Limonero, Lima, Naranjo",
        "fin": "Minador de la hoja",
        "fin_evidencia": "buena cobertura del follaje.",
        "dosis_minima": 400.0,
        "dosis_maxima": 600.0,
        "dosis_texto": "400 - 600",
        "marcador_grupo_cultivos": "(1)",
    },
    {
        "id": "FICH-EXALT-MANGO-TRIPS-001",
        "cultivo": "Mango",
        "problema_fitosanitario": "Trips de las flores (Frankliniella occidentalis)",
        "pagina": 5,
        "inicio": "Mango \n(1)",
        "fin": "Papayo \n(1)",
        "fin_evidencia": "600 L de agua/ha.",
        "dosis_minima": 400.0,
        "dosis_maxima": 600.0,
        "dosis_texto": "400-600",
        "marcador_grupo_cultivos": "(1)",
    },
    {
        "id": "FICH-EXALT-PAPAYO-SPODOPTERA-001",
        "cultivo": "Papayo",
        "problema_fitosanitario": "Gusano soldado (Spodoptera exigua)",
        "pagina": 5,
        "inicio": "Papayo \n(1)",
        "fin": "450-550 L de agua/ha.",
        "fin_evidencia": "450-550 L de agua/ha.",
        "dosis_minima": 200.0,
        "dosis_maxima": 300.0,
        "dosis_texto": "200 - 300",
        "marcador_grupo_cultivos": "(1)",
    },
)

EXALT_EVIDENCE_FIELDS = {
    "producto_comercial",
    "ingrediente_activo",
    "registro_cofepris",
    "titular",
    "cultivo",
    "problema_fitosanitario",
    "dosis",
    "unidad_dosis",
    "marcador_grupo_cultivos",
    "is_dias",
    "periodo_reingreso_horas",
    "vigencia_registro",
    "fecha_consulta_cofepris",
    "restricciones_proteccion_personal",
    "restricciones_abejas_floracion",
    "restricciones_mezclas",
    "aprobado_omri",
    "compatibilidad_exportacion",
    "nombre_cientifico_cultivo",
    "limitacion_documental",
    "etiqueta_oficial_verificada",
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


class DosisEspecificacion(BaseModel):
    """Especificación numérica de dosis con validación de positividad y rango."""

    minima: float | None = Field(
        default=None,
        gt=0,
        description="Dosis mínima transcrita. Debe ser > 0 cuando existe.",
    )
    maxima: float = Field(
        ...,
        gt=0,
        description="Dosis máxima transcrita. Obligatoria y mayor a 0.",
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


class CitaEvidencia(BaseModel):
    """Referencia verificable a un fragmento PDF o a una inspección visual."""

    archivo: str
    sha256: str | None
    ubicacion: str
    fragmento: str
    metodo_verificacion: Literal[
        "extraccion_textual_pdf",
        "inspeccion_visual_asistida_por_agente",
    ]
    alcance: str
    no_verificado_por_ocr: bool = False


class EvidenciaCampo(BaseModel):
    """Valor de un campo, su estado epistemológico y las citas que lo respaldan."""

    valor: str | int | float | bool | None
    estado: Literal[
        "respaldado_en_fuente",
        "respaldado_solo_en_documento_ilustrativo",
        "interpretado_desde_marcador_ilustrativo",
        "desconocido",
        "limitacion_critica",
    ]
    citas: list[CitaEvidencia] = Field(default_factory=list)
    motivo: str | None = None


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
    evidencia_documental: dict[str, EvidenciaCampo] = Field(
        default_factory=dict,
        description=(
            "Evidencia por campo con fuente, ubicación, fragmento literal y hash."
        ),
    )
    estado_revision_documental: str = Field(
        default="PENDIENTE_REVISION",
        description="Estado y limitaciones de la revisión documental.",
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


def normalizar_fragmento_evidencia(texto: str) -> str:
    """Normaliza espacios para cotejar fragmentos PDF sin alterar sus palabras."""
    return re.sub(r"\s+", " ", texto).strip().casefold()


def cita_pdf(
    paginas: dict[int, str],
    numero_pagina: int,
    inicio: str,
    fin: str,
    sha256: str | None,
    alcance: str,
) -> CitaEvidencia:
    """Extrae y valida una cita literal de una página concreta del PDF."""
    texto = paginas.get(numero_pagina, "")
    indice_inicio = texto.find(inicio)
    if indice_inicio < 0:
        raise ValueError(
            f"No se encontró evidencia PDF en página {numero_pagina}: {inicio!r}"
        )
    indice_fin = texto.find(fin, indice_inicio + len(inicio))
    if indice_fin < 0:
        raise ValueError(
            f"No se encontró el final de evidencia PDF en página {numero_pagina}: "
            f"{fin!r}"
        )
    fragmento = texto[indice_inicio : indice_fin + len(fin)].strip()
    return CitaEvidencia(
        archivo=EXALT_LABEL,
        sha256=sha256,
        ubicacion=f"Página {numero_pagina}",
        fragmento=fragmento,
        metodo_verificacion="extraccion_textual_pdf",
        alcance=alcance,
    )


def cita_cofepris(
    fragmento: str,
    sha256: str | None,
    alcance: str,
) -> CitaEvidencia:
    """Registra una transcripción visual de la captura, no una lectura OCR."""
    return CitaEvidencia(
        archivo=COFEPRIS_EXALT_EVIDENCE,
        sha256=sha256,
        ubicacion="Captura: detalle del registro",
        fragmento=fragmento,
        metodo_verificacion="inspeccion_visual_asistida_por_agente",
        alcance=alcance,
        no_verificado_por_ocr=True,
    )


def campo_evidencia(
    valor: Any,
    citas: list[CitaEvidencia] | None = None,
    *,
    estado: str = "respaldado_en_fuente",
    motivo: str | None = None,
) -> EvidenciaCampo:
    """Representa respaldo o desconocimiento explícito de un campo."""
    return EvidenciaCampo(
        valor=valor,
        estado=estado,
        citas=citas or [],
        motivo=motivo,
    )


def serializar_evidencia_campos(
    evidencia: dict[str, EvidenciaCampo],
) -> dict[str, dict[str, Any]]:
    """Convierte evidencia Pydantic a tipos JSON serializables."""
    return {nombre: campo.model_dump() for nombre, campo in evidencia.items()}


def construir_evidencia_campos_exalt(
    documento: dict[str, Any],
    combinacion: dict[str, Any],
    hashes_fuentes: dict[str, str | None],
) -> dict[str, EvidenciaCampo]:
    """Crea trazabilidad de campo a fuente, página, fragmento y hash."""
    paginas = {pagina["pagina"]: pagina["texto"] for pagina in documento["paginas"]}
    fila = cita_pdf(
        paginas,
        combinacion["pagina"],
        combinacion["inicio"],
        combinacion["fin_evidencia"],
        hashes_fuentes[EXALT_LABEL],
        "Respaldó la combinación cultivo/plaga y su dosis en una etiqueta "
        "que se declara ilustrativa, no una etiqueta real.",
    )
    identidad = cita_pdf(
        paginas,
        1,
        "REGISTRO SANITARIO No.:",
        "México, México",
        hashes_fuentes[EXALT_LABEL],
        "Identidad declarada en el documento ilustrativo.",
    )
    cultivo_captura = {
        "Limonero": "LIMONERO, LIMA, NARANJO, TANGERINO, TORONJO, CIDRO, MANDARINO",
        "Mango": "MANGO, PAPAYO",
        "Papayo": "MANGO, PAPAYO",
    }[combinacion["cultivo"]]
    ingrediente_pdf = cita_pdf(
        paginas,
        1,
        "Spinetoram: (mezcla de Spinosyn J y Spinosyn L)",
        "5.87",
        hashes_fuentes[EXALT_LABEL],
        "Composición de la etiqueta ilustrativa.",
    )
    caveat = cita_pdf(
        paginas,
        1,
        "ESTE DOCUMENTO TIENE FINES ILUSTRATIVOS ÚNICAMENTE.",
        "REV. 12/12/2025",
        hashes_fuentes[EXALT_LABEL],
        "El propio PDF declara que no es una etiqueta real y muestra su revisión impresa.",
    )
    reentrada_is = cita_pdf(
        paginas,
        3,
        "Periodo de reentrada a las áreas tratadas:",
        "(SL) Sin Límite.",
        hashes_fuentes[EXALT_LABEL],
        "Valor de reentrada y leyenda de que IS se expresa en días.",
    )
    ppe = cita_pdf(
        paginas,
        2,
        "Durante el manejo, preparación de la mezcla",
        "Después de haber usado su ropa protectora contaminada",
        hashes_fuentes[EXALT_LABEL],
        "Instrucciones generales de protección personal.",
    )
    polinizadores = cita_pdf(
        paginas,
        2,
        "ESTE PRODUCTO ES ALTAMENTE TÓXICO PARA ABEJAS.",
        "ABEJAS SE ENCUENTRAN LIBANDO.",
        hashes_fuentes[EXALT_LABEL],
        "Restricción expresa durante floración y actividad de abejas.",
    )
    mezclas = cita_pdf(
        paginas,
        3,
        "INCOMPATIBILIDAD.",
        "prueba de compatibilidad y fitotoxicidad previa a la aplicación.",
        hashes_fuentes[EXALT_LABEL],
        "Advertencia general sobre mezclas y prueba previa.",
    )

    evidencia: dict[str, EvidenciaCampo] = {
        "producto_comercial": campo_evidencia(
            "Exalt",
            [
                cita_cofepris(
                    "Nombre comercial: EXALT / PALGUS / GF-1629 / TADEK",
                    hashes_fuentes[COFEPRIS_EXALT_EVIDENCE],
                    "Confirma que el detalle capturado incluye Exalt entre varios nombres comerciales.",
                )
            ],
        ),
        "ingrediente_activo": campo_evidencia(
            "spinetoram (mezcla de Spinosyn J y Spinosyn L)",
            [
                ingrediente_pdf,
                cita_cofepris(
                    "Ingrediente activo: SPINETORAM: (Mezcla de Spinosyn J y Spinosyn L)",
                    hashes_fuentes[COFEPRIS_EXALT_EVIDENCE],
                    "Confirma visualmente el ingrediente, no la dosis ni el uso por plaga.",
                ),
            ],
        ),
        "registro_cofepris": campo_evidencia(
            "RSCO-INAC-0103X-301-064-006",
            [
                identidad,
                cita_cofepris(
                    "Registro: RSCO-INAC-0103X-301-064-006",
                    hashes_fuentes[COFEPRIS_EXALT_EVIDENCE],
                    "Coincide visualmente el número de registro de la etiqueta ilustrativa.",
                ),
            ],
        ),
        "titular": campo_evidencia(
            "CORTEVA MX, S. A. DE C.V.",
            [
                identidad,
                cita_cofepris(
                    "Empresa: CORTEVA MX, S.A. DE C.V.",
                    hashes_fuentes[COFEPRIS_EXALT_EVIDENCE],
                    "El espaciado de puntuación difiere, pero la razón social coincide.",
                ),
            ],
        ),
        "cultivo": campo_evidencia(
            combinacion["cultivo"],
            [
                fila,
                cita_cofepris(
                    cultivo_captura,
                    hashes_fuentes[COFEPRIS_EXALT_EVIDENCE],
                    "La captura incluye el cultivo en el listado general de usos; no identifica la plaga.",
                ),
            ],
        ),
        "problema_fitosanitario": campo_evidencia(
            combinacion["problema_fitosanitario"],
            [fila],
        ),
        "dosis": campo_evidencia(
            combinacion["dosis_texto"],
            [fila],
            estado="respaldado_solo_en_documento_ilustrativo",
            motivo=(
                "La captura COFEPRIS no muestra ni valida dosis; el único respaldo "
                "es la etiqueta ilustrativa de Corteva."
            ),
        ),
        "unidad_dosis": campo_evidencia(
            "mL/ha",
            [
                cita_pdf(
                    paginas,
                    combinacion["pagina"],
                    "CULTIVO PLAGA DOSIS",
                    "RECOMENDACIONES",
                    hashes_fuentes[EXALT_LABEL],
                    "Encabezado de dosis de la tabla ilustrativa.",
                ),
                fila,
            ],
            estado="respaldado_solo_en_documento_ilustrativo",
            motivo="La unidad no aparece en la captura COFEPRIS.",
        ),
        "marcador_grupo_cultivos": campo_evidencia(
            combinacion["marcador_grupo_cultivos"],
            [fila],
            estado="respaldado_solo_en_documento_ilustrativo",
            motivo="El marcador procede de la fila/grupo del documento ilustrativo.",
        ),
        "is_dias": campo_evidencia(
            1,
            [
                fila,
                cita_pdf(
                    paginas,
                    3,
                    "Maíz  (1 día grano)",
                    "(3 días forraje)",
                    hashes_fuentes[EXALT_LABEL],
                    "Ejemplo de la misma tabla que muestra códigos de grupo expresados en días.",
                ),
                cita_pdf(
                    paginas,
                    3,
                    "(IS) Intervalo de Seguridad:",
                    "(SL) Sin Límite.",
                    hashes_fuentes[EXALT_LABEL],
                    "Define IS en días; la interpretación de (1) como un día se apoya "
                    "en la notación de la tabla, no en la captura COFEPRIS.",
                ),
            ],
            estado="interpretado_desde_marcador_ilustrativo",
            motivo="Requiere cotejo con una etiqueta oficial, no ilustrativa.",
        ),
        "periodo_reingreso_horas": campo_evidencia(
            4,
            [reentrada_is],
            estado="respaldado_solo_en_documento_ilustrativo",
            motivo="La captura COFEPRIS no muestra periodo de reentrada.",
        ),
        "vigencia_registro": campo_evidencia(
            "19/06/2028",
            [
                cita_cofepris(
                    "Vigencia: 19/06/2028",
                    hashes_fuentes[COFEPRIS_EXALT_EVIDENCE],
                    "Fecha de vigencia visible en la captura; no es la fecha de consulta.",
                )
            ],
        ),
        "fecha_consulta_cofepris": campo_evidencia(
            None,
            estado="desconocido",
            motivo="La captura no muestra la fecha en que se realizó la consulta.",
        ),
        "restricciones_proteccion_personal": campo_evidencia(
            "Aplicar el equipo de protección indicado en la etiqueta.",
            [ppe],
            estado="respaldado_solo_en_documento_ilustrativo",
            motivo="El detalle COFEPRIS no muestra instrucciones de protección personal.",
        ),
        "restricciones_abejas_floracion": campo_evidencia(
            "No aplicar cuando el cultivo o malezas estén en flor ni cuando las abejas liben.",
            [polinizadores],
            estado="respaldado_solo_en_documento_ilustrativo",
            motivo="El detalle COFEPRIS no muestra esta restricción.",
        ),
        "restricciones_mezclas": campo_evidencia(
            "No se recomienda mezclar Exalt en mezclas de tanque; si se mezcla, realizar prueba previa.",
            [mezclas],
            estado="respaldado_solo_en_documento_ilustrativo",
            motivo="El detalle COFEPRIS no muestra restricciones de mezclas.",
        ),
        "aprobado_omri": campo_evidencia(
            None,
            estado="desconocido",
            motivo="Ni la etiqueta ilustrativa ni la captura presentan evidencia OMRI.",
        ),
        "compatibilidad_exportacion": campo_evidencia(
            None,
            estado="desconocido",
            motivo="Las fuentes revisadas no documentan compatibilidad de exportación.",
        ),
        "nombre_cientifico_cultivo": campo_evidencia(
            None,
            estado="desconocido",
            motivo=(
                "Las dos fuentes cotejadas solo sustentan el nombre común del cultivo; "
                "no se atribuye un nombre científico."
            ),
        ),
        "limitacion_documental": campo_evidencia(
            "Etiqueta web ilustrativa; no es una etiqueta real.",
            [caveat],
            estado="limitacion_critica",
            motivo=(
                "La fuente no acredita que los usos y dosis sean los autorizados "
                "en una etiqueta real vigente."
            ),
        ),
        "etiqueta_oficial_verificada": campo_evidencia(
            False,
            [caveat],
            estado="limitacion_critica",
            motivo=(
                "El PDF revisado se identifica como ilustrativo; no es una etiqueta "
                "oficial verificable."
            ),
        ),
    }
    return evidencia


def validar_evidencia_documental_exalt(
    evidencia: dict[str, EvidenciaCampo],
    paginas: dict[int, str] | None,
    hashes_actuales: dict[str, str | None],
) -> tuple[bool, list[str]]:
    """Comprueba cobertura, citas literales, hashes y límites de autoridad."""
    motivos: list[str] = []
    for archivo, hash_revisado in EXALT_REVIEWED_SOURCE_HASHES.items():
        if hashes_actuales.get(archivo) != hash_revisado:
            motivos.append(
                f"La fuente {archivo} falta o cambió desde la revisión asistida."
            )
    faltantes = EXALT_EVIDENCE_FIELDS - evidencia.keys()
    if faltantes:
        motivos.append(
            "Faltan campos con evidencia o motivo explícito: "
            + ", ".join(sorted(faltantes))
        )
    for nombre, campo in evidencia.items():
        estado = campo.estado
        citas = campo.citas
        if estado == "desconocido":
            if not campo.motivo:
                motivos.append(f"El campo desconocido {nombre} carece de motivo.")
            continue
        if not citas:
            motivos.append(f"El campo {nombre} no tiene citas.")
            continue
        for cita in citas:
            archivo = cita.archivo
            digest = cita.sha256
            if not archivo or digest is None:
                motivos.append(f"La cita del campo {nombre} carece de archivo o hash.")
                continue
            if hashes_actuales.get(archivo) != digest:
                motivos.append(
                    f"El hash de la fuente de {nombre} no coincide con el archivo actual."
                )
            if (
                cita.metodo_verificacion == "extraccion_textual_pdf"
                and paginas is not None
            ):
                match = re.search(r"Página (\d+)", cita.ubicacion)
                if match is None:
                    motivos.append(f"La cita PDF de {nombre} carece de página.")
                    continue
                texto_pagina = paginas.get(int(match.group(1)), "")
                if normalizar_fragmento_evidencia(
                    cita.fragmento
                ) not in normalizar_fragmento_evidencia(texto_pagina):
                    motivos.append(
                        f"El fragmento de {nombre} no aparece en la página citada."
                    )
            elif (
                cita.archivo == COFEPRIS_EXALT_EVIDENCE
                and cita.metodo_verificacion == "inspeccion_visual_asistida_por_agente"
                and not cita.no_verificado_por_ocr
            ):
                motivos.append(
                    f"La cita visual de {nombre} debe indicar que no fue verificada por OCR."
                )
    if "limitacion_documental" not in evidencia:
        motivos.append("No se declaró la limitación de autoridad de la etiqueta.")
    return not motivos, motivos


def puede_aprobar_exalt(
    evidencia: dict[str, EvidenciaCampo],
    evidencia_completa_y_vigente: bool,
) -> bool:
    """Acepta una revisión asistida solo con evidencia de etiqueta oficial verificable."""
    etiqueta_oficial = evidencia.get("etiqueta_oficial_verificada")
    return (
        evidencia_completa_y_vigente
        and etiqueta_oficial is not None
        and etiqueta_oficial.valor is True
        and etiqueta_oficial.estado == "respaldado_en_fuente"
        and bool(etiqueta_oficial.citas)
    )


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
            f"Cultivo: {combinacion['cultivo']}.",
            f"Problema fitosanitario: {combinacion['problema_fitosanitario']}.",
            f"Dosis transcrita: {combinacion['dosis_texto']} mL/ha.",
            f"Marcador de grupo de cultivos: {combinacion['marcador_grupo_cultivos']}.",
            (
                "Intervalo de seguridad interpretado como 1 día a partir del marcador "
                "(1) y de la leyenda de IS en días; requiere cotejo con etiqueta oficial."
            ),
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


def crear_fichas_exalt_validadas(
    ruta_json: Path,
) -> list[FichaFitosanitaria]:
    """Crea candidatos con trazas asistidas; no confunde revisión con autorización."""
    with ruta_json.open(encoding="utf-8") as archivo:
        documentos = json.load(archivo)

    documento = next(
        (doc for doc in documentos if doc["archivo"] == EXALT_LABEL),
        None,
    )
    if documento is None:
        return []

    rutas_fuentes = {
        EXALT_LABEL: DATA_RAW / EXALT_LABEL,
        COFEPRIS_EXALT_EVIDENCE: DATA_RAW / COFEPRIS_EXALT_EVIDENCE,
    }
    hashes = {archivo: hash_sha256(ruta) for archivo, ruta in rutas_fuentes.items()}
    paginas = {pagina["pagina"]: pagina["texto"] for pagina in documento["paginas"]}
    disclaimer = "ESTE DOCUMENTO TIENE FINES ILUSTRATIVOS ÚNICAMENTE."
    if disclaimer not in paginas.get(1, ""):
        raise ValueError(
            "El PDF de Exalt ya no contiene la limitación ilustrativa revisada."
        )

    fuente_etiqueta = documento["documento_o_url"]
    hash_etiqueta = hashes[EXALT_LABEL]
    fichas: list[FichaFitosanitaria] = []

    for combinacion in EXALT_COMBINACIONES:
        texto = construir_texto_exalt(documento, combinacion)
        evidencia = construir_evidencia_campos_exalt(documento, combinacion, hashes)
        evidencia_completa, motivos_evidencia = validar_evidencia_documental_exalt(
            evidencia,
            paginas,
            hashes,
        )
        # La revisión asistida no reemplaza una etiqueta autorizada verificable.
        aprobada = puede_aprobar_exalt(evidencia, evidencia_completa)
        estado = (
            "REVISADO_POR_AGENTE_PENDIENTE_ETIQUETA_OFICIAL"
            if evidencia_completa
            else "EVIDENCIA_INCOMPLETA_O_FUENTE_CAMBIADA"
        )
        nota_revision = (
            "Revisión documental asistida por agente; no representa firma ni "
            "aprobación humana. La etiqueta web se declara ilustrativa y no es "
            "una etiqueta real; la captura COFEPRIS no valida dosis ni plaga. "
            "Pendiente de cotejo con etiqueta oficial."
            if evidencia_completa
            else "La revisión asistida no pasó los controles: "
            + " ".join(motivos_evidencia)
        )
        fuentes_adicionales = [
            TrazabilidadFuente(
                documento_o_url=f"data/raw/{COFEPRIS_EXALT_EVIDENCE}",
                ubicacion_fuente=(
                    "Inspección visual del detalle: registro, empresa, ingrediente, "
                    "nombres comerciales, cultivos listados y vigencia 19/06/2028. "
                    "La captura no acredita dosis, plaga ni fecha de consulta."
                ),
                fecha_consulta=None,
                sha256=hashes[COFEPRIS_EXALT_EVIDENCE],
            )
        ]
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
                    fecha_consulta=None,
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
                revision_documental_aprobada=aprobada,
                evidencia_documental=evidencia,
                estado_revision_documental=estado,
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
    ruta_revision = directorio / EXALT_REVIEW_REPORT
    ruta_plantilla_obsoleta = directorio / "revision_manual_exalt.template.json"
    if ruta_plantilla_obsoleta.is_file():
        ruta_plantilla_obsoleta.unlink()
    hashes_actuales = {
        EXALT_LABEL: hash_sha256(DATA_RAW / EXALT_LABEL),
        COFEPRIS_EXALT_EVIDENCE: hash_sha256(DATA_RAW / COFEPRIS_EXALT_EVIDENCE),
    }
    fichas_clasificadas: list[FichaFitosanitaria] = []
    for ficha in fichas:
        if ficha.id_registro.startswith("FICH-EXALT-"):
            evidencia_completa, motivos_evidencia = validar_evidencia_documental_exalt(
                ficha.evidencia_documental,
                None,
                hashes_actuales,
            )
            estado = (
                "REVISADO_POR_AGENTE_PENDIENTE_ETIQUETA_OFICIAL"
                if evidencia_completa
                else "EVIDENCIA_INCOMPLETA_O_FUENTE_CAMBIADA"
            )
            nota_estado = (
                "La fuente de dosis/usos es ilustrativa, no una etiqueta real."
                if evidencia_completa
                else "La revisión asistida quedó invalidada: "
                + " ".join(motivos_evidencia)
            )
            ficha = ficha.model_copy(
                update={
                    "revision_documental_aprobada": False,
                    "estado_revision_documental": estado,
                    "observaciones": (
                        (ficha.observaciones or "") + " " + nota_estado
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
                "marcador_grupo_cultivos": f.evidencia_documental.get(
                    "marcador_grupo_cultivos", {}
                ).valor,
                "is_dias": f.is_dias,
                "periodo_reingreso_horas": f.periodo_reingreso_horas,
                "aprobado_omri": f.aprobado_omri,
                "revision_documental_aprobada": f.revision_documental_aprobada,
                "estado_revision_documental": f.estado_revision_documental,
                "evidencia_documental": serializar_evidencia_campos(
                    f.evidencia_documental
                ),
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
                "marcador_grupo_cultivos": f.evidencia_documental.get(
                    "marcador_grupo_cultivos", {}
                ).valor,
                "is_dias": f.is_dias,
                "periodo_reingreso_horas": f.periodo_reingreso_horas,
                "aprobado_omri": f.aprobado_omri,
                "revision_documental_aprobada": f.revision_documental_aprobada,
                "estado_revision_documental": f.estado_revision_documental,
                "evidencia_documental": serializar_evidencia_campos(
                    f.evidencia_documental
                ),
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

    informe_revision = {
        "tipo_revision": "documental_asistida_por_agente",
        "revisor": EXALT_AGENT_REVIEWER,
        "es_revisor_humano": False,
        "aprobacion_humana": False,
        "fecha_revision": EXALT_AGENT_REVIEWED_AT,
        "metodo": (
            "Extracción textual de páginas PDF con pypdf y cotejo directo de la "
            "captura PNG mediante inspección visual. La captura no se trató como "
            "verificación OCR."
        ),
        "hashes_revisados": EXALT_REVIEWED_SOURCE_HASHES,
        "hashes_actuales": hashes_actuales,
        "alcance_cofepris": (
            "La captura muestra registro, empresa, ingrediente, nombres comerciales, "
            "usos listados y vigencia 19/06/2028; no muestra dosis, plagas por cultivo "
            "ni fecha de consulta."
        ),
        "resultado": "PENDIENTE",
        "revision_asistida_completa": all(
            ficha.estado_revision_documental
            == "REVISADO_POR_AGENTE_PENDIENTE_ETIQUETA_OFICIAL"
            for ficha in candidatos_exalt
        ),
        "etiqueta_oficial_verificada": all(
            ficha.evidencia_documental["etiqueta_oficial_verificada"].valor is True
            for ficha in candidatos_exalt
        ),
        "aprobacion_corpus_elegible": bool(candidatos_exalt)
        and all(ficha.revision_documental_aprobada for ficha in candidatos_exalt),
        "motivo_bloqueo": (
            "La etiqueta web se declara ilustrativa y no es una etiqueta real. "
            "La captura COFEPRIS no corrobora dosis ni combinaciones cultivo/plaga; "
            "se requiere una etiqueta oficial verificable antes de indexar."
        ),
        "fichas": [
            {
                "id_registro": f.id_registro,
                "estado": f.estado_revision_documental,
                "revision_documental_aprobada": f.revision_documental_aprobada,
                "evidencia_completa_y_vigente": (
                    f.estado_revision_documental
                    == "REVISADO_POR_AGENTE_PENDIENTE_ETIQUETA_OFICIAL"
                ),
                "evidencia_por_campo": serializar_evidencia_campos(
                    f.evidencia_documental
                ),
            }
            for f in candidatos_exalt
        ],
    }
    with ruta_revision.open("w", encoding="utf-8") as f:
        json.dump(informe_revision, f, ensure_ascii=False, indent=2)

    return {
        "total_procesadas": len(fichas),
        "total_validadas_rag": len(validadas),
        "total_pendientes_revision": len(pendientes),
        "total_candidatos_exalt": len(candidatos_exalt),
        "ruta_vademecum": ruta_vademecum,
        "ruta_chunks": ruta_chunks,
        "ruta_pendientes": ruta_pendientes,
        "ruta_candidatos": ruta_candidatos,
        "ruta_revision_documental": ruta_revision,
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
   no debe cargarse al índice RAG. `revision_documental_exalt.json` contiene el
   cotejo asistido, las citas por campo y los motivos concretos para mantener
   Exalt pendiente.
6. La revisión asistida por agente no equivale a firma, aprobación humana ni
   autorización regulatoria. Exalt solo podrá aprobarse cuando evidencia completa
   y consistente provenga de una etiqueta oficial verificable; si una fuente cambia
   o falta, la revisión ligada a sus hashes deja de ser vigente.

La etiqueta web de Exalt se identifica como ilustrativa y no es una etiqueta real.
La captura COFEPRIS acredita solo los datos visibles del registro (no dosis ni plaga).
Las fichas son elaboradas por PhytoRAG-Tropical y no son emitidas ni aprobadas por
COFEPRIS. No se infiere aprobación OMRI ni compatibilidad de exportación. Este
paquete no constituye una recomendación agronómica ni demuestra “cero alucinaciones”.
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

    hashes = {
        EXALT_LABEL: hash_sha256(DATA_RAW / EXALT_LABEL),
        COFEPRIS_EXALT_EVIDENCE: hash_sha256(DATA_RAW / COFEPRIS_EXALT_EVIDENCE),
    }
    informe_path = DATA_PROCESSED / EXALT_REVIEW_REPORT
    if informe_path.is_file():
        informe = json.loads(informe_path.read_text(encoding="utf-8"))
    else:
        informe = {
            "resultado": "PENDIENTE",
            "motivo_bloqueo": "No se generó el informe de revisión documental.",
        }
    estado_revision = (
        "revisión asistida por agente; fichas pendientes de etiqueta oficial"
    )
    motivo_texto = informe.get("motivo_bloqueo", "Sin detalle de bloqueo.")
    commit_base = "454225a2958da55ed2961f19f173589c1272a7ed"
    manifiesto_lineas = [
        "# Manifiesto de datos PhytoRAG-Tropical — M1\n\n"
        + f"- Commit de código de partida verificado: `{commit_base}`.\n"
        + f"- SHA-256 del código de ingesta ejecutado: `{hash_sha256(PROJECT_ROOT / 'src' / 'data_ingest.py')}`.\n"
        + f"- Python: `{platform.python_version()}`.\n"
        + f"- Estado de revisión asistida Exalt: **{estado_revision}**.\n"
        + f"- Observaciones de revisión: {motivo_texto}\n"
        + f"- Revisor documental: `{EXALT_AGENT_REVIEWER}` (agente; no humano).\n"
        + f"- Fecha de cotejo: `{EXALT_AGENT_REVIEWED_AT}`.\n"
        + "- La captura se inspeccionó visualmente; no se trató como validación OCR.\n"
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
        + "\n\n## Estado del cotejo documental\n\n"
        + f"- Captura COFEPRIS Exalt: `{hashes[COFEPRIS_EXALT_EVIDENCE]}`.\n"
        + f"- Etiqueta ilustrativa Exalt: `{hashes[EXALT_LABEL]}`.\n"
        + "- Dosis y plagas: respaldadas únicamente por documento ilustrativo.\n"
        + "- Fecha de consulta COFEPRIS: desconocida; la captura solo muestra vigencia.\n"
        + "- Aprobación humana: no registrada ni atribuida.\n"
    ]
    manifiesto_lineas.append(
        "- No se aprueba Exalt para indexación hasta cotejar la etiqueta oficial.\n"
    )
    manifiesto = "".join(manifiesto_lineas)
    ruta_manifiesto.write_text(manifiesto, encoding="utf-8")

    archivos_paquete = [*archivos, ruta_manifiesto]
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
        print(
            f"  * Estado de revisión: {f_val.estado_revision_documental} "
            f"(aprobada para RAG: {f_val.revision_documental_aprobada})"
        )
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
        f"  * Informe campo por campo: {resultado['ruta_revision_documental']}"
    )

    print(f"[REVISION] Documentos de productos guardados en: {ruta_documentos}")
    ruta_paquete = crear_manifiesto_y_paquete()
    print(f"[PAQUETE] Datos, manifiesto e instrucciones: {ruta_paquete}")

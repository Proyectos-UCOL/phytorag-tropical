"""PhytoRAG-Tropical: Motor de Recuperación y Generación Aumentada (RAG Híbrido).

Responsable: Alumno 2 (RAG Architecture Lead) — Sofía (@SOFIARENASM)
Director: Dr. Carlos Flores | Facultad de Telemática — Universidad de Colima
"""

import json
import os
import re
from pathlib import Path
from typing import Any

import chromadb
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rank_bm25 import BM25Okapi

load_dotenv()

# Rutas estándar del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"
CORPUS_OFICIAL_FILE = DATA_PROCESSED / "corpus_motor_rag.json"

# Normalización de nombres de cultivos compartida con Alumno 1 (Ricardo: Limonero, Mango, Papayo)
MAPA_CULTIVOS_CANONICOS: dict[str, str] = {
    "limon": "limonero",
    "limón": "limonero",
    "limonero": "limonero",
    "citricos": "limonero",
    "cítricos": "limonero",
    "mango": "mango",
    "papaya": "papayo",
    "papayo": "papayo",
}


def normalizar_cultivo(cultivo: str | None) -> str:
    """Normaliza el nombre del cultivo al término canónico estándar del corpus."""
    if not cultivo:
        return ""
    c = cultivo.strip().lower().replace("ó", "o")
    return MAPA_CULTIVOS_CANONICOS.get(c, c)


class RecomendacionTratamiento(BaseModel):
    """Esquema estructurado de salida de la recomendación fitosanitaria."""

    producto_comercial: str
    ingrediente_activo: str
    registro_sanitario_cofepris: str
    dosis_autorizada: str | None = None
    intervalo_seguridad_dias: int | None = None
    aprobacion_organica_omri: bool | None = None
    compatible_exportacion_usda: bool | None = None
    recomendacion_agronomica: str
    fragmento_oficial_citado: str
    fuente_documental: str


class ResultadoRecuperacion(BaseModel):
    """Modelo estructurado que representa un fragmento documental recuperado."""

    id_documento: str = Field(
        ..., description="Identificador único de la ficha o fragmento"
    )
    texto: str = Field(..., description="Texto normativo indexado")
    score: float = Field(..., description="Puntaje de relevancia híbrida combinada")
    metadatos: dict[str, Any] = Field(
        default_factory=dict, description="Metadatos normativos asociados"
    )


class MotorPhytoRAG:
    """Motor RAG Híbrido especializado en cumplimiento fitosanitario y vademécum oficial."""

    def __init__(
        self,
        vector_db_path: Path | None = None,
        corpus_path: Path | None = None,
    ):
        self.db_path = vector_db_path or VECTOR_STORE_DIR
        self.corpus_path = corpus_path or CORPUS_OFICIAL_FILE
        self.db_path.mkdir(parents=True, exist_ok=True)
        DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

        # 1. Inicializar cliente persistente de ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=str(self.db_path))
        self.collection = self.chroma_client.get_or_create_collection(
            name="corpus_fitosanitario",
            metadata={"hnsw:space": "cosine"},
        )

        # 2. Cargar e indexar corpus oficial aprobado
        self.documentos = self._cargar_corpus()
        self._indexar_en_chromadb()

        # 3. Inicializar índice léxico BM25
        self.tokenized_corpus = [
            self._tokenizar(doc["texto_completo"]) for doc in self.documentos
        ]
        self.bm25 = BM25Okapi(self.tokenized_corpus) if self.tokenized_corpus else None

    @staticmethod
    def _tokenizar(texto: str) -> list[str]:
        """Normaliza y tokeniza texto para el índice léxico BM25."""
        texto_limpio = re.sub(r"[^\w\s]", " ", texto.lower())
        return [t for t in texto_limpio.split() if len(t) > 1]

    def _cargar_corpus(self) -> list[dict[str, Any]]:
        """Carga exclusivamente el corpus aprobado desde corpus_motor_rag.json.

        Si el archivo no existe o está vacío, arranca en limpio sin crear archivos semilla
        ni indexar archivos de cuarentena.
        """
        if not self.corpus_path.exists():
            return []

        documentos_cargados = []
        try:
            with open(self.corpus_path, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if isinstance(datos, list):
                    documentos_cargados = datos
        except (json.JSONDecodeError, OSError) as e:
            print(f"[AVISO] Error al leer archivo {self.corpus_path}: {e}")
            return []

        # Formatear documentos para indexación tolerando campos nulos
        corpus_formateado = []
        for ficha in documentos_cargados:
            is_dias = ficha.get("intervalo_seguridad_dias")
            is_dias_str = (
                f"{is_dias} días"
                if is_dias is not None
                else "No especificado / Sin límite"
            )

            omri_val = ficha.get("aprobado_omri")
            omri_str = (
                "Sí"
                if omri_val is True
                else ("No" if omri_val is False else "Desconocido")
            )

            usda_val = ficha.get("compatible_exportacion_usda")
            usda_str = (
                "Sí"
                if usda_val is True
                else ("No" if usda_val is False else "Desconocido")
            )

            dosis_str = ficha.get("dosis_autorizada") or "No especificada"

            texto_completo = (
                f"Cultivo: {ficha.get('cultivo', '')}. "
                f"Problema o Plaga: {ficha.get('problema_fitosanitario', '')}. "
                f"Producto Comercial: {ficha.get('producto_comercial', '')}. "
                f"Ingrediente Activo: {ficha.get('ingrediente_activo', '')}. "
                f"Registro COFEPRIS: {ficha.get('registro_sanitario_cofepris', '')}. "
                f"Dosis Oficial: {dosis_str}. "
                f"Intervalo de Seguridad: {is_dias_str}. "
                f"Aprobación Orgánica OMRI: {omri_str}. "
                f"Apto Exportación USDA: {usda_str}. "
                f"Detalle Oficial: {ficha.get('fragmento_oficial_citado', '')} "
                f"Recomendación: {ficha.get('recomendacion_agronomica', '')}"
            )
            corpus_formateado.append(
                {
                    "id": str(
                        ficha.get("id", ficha.get("registro_sanitario_cofepris", ""))
                    ),
                    "texto_completo": texto_completo,
                    "metadatos": ficha,
                }
            )
        return corpus_formateado

    def _indexar_en_chromadb(self):
        """Indexa los documentos en la colección de ChromaDB tolerando valores nulos."""
        if not self.documentos:
            return

        existentes = set(self.collection.get()["ids"])
        por_insertar_ids = []
        por_insertar_docs = []
        por_insertar_metadatos = []

        for doc in self.documentos:
            doc_id = doc["id"]
            if doc_id not in existentes:
                por_insertar_ids.append(doc_id)
                por_insertar_docs.append(doc["texto_completo"])

                raw_is = doc["metadatos"].get("intervalo_seguridad_dias")
                is_dias_val = int(raw_is) if raw_is is not None else -1

                # ChromaDB requiere que los valores de metadatos sean tipos primitivos
                meta_plano = {
                    "producto_comercial": str(
                        doc["metadatos"].get("producto_comercial") or ""
                    ),
                    "ingrediente_activo": str(
                        doc["metadatos"].get("ingrediente_activo") or ""
                    ),
                    "registro_sanitario_cofepris": str(
                        doc["metadatos"].get("registro_sanitario_cofepris") or ""
                    ),
                    "cultivo": str(doc["metadatos"].get("cultivo") or ""),
                    "dosis_autorizada": str(
                        doc["metadatos"].get("dosis_autorizada") or ""
                    ),
                    "intervalo_seguridad_dias": is_dias_val,
                    "aprobado_omri": str(doc["metadatos"].get("aprobado_omri")),
                    "compatible_exportacion_usda": str(
                        doc["metadatos"].get("compatible_exportacion_usda")
                    ),
                }
                por_insertar_metadatos.append(meta_plano)

        if por_insertar_ids:
            self.collection.add(
                ids=por_insertar_ids,
                documents=por_insertar_docs,
                metadatas=por_insertar_metadatos,
            )
            print(
                f"[ChromaDB] Indexados {len(por_insertar_ids)} nuevos fragmentos normativos."
            )

    def recuperar_documentos(
        self,
        query: str,
        top_k: int = 3,
        k_rrf: int = 60,
        cultivo: str | None = None,
    ) -> list[ResultadoRecuperacion]:
        """Recuperación híbrida usando Reciprocal Rank Fusion (RRF) con filtro estricto por cultivo."""
        if not self.documentos:
            return []

        tokens_query = self._tokenizar(query)
        stop_words_agronomicas = {
            "cultivo",
            "huerta",
            "arbol",
            "planta",
            "en",
            "de",
            "la",
            "el",
            "los",
            "las",
            "un",
            "una",
            "para",
            "por",
            "con",
            "etapa",
            "problema",
        }
        tokens_problema_query = [
            t for t in tokens_query if t not in stop_words_agronomicas
        ]

        # Auto-detección de cultivo si no fue provisto explícitamente
        if not cultivo:
            for c_candidato in MAPA_CULTIVOS_CANONICOS:
                if c_candidato in tokens_query or c_candidato in query.lower():
                    cultivo = c_candidato
                    break

        # 1. Recuperación léxica con BM25
        bm25_scores = (
            self.bm25.get_scores(tokens_query)
            if self.bm25
            else [0] * len(self.documentos)
        )
        ranking_bm25_indices = sorted(
            range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True
        )

        # 2. Recuperación semántica densa con ChromaDB
        res_vectorial = self.collection.query(
            query_texts=[query], n_results=min(top_k * 2, len(self.documentos))
        )
        ranking_vectorial_ids = (
            res_vectorial["ids"][0] if res_vectorial and res_vectorial["ids"] else []
        )

        # 3. Fusión por Reciprocal Rank Fusion (RRF)
        rrf_scores: dict[str, float] = {}
        docs_map: dict[str, dict[str, Any]] = {
            doc["id"]: doc for doc in self.documentos
        }

        for rank, idx in enumerate(ranking_bm25_indices[: top_k * 3]):
            doc_id = self.documentos[idx]["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (
                1.0 / (k_rrf + rank + 1)
            )

        for rank, doc_id in enumerate(ranking_vectorial_ids):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (
                1.0 / (k_rrf + rank + 1)
            )

        # Ordenar por puntaje RRF descendente
        resultados_ordenados = sorted(
            rrf_scores.items(), key=lambda item: item[1], reverse=True
        )

        # 4. Filtro Estricto por Cultivo (Anti Off-label) y Control de Relevancia Patológica
        resultados_finales: list[ResultadoRecuperacion] = []
        for doc_id, score in resultados_ordenados:
            doc_info = docs_map.get(doc_id)
            if not doc_info:
                continue

            # A) Filtro Estricto por Cultivo Normalizado
            if cultivo:
                cultivo_doc_norm = normalizar_cultivo(
                    str(doc_info["metadatos"].get("cultivo", ""))
                )
                cultivo_solic_norm = normalizar_cultivo(cultivo)
                if (
                    cultivo_solic_norm != cultivo_doc_norm
                    and cultivo_solic_norm not in cultivo_doc_norm
                ):
                    continue

            # B) Filtro de Alineación Patológica
            if tokens_problema_query:
                texto_problema_doc = self._tokenizar(
                    str(doc_info["metadatos"].get("problema_fitosanitario", ""))
                )
                coincidencias = set(tokens_problema_query).intersection(
                    set(texto_problema_doc)
                )
                if not coincidencias:
                    continue

            resultados_finales.append(
                ResultadoRecuperacion(
                    id_documento=doc_id,
                    texto=doc_info["texto_completo"],
                    score=round(score, 5),
                    metadatos=doc_info["metadatos"],
                )
            )
            if len(resultados_finales) >= top_k:
                break

        return resultados_finales

    def generar_recomendacion(
        self,
        consulta_texto: str,
        contexto: list[ResultadoRecuperacion],
        regimen: str = "convencional",
        cultivo: str | None = None,
    ) -> RecomendacionTratamiento:
        """Genera el dictamen agronómico oficial empleando guardrails deterministas estrictos."""
        # Auto-detección de cultivo si no fue provisto
        if not cultivo:
            for c_candidato in MAPA_CULTIVOS_CANONICOS:
                if c_candidato in consulta_texto.lower():
                    cultivo = c_candidato
                    break

        # Caso 1: Sin contexto recuperado
        if not contexto:
            mensaje_sin_contexto = (
                f"No se encontró un registro oficial en el Vademécum COFEPRIS / OMRI para el cultivo "
                f"de '{cultivo}' con los parámetros indicados. Se prohíbe el uso de productos no autorizados "
                "para este cultivo específico (infracción por uso fuera de etiqueta / off-label)."
                if cultivo
                else (
                    "No se encontró un registro oficial en el Vademécum COFEPRIS / OMRI para los parámetros indicados. "
                    "Se recomienda acudir con un ingeniero agrónomo certificado antes de aplicar insumos no verificados."
                )
            )
            return RecomendacionTratamiento(
                producto_comercial="No localizado",
                ingrediente_activo="Sin coincidencia oficial",
                registro_sanitario_cofepris="No disponible",
                dosis_autorizada=None,
                intervalo_seguridad_dias=None,
                aprobacion_organica_omri=None,
                compatible_exportacion_usda=None,
                recomendacion_agronomica=mensaje_sin_contexto,
                fragmento_oficial_citado="Sin evidencia documental autorizada para este cultivo.",
                fuente_documental="Vademécum Oficial PhytoRAG-Tropical",
            )

        # Caso 2: Filtrado Estricto por Cultivo (Blindaje contra vulnerabilidad Off-label)
        candidatos = contexto
        if cultivo:
            cultivo_solic_norm = normalizar_cultivo(cultivo)
            candidatos_cultivo = [
                c
                for c in contexto
                if (
                    cultivo_solic_norm
                    == normalizar_cultivo(str(c.metadatos.get("cultivo", "")))
                    or cultivo_solic_norm
                    in normalizar_cultivo(str(c.metadatos.get("cultivo", "")))
                )
            ]
            if not candidatos_cultivo:
                return RecomendacionTratamiento(
                    producto_comercial="No autorizado para este cultivo",
                    ingrediente_activo="Sin registro oficial para el cultivo",
                    registro_sanitario_cofepris="N/A",
                    dosis_autorizada=None,
                    intervalo_seguridad_dias=None,
                    aprobacion_organica_omri=None,
                    compatible_exportacion_usda=None,
                    recomendacion_agronomica=(
                        f"RECHAZO REGULATORIO (OFF-LABEL): No existe ningún producto autorizado en el catálogo oficial "
                        f"para el cultivo de {cultivo} bajo los criterios consultados. En la legislación mexicana (COFEPRIS), "
                        "está estrictamente prohibido aplicar productos registrados para otros cultivos."
                    ),
                    fragmento_oficial_citado="Infracción por uso fuera de etiqueta (off-label).",
                    fuente_documental="Catálogo Oficial COFEPRIS / SENASICA",
                )
            candidatos = candidatos_cultivo

        # Caso 3: Validación de Régimen Orgánico OMRI (3 estados: True, False, None/desconocido)
        if regimen == "organico_omri":
            candidatos_organicos = [
                c for c in candidatos if c.metadatos.get("aprobado_omri") is True
            ]
            if candidatos_organicos:
                candidatos = candidatos_organicos
            else:
                # Distinguir entre desconocido y explícitamente no aprobado
                candidatos_desconocidos = [
                    c for c in candidatos if c.metadatos.get("aprobado_omri") is None
                ]
                if candidatos_desconocidos:
                    return RecomendacionTratamiento(
                        producto_comercial="Certificación orgánica no verificada",
                        ingrediente_activo="Sin información de certificación en catálogo oficial",
                        registro_sanitario_cofepris="N/A",
                        dosis_autorizada=None,
                        intervalo_seguridad_dias=None,
                        aprobacion_organica_omri=None,
                        compatible_exportacion_usda=None,
                        recomendacion_agronomica=(
                            f"INFORMACIÓN NO VERIFICADA: Los registros oficiales recuperados para {cultivo or 'este cultivo'} "
                            "no cuentan con información confirmada sobre certificación orgánica (OMRI/LPO). Se recomienda "
                            "consultar a un organismo de certificación orgánica o a un profesional agronómico antes de aplicar cualquier insumo."
                        ),
                        fragmento_oficial_citado="Sin información verificada de certificación orgánica.",
                        fuente_documental="Vademécum Oficial OMRI / LPO México",
                    )
                else:
                    return RecomendacionTratamiento(
                        producto_comercial="No autorizado para régimen orgánico",
                        ingrediente_activo="Sin bioinsumo orgánico certificado en catálogo",
                        registro_sanitario_cofepris="N/A",
                        dosis_autorizada=None,
                        intervalo_seguridad_dias=None,
                        aprobacion_organica_omri=False,
                        compatible_exportacion_usda=None,
                        recomendacion_agronomica=(
                            "RECHAZO REGULATORIO: La consulta solicita tratamiento en régimen orgánico (OMRI/LPO), "
                            f"pero los insumos oficiales autorizados para {cultivo or 'este cultivo'} son de síntesis química "
                            "convencional y tienen prohibida su aplicación en huertas orgánicas."
                        ),
                        fragmento_oficial_citado="Sin registro orgánico OMRI aplicable para el cultivo.",
                        fuente_documental="Vademécum Oficial OMRI / LPO México",
                    )

        # Caso 4: Validación de Régimen Exportación USDA (3 estados: True, False, None/desconocido)
        elif regimen == "exportacion_usda":
            candidatos_usda = [
                c
                for c in candidatos
                if c.metadatos.get("compatible_exportacion_usda") is True
            ]
            if candidatos_usda:
                candidatos = candidatos_usda
            else:
                candidatos_desconocidos = [
                    c
                    for c in candidatos
                    if c.metadatos.get("compatible_exportacion_usda") is None
                ]
                if candidatos_desconocidos:
                    return RecomendacionTratamiento(
                        producto_comercial="Compatibilidad de exportación no verificada",
                        ingrediente_activo="Sin información de LMR/EPA en catálogo oficial",
                        registro_sanitario_cofepris="N/A",
                        dosis_autorizada=None,
                        intervalo_seguridad_dias=None,
                        aprobacion_organica_omri=None,
                        compatible_exportacion_usda=None,
                        recomendacion_agronomica=(
                            f"INFORMACIÓN NO VERIFICADA: No se dispone de datos verificados sobre tolerancias de Límites Máximos "
                            f"de Residuos (LMR) por EPA/USDA para los insumos de {cultivo or 'este cultivo'}. Se recomienda "
                            "consultar con el departamento técnico de exportación o la regulación de la EPA antes de aplicar el producto."
                        ),
                        fragmento_oficial_citado="Sin información verificada de tolerancias EPA/USDA.",
                        fuente_documental="Límites Máximos de Residuos USDA / EPA",
                    )
                else:
                    return RecomendacionTratamiento(
                        producto_comercial="No apto para exportación USDA",
                        ingrediente_activo="Riesgo de residuo o LMR no compatible",
                        registro_sanitario_cofepris="N/A",
                        dosis_autorizada=None,
                        intervalo_seguridad_dias=None,
                        aprobacion_organica_omri=None,
                        compatible_exportacion_usda=False,
                        recomendacion_agronomica=(
                            f"RECHAZO POR NORMATIVA DE EXPORTACIÓN: Los insumos recuperados para {cultivo or 'este cultivo'} "
                            "no cuentan con tolerancia aprobada de Límites Máximos de Residuos (LMR) por EPA/USDA para exportación "
                            "hacia EE.UU. Su aplicación provocaría el rechazo del embarque en aduanas."
                        ),
                        fragmento_oficial_citado="Incompatible con tolerancias de exportación USDA/EPA.",
                        fuente_documental="Límites Máximos de Residuos USDA / EPA",
                    )

        mejor_candidato = candidatos[0]
        meta = mejor_candidato.metadatos
        raw_is = meta.get("intervalo_seguridad_dias")
        intervalo_seguridad = int(raw_is) if raw_is is not None else None

        # Base canónica determinista sellada desde la ficha oficial
        dictamen_base = {
            "producto_comercial": str(meta.get("producto_comercial") or ""),
            "ingrediente_activo": str(meta.get("ingrediente_activo") or ""),
            "registro_sanitario_cofepris": str(
                meta.get("registro_sanitario_cofepris") or ""
            ),
            "dosis_autorizada": (
                str(meta.get("dosis_autorizada"))
                if meta.get("dosis_autorizada") is not None
                else None
            ),
            "intervalo_seguridad_dias": intervalo_seguridad,
            "aprobacion_organica_omri": meta.get("aprobado_omri"),
            "compatible_exportacion_usda": meta.get("compatible_exportacion_usda"),
            "fragmento_oficial_citado": str(meta.get("fragmento_oficial_citado") or ""),
            "fuente_documental": str(
                meta.get("fuente_documental") or "COFEPRIS / OMRI"
            ),
            "recomendacion_agronomica": str(
                meta.get("recomendacion_agronomica")
                or "Consultar indicaciones de la etiqueta oficial."
            ),
        }

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key.startswith("AIzaSyTuClaveAqui"):
            return RecomendacionTratamiento(**dictamen_base)

        try:
            from google import genai

            client = genai.Client(api_key=api_key)

            # Pasar a Gemini EXCLUSIVAMENTE el contexto del candidato elegido (no todos)
            contexto_candidato = (
                f"[Documento ID: {mejor_candidato.id_documento}]\n"
                f"{mejor_candidato.texto}"
            )

            prompt_sistema = (
                "Eres el Consultor Agronómico PhytoRAG-Tropical, especializado en vademécum de México.\n"
                "INSTRUCCIONES OBLIGATORIAS:\n"
                "1. Genera una recomendación agronómica breve y profesional en español para el agricultor, "
                "enfocándote en el momento oportuno de aplicación y precauciones según el siguiente contexto oficial.\n"
                "2. PROHIBICIÓN ESTRICTA DE CIFRAS: NO incluyas números, cantidades, dosis numéricas ni días de intervalo "
                "de seguridad en tu narrativa; todos esos datos ya están tabulados en la ficha oficial.\n\n"
                f"CONTEXTO OFICIAL DEL INSUMO ELEGIDO:\n{contexto_candidato}\n\n"
                f"CONSULTA: {consulta_texto} (Régimen: {regimen})\n"
                "RESPONDE ÚNICAMENTE EL PÁRRAFO DE LA RECOMENDACIÓN AGRONÓMICA:"
            )

            modelo_gemini = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
            respuesta = client.models.generate_content(
                model=modelo_gemini,
                contents=prompt_sistema,
            )

            narrativa = respuesta.text.strip() if hasattr(respuesta, "text") else ""

            # Validar que la narrativa no contenga cifras/números (prevención de alucinaciones)
            if re.search(r"\d", narrativa):
                print(
                    "[Guardrail] Narrativa del LLM contenía cifras numéricas no permitidas. "
                    "Se descarta y se aplica recomendación determinista de la ficha."
                )
            elif narrativa:
                dictamen_base["recomendacion_agronomica"] = narrativa

            return RecomendacionTratamiento(**dictamen_base)

        except Exception as e:  # noqa: BLE001
            print(
                f"[AVISO] Error o aviso con LLM ({e}). Aplicando dictamen determinista oficial."
            )
            return RecomendacionTratamiento(**dictamen_base)


if __name__ == "__main__":
    print("[Alumno 2] Inicializando Motor PhytoRAG...")
    motor = MotorPhytoRAG()
    print(
        f"[OK] Motor PhytoRAG inicializado correctamente con {len(motor.documentos)} documentos."
    )

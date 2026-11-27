"""Pruebas unitarias para el Motor RAG Híbrido (PhytoRAG-Tropical).

Verifica los puntos requeridos por la auditoría técnica de Milestone 1 y revisión del 23-nov:
- Normalización y alineación de cultivos con Alumno 1 (Limonero, Mango, Papayo).
- Carga exclusiva de corpus_motor_rag.json (omisión de archivos de cuarentena).
- Comportamiento seguro ante corpus vacío o ausente.
- Sin cultivo reconocido o soportado, el motor no recomienda ni elige ficha (ej. aguacate).
- Comparación sin acentos ni diacríticos en BM25 y filtro de alineación patológica (psilido == psílido).
- Mensajes de rechazo referencian estrictamente el corpus verificado de PhytoRAG y no catálogos externos.
- Tolerancia a valores nulos (intervalo de seguridad, dosis, certificaciones).
- Manejo de 3 estados en regímenes orgánico y exportación (True, False, None/desconocido).
- Salida estructurada tipada con Pydantic (RecomendacionTratamiento).
- Guardrail contra cifras numéricas y números en letra en la narrativa del LLM.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# Garantizar que la raíz del proyecto esté en sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rag_engine import (
    MotorPhytoRAG,
    RecomendacionTratamiento,
    normalizar_cultivo,
)

FIXTURES_PATH = Path(__file__).resolve().parent / "fixtures" / "fichas_prueba.json"


class TestMotorPhytoRAG(unittest.TestCase):
    """Suite de pruebas unitarias para MotorPhytoRAG."""

    def setUp(self):
        # Desactivar llamadas externas reales de LLM por defecto en pruebas
        self._orig_api_key = os.environ.get("GEMINI_API_KEY")
        os.environ["GEMINI_API_KEY"] = "AIzaSyTuClaveAquiPrueba"

    def tearDown(self):
        if self._orig_api_key is not None:
            os.environ["GEMINI_API_KEY"] = self._orig_api_key
        else:
            os.environ.pop("GEMINI_API_KEY", None)

    def test_normalizar_cultivo(self):
        """Valida la homologación de nombres de cultivo entre Alumno 1 y Alumno 2."""
        self.assertEqual(normalizar_cultivo("limon"), "limonero")
        self.assertEqual(normalizar_cultivo("limón"), "limonero")
        self.assertEqual(normalizar_cultivo("Limonero"), "limonero")
        self.assertEqual(normalizar_cultivo("cítricos"), "limonero")
        self.assertEqual(normalizar_cultivo("Mango"), "mango")
        self.assertEqual(normalizar_cultivo("papaya"), "papayo")
        self.assertEqual(normalizar_cultivo("Papayo"), "papayo")
        self.assertEqual(normalizar_cultivo(None), "")

    def test_corpus_vacio(self):
        """Valida que el motor arranque en limpio y sin fallar ante un corpus ausente o vacío."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            db_dir = tmp_path / "chroma_empty"
            archivo_inexistente = tmp_path / "corpus_motor_rag.json"

            motor = MotorPhytoRAG(
                vector_db_path=db_dir, corpus_path=archivo_inexistente
            )
            self.assertEqual(len(motor.documentos), 0)

            docs = motor.recuperar_documentos("Trips en mango", cultivo="mango")
            self.assertEqual(docs, [])

            resultado = motor.generar_recomendacion(
                "Trips en mango", docs, cultivo="mango"
            )
            self.assertIsInstance(resultado, RecomendacionTratamiento)
            self.assertEqual(resultado.producto_comercial, "No localizado")
            self.assertIn(
                "El corpus verificado de PhytoRAG no contiene registros",
                resultado.recomendacion_agronomica,
            )
            self.assertEqual(
                resultado.fuente_documental, "Corpus Verificado PhytoRAG-Tropical"
            )

    def test_sin_cultivo_reconocido_no_recomienda(self):
        """Valida que sin cultivo reconocido o soportado (ej. aguacate), el motor no recomiende ninguna ficha."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_no_crop",
                corpus_path=FIXTURES_PATH,
            )

            # 1. Recuperar sin cultivo reconocido devuelve lista vacía
            docs = motor.recuperar_documentos("antracnosis en aguacate")
            self.assertEqual(docs, [])

            # 2. Generación sin cultivo reconocido retorna abstención segura sin elegir producto
            resultado = motor.generar_recomendacion("antracnosis en aguacate", docs)
            self.assertEqual(resultado.producto_comercial, "No localizado")
            self.assertIn(
                "No se identificó un cultivo válido o soportado",
                resultado.recomendacion_agronomica,
            )
            self.assertNotIn("Mango", resultado.recomendacion_agronomica)
            self.assertEqual(
                resultado.fuente_documental, "Corpus Verificado PhytoRAG-Tropical"
            )

    def test_comparacion_sin_acentos_diacriticos(self):
        """Valida que la recuperación funcione idéntica con o sin acentos (psílido == psilido)."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_accents",
                corpus_path=FIXTURES_PATH,
            )

            # Consulta con acentos
            docs_con_acento = motor.recuperar_documentos("psílido en limón")
            # Consulta sin acentos
            docs_sin_acento = motor.recuperar_documentos("psilido en limon")

            self.assertGreaterEqual(len(docs_con_acento), 1)
            self.assertGreaterEqual(len(docs_sin_acento), 1)
            self.assertEqual(
                docs_con_acento[0].id_documento,
                docs_sin_acento[0].id_documento,
            )
            self.assertEqual(docs_con_acento[0].id_documento, "PRUEBA-007")

    def test_archivos_cuarentena_no_se_indexan(self):
        """Verifica que el motor lea únicamente corpus_motor_rag.json e ignore archivos de cuarentena."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            corpus_file = tmp_path / "corpus_motor_rag.json"
            cuarentena_file_1 = tmp_path / "chunks_candidatos_revision.json"
            cuarentena_file_2 = tmp_path / "registros_pendientes_revision.json"

            corpus_file.write_text(
                """[
                {
                    "id": "APROBADO-01",
                    "producto_comercial": "Insumo Aprobado",
                    "ingrediente_activo": "Activo A",
                    "registro_sanitario_cofepris": "RSCO-PRUEBA-999",
                    "cultivo": "Limonero",
                    "problema_fitosanitario": "Cancro",
                    "dosis_autorizada": "1 kg/ha",
                    "intervalo_seguridad_dias": 0,
                    "aprobado_omri": true,
                    "compatible_exportacion_usda": true
                }
            ]""",
                encoding="utf-8",
            )

            cuarentena_file_1.write_text(
                '[{"id": "CUARENTENA-01", "producto_comercial": "Insumo No Revisado"}]',
                encoding="utf-8",
            )
            cuarentena_file_2.write_text(
                '[{"id": "PENDIENTE-01", "producto_comercial": "Insumo Pendiente"}]',
                encoding="utf-8",
            )

            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_quarantine",
                corpus_path=corpus_file,
            )

            self.assertEqual(len(motor.documentos), 1)
            self.assertEqual(motor.documentos[0]["id"], "APROBADO-01")

    def test_filtro_cultivo_anti_offlabel(self):
        """Verifica que el motor no mezcle productos de un cultivo en otro (anti off-label)."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_test",
                corpus_path=FIXTURES_PATH,
            )

            # Búsqueda válida para Limonero
            docs_limon = motor.recuperar_documentos(
                "Cancro bacteriano en huerta", cultivo="Limonero"
            )
            self.assertGreaterEqual(len(docs_limon), 1)
            self.assertTrue(
                all(
                    normalizar_cultivo(d.metadatos.get("cultivo")) == "limonero"
                    for d in docs_limon
                )
            )

            # Búsqueda para Mango: la plaga 'Cancro bacteriano' solo está en limón en el fixture
            docs_mango = motor.recuperar_documentos(
                "Cancro bacteriano en mango", cultivo="mango"
            )
            self.assertEqual(docs_mango, [])

            # Generación para cultivo no coincidente retorna rechazo off-label
            resultado = motor.generar_recomendacion(
                "Cancro en mango", docs_limon, cultivo="mango"
            )
            self.assertEqual(
                resultado.producto_comercial,
                "No autorizado para este cultivo en corpus",
            )
            self.assertIn(
                "RECHAZO REGULATORIO (OFF-LABEL)",
                resultado.recomendacion_agronomica,
            )
            self.assertIn(
                "El corpus verificado de PhytoRAG no contiene",
                resultado.recomendacion_agronomica,
            )
            self.assertEqual(
                resultado.fuente_documental, "Corpus Verificado PhytoRAG-Tropical"
            )

    def test_alineacion_nombres_cultivo(self):
        """Valida la homologación entre 'papaya' (usuario) y 'Papayo' (catálogo de Ricardo)."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_alias",
                corpus_path=FIXTURES_PATH,
            )

            docs = motor.recuperar_documentos(
                "Gusano barrenador en papaya", cultivo="papaya"
            )
            self.assertGreaterEqual(len(docs), 1)
            self.assertEqual(docs[0].metadatos.get("cultivo"), "Papayo")

    def test_tolerancia_campos_null(self):
        """Verifica que el motor maneje valores nulos en dosis, intervalo y certificaciones sin lanzar TypeError."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_nulls",
                corpus_path=FIXTURES_PATH,
            )

            docs = motor.recuperar_documentos(
                "Minador de la hoja en limonero", cultivo="limonero"
            )
            self.assertGreaterEqual(len(docs), 1)

            resultado = motor.generar_recomendacion(
                "Minador de la hoja en limonero", docs, cultivo="limonero"
            )
            self.assertIsInstance(resultado, RecomendacionTratamiento)
            self.assertIsNone(resultado.dosis_autorizada)
            self.assertIsNone(resultado.intervalo_seguridad_dias)
            self.assertIsNone(resultado.aprobacion_organica_omri)
            self.assertIsNone(resultado.compatible_exportacion_usda)

    def test_regimen_organico_y_exportacion_desconocido(self):
        """Verifica que 'desconocido' (None) NO se interprete como rechazo regulatorio ('No')."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_unknown",
                corpus_path=FIXTURES_PATH,
            )

            docs = motor.recuperar_documentos(
                "Minador de la hoja en limonero", cultivo="limonero"
            )

            # 1. Régimen orgánico con valor desconocido
            res_org = motor.generar_recomendacion(
                "Minador de la hoja",
                docs,
                regimen="organico_omri",
                cultivo="limonero",
            )
            self.assertEqual(
                res_org.producto_comercial,
                "Certificación orgánica no verificada",
            )
            self.assertIsNone(res_org.aprobacion_organica_omri)
            self.assertIn("INFORMACIÓN NO VERIFICADA", res_org.recomendacion_agronomica)
            self.assertIn(
                "El corpus verificado de PhytoRAG", res_org.recomendacion_agronomica
            )
            self.assertEqual(
                res_org.fuente_documental, "Corpus Verificado PhytoRAG-Tropical"
            )

            # 2. Régimen exportación USDA con valor desconocido
            res_usda = motor.generar_recomendacion(
                "Minador de la hoja",
                docs,
                regimen="exportacion_usda",
                cultivo="limonero",
            )
            self.assertEqual(
                res_usda.producto_comercial,
                "Compatibilidad de exportación no verificada",
            )
            self.assertIsNone(res_usda.compatible_exportacion_usda)
            self.assertIn(
                "INFORMACIÓN NO VERIFICADA", res_usda.recomendacion_agronomica
            )
            self.assertIn(
                "El corpus verificado de PhytoRAG", res_usda.recomendacion_agronomica
            )
            self.assertEqual(
                res_usda.fuente_documental, "Corpus Verificado PhytoRAG-Tropical"
            )

    def test_regimen_rechazo_explicito(self):
        """Verifica que cuando un producto tiene explícitamente False en OMRI o USDA, se emita el rechazo formal."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_rejection",
                corpus_path=FIXTURES_PATH,
            )

            docs = motor.recuperar_documentos("Trips en mango", cultivo="mango")
            self.assertGreaterEqual(len(docs), 1)

            # Rechazo orgánico explícito
            res_org = motor.generar_recomendacion(
                "Trips en mango", docs, regimen="organico_omri", cultivo="mango"
            )
            self.assertEqual(
                res_org.producto_comercial,
                "No autorizado para régimen orgánico",
            )
            self.assertFalse(res_org.aprobacion_organica_omri)
            self.assertIn("RECHAZO REGULATORIO", res_org.recomendacion_agronomica)
            self.assertIn(
                "corpus verificado de PhytoRAG", res_org.recomendacion_agronomica
            )
            self.assertEqual(
                res_org.fuente_documental, "Corpus Verificado PhytoRAG-Tropical"
            )

            # Rechazo exportación USDA explícito
            res_usda = motor.generar_recomendacion(
                "Trips en mango", docs, regimen="exportacion_usda", cultivo="mango"
            )
            self.assertEqual(
                res_usda.producto_comercial, "No apto para exportación USDA"
            )
            self.assertFalse(res_usda.compatible_exportacion_usda)
            self.assertIn(
                "RECHAZO POR NORMATIVA DE EXPORTACIÓN",
                res_usda.recomendacion_agronomica,
            )
            self.assertIn(
                "corpus verificado de PhytoRAG", res_usda.recomendacion_agronomica
            )
            self.assertEqual(
                res_usda.fuente_documental, "Corpus Verificado PhytoRAG-Tropical"
            )

    def test_guardrail_narrativa_prohibe_cifras(self):
        """Verifica que si el LLM incluye cifras o dosis en su narrativa (numérica o con letra), el guardrail la descarte."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            tmp_path = Path(tmp_dir)
            motor = MotorPhytoRAG(
                vector_db_path=tmp_path / "chroma_llm",
                corpus_path=FIXTURES_PATH,
            )
            docs = motor.recuperar_documentos("Cenicilla en mango", cultivo="mango")

            # Caso A: Cifras numéricas
            mock_response_num = MagicMock()
            mock_response_num.text = (
                "Recomiendo aplicar 4.5 kg/ha de este producto cada 10 días."
            )
            mock_client_num = MagicMock()
            mock_client_num.models.generate_content.return_value = mock_response_num
            mock_genai_mod = MagicMock()
            mock_genai_mod.Client.return_value = mock_client_num

            with (
                unittest.mock.patch.dict(
                    "os.environ", {"GEMINI_API_KEY": "AIzaSyPruebaValida123456789"}
                ),
                unittest.mock.patch.dict(
                    "sys.modules", {"google.genai": mock_genai_mod}
                ),
            ):
                res_num = motor.generar_recomendacion(
                    "Cenicilla en mango", docs, cultivo="mango"
                )

            self.assertNotIn("4.5 kg/ha", res_num.recomendacion_agronomica)
            self.assertEqual(
                res_num.recomendacion_agronomica,
                docs[0].metadatos["recomendacion_agronomica"],
            )

            # Caso B: Cifras en letra
            mock_response_letra = MagicMock()
            mock_response_letra.text = (
                "Recomiendo aplicar dos litros por hectárea cada quince días."
            )
            mock_client_num.models.generate_content.return_value = mock_response_letra

            with (
                unittest.mock.patch.dict(
                    "os.environ", {"GEMINI_API_KEY": "AIzaSyPruebaValida123456789"}
                ),
                unittest.mock.patch.dict(
                    "sys.modules", {"google.genai": mock_genai_mod}
                ),
            ):
                res_letra = motor.generar_recomendacion(
                    "Cenicilla en mango", docs, cultivo="mango"
                )

            self.assertNotIn("dos litros", res_letra.recomendacion_agronomica)
            self.assertEqual(
                res_letra.recomendacion_agronomica,
                docs[0].metadatos["recomendacion_agronomica"],
            )


if __name__ == "__main__":
    unittest.main()

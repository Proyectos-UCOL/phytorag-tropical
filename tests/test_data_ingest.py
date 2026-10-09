"""Pruebas de trazabilidad, fail-closed y separación de chunks para Issue #1."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import src.data_ingest as ingest
from src.data_ingest import (
    CAMPOS_REVISION_MANUAL_EXALT,
    COFEPRIS_EXALT_EVIDENCE,
    EXALT_COMBINACIONES,
    EXALT_LABEL,
    clasificar_y_exportar,
    construir_texto_exalt,
    crear_fichas_exalt_validadas,
    validar_revision_manual_exalt,
)


def documento_exalt_minimo() -> dict:
    """Construye evidencia de fixture delimitada por la estructura del PDF."""
    pagina_1 = (
        "Ilustración para Consulta. Este documento tiene fines ilustrativos. "
        "Registro RSCO-INAC-0103X-301-064-006. "
        "CORTEVA MX, S. A. DE C.V."
    )
    pagina_2 = (
        "Equipo de protección personal. "
        "NO LO APLIQUE CUANDO EL CULTIVO ESTÁ EN FLOR. "
        "NO ABEJAS LIBANDO."
    )
    pagina_3 = (
        "CULTIVO PLAGA DOSIS mL/ha RECOMENDACIONES\n"
        "Limonero, Lima, Naranjo (1) Psílido Diaphorina citri "
        "400 - 600 Realizar una aplicación al follaje.\n"
        "Minador de la hoja 200 - 400 otra recomendación.\n"
        "Periodo de reentrada a las áreas tratadas: 4 horas. "
        "(IS) Intervalo de Seguridad: Días entre aplicación y cosecha. "
        "(SL) Sin Límite.\n"
        "MÉTODOS PARA PREPARAR Y APLICAR EL PRODUCTO.\n"
        "Use protección personal. Agite la mezcla y asegure cobertura.\n"
        "En aplicaciones terrestres en solanáceas se recomienda otra dosis.\n"
        "CONTRAINDICACIONES. No aplique con viento.\n"
        "INCOMPATIBILIDAD. No se recomienda mezclar Exalt en mezclas de tanque.\n"
        "FITOTOXICIDAD. No es fitotóxico según la etiqueta.\n"
        "MANEJO DE RESISTENCIA. Rote modos de acción. "
        "Exalt® no debe alternarse o ser mezclado con cualquier insecticida "
        "al que ya se haya desarrollado resistencia.\n"
    )
    pagina_5 = (
        "Mango \n(1)\nTrips de las flores\nFrankliniella occidentalis\n"
        "400-600 Realizar 2 aplicaciones foliares a las inflorescencias; "
        "volumen 600 L de agua/ha.\n"
        "Papayo \n(1)\nGusano soldado\nSpodoptera exigua\n"
        "200 - 300 Realizar una aplicación foliar; "
        "volumen de aplicación sugerido 450-550 L de agua/ha.\n"
        "Sorgo (21) Gusano cogollero Spodoptera frugiperda 75-100.\n"
        "CULTIVO PLAGA DOSIS mL/ha RECOMENDACIONES\n"
    )
    return {
        "paginas": [
            {"pagina": 1, "texto": pagina_1},
            {"pagina": 2, "texto": pagina_2},
            {"pagina": 3, "texto": pagina_3},
            {"pagina": 5, "texto": pagina_5},
        ]
    }


class RevisionManualExaltTests(unittest.TestCase):
    def registro_valido(self, hashes: dict[str, str | None]) -> dict:
        return {
            "revisor": "Revisor de prueba",
            "fecha_revision": "2026-10-08",
            "aprobada": True,
            "hashes_fuentes": hashes,
            "combinaciones_verificadas": [
                combinacion["id"] for combinacion in EXALT_COMBINACIONES
            ],
            "campos_verificados": sorted(CAMPOS_REVISION_MANUAL_EXALT),
        }

    def test_hashes_de_fuente_modificados_o_ausentes_rechazan_revision(self) -> None:
        hashes = {
            EXALT_LABEL: "a" * 64,
            COFEPRIS_EXALT_EVIDENCE: "b" * 64,
        }
        revision = self.registro_valido(hashes)

        self.assertEqual(validar_revision_manual_exalt(revision, hashes)[0], True)
        hashes_modificados = {**hashes, EXALT_LABEL: "c" * 64}
        self.assertFalse(validar_revision_manual_exalt(revision, hashes_modificados)[0])
        hashes_ausentes = {**hashes, COFEPRIS_EXALT_EVIDENCE: None}
        self.assertFalse(validar_revision_manual_exalt(revision, hashes_ausentes)[0])

    def test_sin_atestacion_no_hay_aprobacion(self) -> None:
        hashes = {
            EXALT_LABEL: "a" * 64,
            COFEPRIS_EXALT_EVIDENCE: "b" * 64,
        }
        aprobada, motivos = validar_revision_manual_exalt(None, hashes)

        self.assertFalse(aprobada)
        self.assertTrue(any("No existe" in motivo for motivo in motivos))

    def test_chunks_contienen_solo_la_combinacion_objetivo_y_restricciones(
        self,
    ) -> None:
        documento = documento_exalt_minimo()
        chunks = {
            combinacion["cultivo"]: construir_texto_exalt(documento, combinacion)
            for combinacion in EXALT_COMBINACIONES
        }

        limonero = chunks["Limonero"]
        self.assertIn("Diaphorina citri", limonero)
        self.assertIn("400 - 600", limonero)
        self.assertNotIn("Minador de la hoja", limonero)

        mango = chunks["Mango"]
        self.assertIn("Frankliniella occidentalis", mango)
        self.assertIn("400-600", mango)
        self.assertNotIn("Diaphorina citri", mango)
        self.assertNotIn("Spodoptera exigua", mango)

        papayo = chunks["Papayo"]
        self.assertIn("Spodoptera exigua", papayo)
        self.assertIn("200 - 300", papayo)
        self.assertNotIn("Frankliniella occidentalis", papayo)
        self.assertNotIn("Sorgo", papayo)
        self.assertNotIn("Spodoptera frugiperda", papayo)

        for texto in chunks.values():
            self.assertIn("mL/ha", texto)
            self.assertIn("4 horas", texto)
            self.assertIn("Intervalo de Seguridad", texto)
            self.assertIn("protección personal", texto)
            self.assertIn("ABEJAS", texto)
            self.assertIn("INCOMPATIBILIDAD", texto)
            self.assertNotIn("FICHA TÉCNICA OFICIAL VALIDADA [COFEPRIS]", texto)

    def assert_aprobacion_retirada(self, cambiar_etiqueta: bool) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            raw = raiz / "raw"
            raw.mkdir()
            etiqueta = raw / EXALT_LABEL
            captura = raw / COFEPRIS_EXALT_EVIDENCE
            etiqueta.write_bytes(b"etiqueta revisada")
            captura.write_bytes(b"captura revisada")
            hashes = {
                EXALT_LABEL: hashlib.sha256(etiqueta.read_bytes()).hexdigest(),
                COFEPRIS_EXALT_EVIDENCE: hashlib.sha256(
                    captura.read_bytes()
                ).hexdigest(),
            }
            revision = self.registro_valido(hashes)
            ruta_revision = raw / "revision_manual_exalt.json"
            ruta_revision.write_text(json.dumps(revision), encoding="utf-8")
            ruta_documentos = raiz / "documentos.json"
            ruta_documentos.write_text(
                json.dumps(
                    [
                        {
                            "archivo": EXALT_LABEL,
                            "documento_o_url": "fuente/Exalt.pdf",
                            "paginas": documento_exalt_minimo()["paginas"],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            with (
                patch.object(ingest, "DATA_RAW", raw),
                patch.object(ingest, "REVISION_MANUAL_EXALT", ruta_revision),
            ):
                fichas = crear_fichas_exalt_validadas(ruta_documentos)
                self.assertEqual(len(fichas), 3)
                self.assertTrue(
                    all(ficha.revision_documental_aprobada for ficha in fichas)
                )
                if cambiar_etiqueta:
                    etiqueta.write_bytes(b"etiqueta modificada")
                else:
                    captura.unlink()

                resultado = clasificar_y_exportar(fichas, raiz / "processed")
                aprobadas = json.loads(
                    resultado["ruta_chunks"].read_text(encoding="utf-8")
                )
                pendientes = json.loads(
                    resultado["ruta_pendientes"].read_text(encoding="utf-8")
                )
                self.assertEqual(aprobadas, [])
                self.assertEqual(len(pendientes), 3)

    def test_fuente_modificada_retiro_aprobacion(self) -> None:
        self.assert_aprobacion_retirada(cambiar_etiqueta=True)

    def test_fuente_ausente_retiro_aprobacion(self) -> None:
        self.assert_aprobacion_retirada(cambiar_etiqueta=False)


if __name__ == "__main__":
    unittest.main()

"""Pruebas de evidencia documental asistida y chunks separados para Issue #1."""

import unittest

from src.data_ingest import (
    COFEPRIS_EXALT_EVIDENCE,
    EXALT_COMBINACIONES,
    EXALT_LABEL,
    EXALT_REVIEWED_SOURCE_HASHES,
    construir_evidencia_campos_exalt,
    construir_texto_exalt,
    puede_aprobar_exalt,
    validar_evidencia_documental_exalt,
)


def documento_exalt_minimo() -> dict:
    """Crea páginas sintéticas para comprobar citas y límites de cada chunk."""
    pagina_1 = (
        'Ilustración para Consulta. " ESTE DOCUMENTO TIENE FINES ILUSTRATIVOS '
        'ÚNICAMENTE. NO ES UNA ETIQUETA REAL." REV. 12/12/2025\n'
        "Spinetoram: (mezcla de Spinosyn J y Spinosyn L) 5.87\n"
        "REGISTRO SANITARIO No.: RSCO-INAC-0103X-301-064-006\n"
        "TITULAR DEL REGISTRO, IMPORTADOR Y DISTRIBUIDOR POR: "
        "CORTEVA MX, S. A. DE C.V.\n"
        "Lago Alberto No. 319, Piso 17, Col. Granada, "
        "Miguel Hidalgo, Ciudad de México, México"
    )
    pagina_2 = (
        "Durante el manejo, preparación de la mezcla, aplicación, "
        "siempre utilice guantes, careta y ropa limpia. "
        "Después de haber usado su ropa protectora contaminada.\n"
        "ESTE PRODUCTO ES ALTAMENTE TÓXICO PARA ABEJAS. NO LO APLIQUE "
        "CUANDO EL CULTIVO O LAS MALEZAS ESTÁN EN FLOR O CUANDO LAS "
        "ABEJAS SE ENCUENTRAN LIBANDO."
    )
    pagina_3 = (
        "CULTIVO PLAGA DOSIS  mL/ha RECOMENDACIONES\n"
        "Maíz  (1 día grano) Gusano cogollero 100\n"
        "(3 días forraje) Spodoptera frugiperda.\n"
        "Periodo de reentrada a las áreas tratadas: 4 horas. "
        "(IS) Intervalo de Seguridad: Días que deben transcurrir entre "
        "la última aplicación y la cosecha. (SL) Sin Límite.\n"
        "MÉTODOS PARA PREPARAR Y APLICAR EL PRODUCTO.\n"
        "Durante la preparación y aplicación del producto, utilice protección.\n"
        "En aplicaciones terrestres en solanáceas se recomienda otra dosis.\n"
        "CONTRAINDICACIONES. No aplique con viento.\n"
        "INCOMPATIBILIDAD. No se recomienda mezclar Exalt® en mezclas de "
        "tanque. Si desea mezclar, la mezcla se hará con productos registrados "
        "en los cultivos recomendados en esta etiqueta, sin embargo es necesario "
        "realizar una prueba de compatibilidad y fitotoxicidad previa a la aplicación.\n"
        "FITOTOXICIDAD. No es fitotóxico según la etiqueta.\n"
        "Exalt® no debe alternarse o ser mezclado con cualquier insecticida "
        "al que ya se haya desarrollado resistencia."
    )
    pagina_4 = (
        "CULTIVO PLAGA DOSIS  mL/ha RECOMENDACIONES\n"
        "Limonero, Lima, Naranjo, Psílido Asiático 400 - 600 "
        "Realizar una aplicación al follaje.\n"
        "Tangerino, Toronjo, de los cítricos ninfas.\n"
        "Cidro, Mandarino (1) Diaphorina citri de los árboles tratados para "
        "asegurar una buena cobertura del follaje.\n"
        "Minador de la hoja 200 - 400 otra recomendación."
    )
    pagina_5 = (
        "CULTIVO PLAGA DOSIS  mL/ha RECOMENDACIONES\n"
        "Mango \n(1)\nTrips de las flores\nFrankliniella occidentalis\n"
        "400-600 Realizar 2 aplicaciones foliares a las inflorescencias; "
        "volumen 600 L de agua/ha.\n"
        "Papayo \n(1)\nGusano soldado\nSpodoptera exigua\n"
        "200 - 300 Realizar una aplicación foliar; "
        "volumen de aplicación sugerido 450-550 L de agua/ha.\n"
        "Sorgo (21) Gusano cogollero Spodoptera frugiperda 75-100.\n"
    )
    return {
        "paginas": [
            {"pagina": 1, "texto": pagina_1},
            {"pagina": 2, "texto": pagina_2},
            {"pagina": 3, "texto": pagina_3},
            {"pagina": 4, "texto": pagina_4},
            {"pagina": 5, "texto": pagina_5},
        ]
    }


class EvidenciaDocumentalExaltTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documento = documento_exalt_minimo()
        self.paginas = {
            pagina["pagina"]: pagina["texto"] for pagina in self.documento["paginas"]
        }
        self.hashes = dict(EXALT_REVIEWED_SOURCE_HASHES)

    def test_chunks_separan_combinaciones_y_conservan_restricciones(self) -> None:
        chunks = {
            combinacion["cultivo"]: construir_texto_exalt(self.documento, combinacion)
            for combinacion in EXALT_COMBINACIONES
        }

        limonero = chunks["Limonero"]
        self.assertIn("--- Tabla de usos; página 4;", limonero)
        self.assertIn("Diaphorina citri", limonero)
        self.assertIn("400 - 600", limonero)
        self.assertIn("Marcador de grupo de cultivos: (1)", limonero)
        self.assertNotIn("Minador de la hoja", limonero)

        mango = chunks["Mango"]
        self.assertIn("Frankliniella occidentalis", mango)
        self.assertNotIn("Diaphorina citri", mango)
        self.assertNotIn("Spodoptera exigua", mango)

        papayo = chunks["Papayo"]
        self.assertIn("Spodoptera exigua", papayo)
        self.assertNotIn("Frankliniella occidentalis", papayo)
        self.assertNotIn("Spodoptera frugiperda", papayo)
        for texto in chunks.values():
            self.assertIn("mL/ha", texto)
            self.assertIn("4 horas", texto)
            self.assertIn("Intervalo de Seguridad", texto)
            self.assertIn("protección", texto.lower())
            self.assertIn("ABEJAS", texto)
            self.assertIn("INCOMPATIBILIDAD", texto)
            self.assertIn("ilustrativo", texto)

    def test_evidencia_por_campo_cita_fuente_pagina_fragmento_y_hash(self) -> None:
        for combinacion in EXALT_COMBINACIONES:
            with self.subTest(cultivo=combinacion["cultivo"]):
                evidencia = construir_evidencia_campos_exalt(
                    self.documento, combinacion, self.hashes
                )
                completa, motivos = validar_evidencia_documental_exalt(
                    evidencia, self.paginas, self.hashes
                )
                self.assertTrue(completa, motivos)
                self.assertEqual(evidencia["dosis"].valor, combinacion["dosis_texto"])
                self.assertEqual(evidencia["dosis"].citas[0].archivo, EXALT_LABEL)
                self.assertIn(
                    f"Página {combinacion['pagina']}",
                    evidencia["dosis"].citas[0].ubicacion,
                )
                self.assertEqual(
                    evidencia["dosis"].citas[0].sha256,
                    self.hashes[EXALT_LABEL],
                )
                self.assertTrue(
                    all(
                        cite.archivo != COFEPRIS_EXALT_EVIDENCE
                        for cite in evidencia["dosis"].citas
                    )
                )
                fragmento_fila = evidencia["cultivo"].citas[0].fragmento
                cultivos_ajenos = {
                    "Limonero": ("Minador de la hoja",),
                    "Mango": ("Papayo", "Spodoptera exigua"),
                    "Papayo": ("Sorgo", "Spodoptera frugiperda"),
                }[combinacion["cultivo"]]
                for dato_ajeno in cultivos_ajenos:
                    self.assertNotIn(dato_ajeno, fragmento_fila)

    def test_valores_desconocidos_se_conservan_sin_inferencia(self) -> None:
        evidencia = construir_evidencia_campos_exalt(
            self.documento, EXALT_COMBINACIONES[0], self.hashes
        )
        for nombre in (
            "fecha_consulta_cofepris",
            "aprobado_omri",
            "compatibilidad_exportacion",
            "nombre_cientifico_cultivo",
        ):
            self.assertIsNone(evidencia[nombre].valor)
            self.assertEqual(evidencia[nombre].estado, "desconocido")
            self.assertTrue(evidencia[nombre].motivo)

    def test_revision_asistida_no_requiere_firma_humana_ni_aprueba_etiqueta(
        self,
    ) -> None:
        evidencia = construir_evidencia_campos_exalt(
            self.documento, EXALT_COMBINACIONES[0], self.hashes
        )
        completa, motivos = validar_evidencia_documental_exalt(
            evidencia, self.paginas, self.hashes
        )
        self.assertTrue(completa, motivos)
        self.assertFalse(puede_aprobar_exalt(evidencia, completa))

    def test_hash_ausente_modificado_o_cita_fabricada_invalida_revision(self) -> None:
        evidencia = construir_evidencia_campos_exalt(
            self.documento, EXALT_COMBINACIONES[0], self.hashes
        )
        evidencia_incompleta = {
            nombre: campo for nombre, campo in evidencia.items() if nombre != "dosis"
        }
        completa, motivos = validar_evidencia_documental_exalt(
            evidencia_incompleta, self.paginas, self.hashes
        )
        self.assertFalse(completa)
        self.assertTrue(any("Faltan campos" in motivo for motivo in motivos))

        hashes_modificados = {**self.hashes, EXALT_LABEL: "0" * 64}
        completa, motivos = validar_evidencia_documental_exalt(
            evidencia, self.paginas, hashes_modificados
        )
        self.assertFalse(completa)
        self.assertTrue(any("cambió" in motivo for motivo in motivos))

        hashes_ausentes = {**self.hashes, COFEPRIS_EXALT_EVIDENCE: None}
        completa, _ = validar_evidencia_documental_exalt(
            evidencia, self.paginas, hashes_ausentes
        )
        self.assertFalse(completa)

        evidencia_falsa = {
            **evidencia,
            "dosis": evidencia["dosis"].model_copy(
                update={
                    "citas": [
                        evidencia["dosis"]
                        .citas[0]
                        .model_copy(update={"fragmento": "Dosis 999 L/ha"})
                    ]
                }
            ),
        }
        completa, motivos = validar_evidencia_documental_exalt(
            evidencia_falsa, self.paginas, self.hashes
        )
        self.assertFalse(completa)
        self.assertTrue(any("no aparece" in motivo for motivo in motivos))


if __name__ == "__main__":
    unittest.main()

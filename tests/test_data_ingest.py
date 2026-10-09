"""Pruebas de evidencia documental asistida y chunks separados para Issue #1."""

import unittest

from src.data_ingest import (
    COFEPRIS_EXALT_EVIDENCE,
    EXALT_COMBINACIONES,
    EXALT_CORTEVA_TECHNICAL_SHEET_SHA256,
    EXALT_LABEL,
    EXALT_REVIEWED_SOURCE_HASHES,
    DosisEspecificacion,
    EvidenciaCampo,
    FichaFitosanitaria,
    TrazabilidadFuente,
    construir_evidencia_campos_exalt,
    construir_informe_busqueda_documental_exalt,
    construir_texto_exalt,
    puede_aprobar_exalt,
    serializar_metadatos_ficha,
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

    def test_metadatos_exportados_incluyen_dosis_y_campos_canonicos(self) -> None:
        ficha = FichaFitosanitaria(
            id_registro="FICH-TEST-001",
            cultivo="Limonero",
            problema_fitosanitario="Diaphorina citri",
            ingrediente_activo="spinetoram",
            registro_cofepris="RSCO-TEST",
            dosis=DosisEspecificacion(
                minima=400,
                maxima=600,
                unidad="mL/ha",
                texto_etiqueta="400 - 600",
            ),
            aprobado_omri=None,
            trazabilidad=TrazabilidadFuente(
                documento_o_url="etiqueta.pdf",
                ubicacion_fuente="Página 4",
                sha256="a" * 64,
            ),
            evidencia_documental={
                "marcador_grupo_cultivos": EvidenciaCampo(
                    valor="(1)",
                    estado="respaldado_solo_en_documento_ilustrativo",
                )
            },
        )

        metadatos = serializar_metadatos_ficha(ficha)

        self.assertEqual(metadatos["dosis"]["texto_etiqueta"], "400 - 600")
        self.assertEqual(metadatos["dosis"]["unidad"], "mL/ha")
        self.assertEqual(metadatos["cultivo"], "Limonero")
        self.assertEqual(metadatos["problema_fitosanitario"], "Diaphorina citri")
        self.assertEqual(metadatos["ingrediente_activo"], "spinetoram")
        self.assertEqual(metadatos["registro_cofepris"], "RSCO-TEST")
        self.assertIsNone(metadatos["is_dias"])
        self.assertIsNone(metadatos["aprobado_omri"])

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

    def test_ficha_tecnica_corrobora_datos_sin_aprobar_etiqueta_ni_formulacion(
        self,
    ) -> None:
        paginas = {
            2: (
                "Registro Sanitario: RSCO-INAC-0103X-301-064-006 "
                "Insecticida de origen natural novedoso para el control de plagas. "
                "Ingredientes Activos: Jemvelva® active: Equivalente a 60 g de i.a./L. "
                "Ingredientes Inertes:"
            ),
            4: (
                "Limonero, Lima, Naranjo Tangerino, Toronjo, Cidro, Mandarino (1) "
                "Psílido Asíatico de los cítricos (Diaphorina citri) 400-600 "
                "Realizar una aplicación al follaje cuando se observen la presencia "
                "de ninfas. Utilizar un volumen de agua adecuado en función del "
                "tamaño de los árboles tratados para asegurar una buena cobertura "
                "del follaje. "
                "Mango (1) Trips de las flores (Frankliniella occidentalis) 400-600 "
                "Realizar 2 aplicaciones foliares dirigidas a las inflorescencias "
                "y brotes jóvenes a intervalo de 7 días; volumen sugerido "
                "600 L de agua/ha. "
                "Papayo (1) Gusano soldado Spodoptera exigua 200 - 300 "
                "Realizar una aplicación foliar cuando se detecten las primeras "
                "larvas vivas; volumen de aplicación sugerido 450-550 L de agua/ha."
            ),
            5: (
                "Periodo de reentrada a las áreas tratadas: 4 horas. "
                "Intervalo de seguridad: días que deben transcurrir entre la última "
                "aplicación y la cosecha. (SL) Sin límite."
            ),
        }
        informe = construir_informe_busqueda_documental_exalt(
            paginas,
            EXALT_CORTEVA_TECHNICAL_SHEET_SHA256,
        )

        self.assertEqual(len(informe["fichas"]), 3)
        self.assertFalse(informe["aprobacion_corpus_elegible"])
        self.assertFalse(informe["fuente_fabricante"]["limitaciones"] == [])
        self.assertTrue(
            all(
                not ficha["elegible_para_aprobacion_corpus"]
                for ficha in informe["fichas"]
            )
        )
        for ficha in informe["fichas"]:
            with self.subTest(cultivo=ficha["cultivo"]):
                self.assertTrue(ficha["cultivo_y_plaga"]["citas"])
                self.assertTrue(ficha["dosis"]["citas"])
                self.assertTrue(ficha["intervalo_seguridad"]["citas"])
                self.assertEqual(
                    ficha["formulacion"]["resultado"],
                    "no confirmada en la ficha técnica consultada",
                )
                citas = ficha["dosis"]["citas"]
                self.assertTrue(
                    all(
                        cita["sha256"] == EXALT_CORTEVA_TECHNICAL_SHEET_SHA256
                        and cita["archivo"]
                        == "Exalt_ficha_tecnica_Corteva_Mex_2026.pdf"
                        for cita in citas
                    )
                )

    def test_hash_ficha_tecnica_distinto_invalida_sus_citas(self) -> None:
        informe = construir_informe_busqueda_documental_exalt(
            {4: "datos que no deben usarse"},
            "0" * 64,
        )

        self.assertEqual(
            informe["fuente_fabricante"]["estado_hash"],
            "fuente_ausente_o_modificada_no_verificada",
        )
        self.assertFalse(informe["aprobacion_corpus_elegible"])
        self.assertTrue(all(not ficha["dosis"]["citas"] for ficha in informe["fichas"]))

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

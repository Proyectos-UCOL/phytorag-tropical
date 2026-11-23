# 🌿 PhytoRAG-Tropical: Sistema RAG Especializado en Cumplimiento Fitosanitario, Vademécum Oficial y Mitigación de Alucinaciones en Dosificación Agrícola

### **Director de Proyecto:** Dr. Carlos Flores
**Institución:** Facultad de Telemática — Universidad de Colima  
**Cuerpo Académico:** CA-54 Redes y Telecomunicaciones  
**Tipo de Proyecto:** Investigación Aplicada y Servicio Social Constitucional (480 horas)  
**Equipo:** 2 Estudiantes de Ingeniería Telemática / Software  
**Estado:** `activo`

---

## 🎯 1. Descripción del Proyecto

En la agricultura moderna de exportación y producción agroecológica (como el limón, mango, papaya y frutales tropicales en México), la aplicación de insumos fitosanitarios (plaguicidas, bioinsumos, fertilizantes foliares) está estrictamente regulada por normativas federales e internacionales:
1. **Regulación Federal (México):** Catálogo de Registros Sanitarios de Plaguicidas de **COFEPRIS** y **SENASICA**.
2. **Certificación Orgánica:** Listados oficiales **OMRI (Organic Materials Review Institute)** y **LPO (Ley de Productos Orgánicos de México)**.
3. **Exportación Internacional:** Límites Máximos de Residuos (**LMRs**) de la **EPA / USDA (EE.UU.)** y la **Unión Europea**.

Los modelos de lenguaje generalistas (LLMs comerciales como ChatGPT o Gemini sin RAG) presentan **alucinaciones críticas en dosificación numérica** y **contaminación regulatoria entre países**, recomendando con frecuencia productos cancelados, dosis tóxicas o químicos prohibidos para exportación u orgánicos.

**`PhytoRAG-Tropical`** es un sistema de **Generación Aumentada por Recuperación (RAG Híbrido con Guardrails Deterministas)** que actúa como un **Consultor Agronómico Digital de Máxima Fidelidad**: responde solo con fichas verificadas y los campos regulados (registro, dosis e intervalo de seguridad) salen de la ficha, no del modelo.

---

## 🔬 2. El Experimento Científico (Objetivo del Artículo 1)

**Pregunta:** ¿cuánto reducen la recuperación de fichas verificadas y los candados deterministas los errores de dosis y las recomendaciones fuera de etiqueta de un modelo de lenguaje, en consultas fitosanitarias de limón, mango y papaya?

Se comparan 4 arquitecturas, con el mismo modelo generador, sobre un banco de **100 consultas derivadas de las fichas aprobadas del corpus**:

| Arquitectura | Recuperación | Quién llena registro, dosis e intervalo |
| :--- | :--- | :--- |
| **M1: Baseline LLM** | Ninguna | El modelo, de memoria |
| **M2: RAG Vectorial Simple** | Búsqueda semántica densa (*ChromaDB*) | El modelo, leyendo el contexto recuperado |
| **M3: RAG Híbrido** | Léxica (*BM25*) y semántica, fusionadas con RRF | El modelo, leyendo el contexto recuperado |
| **M4: RAG Híbrido + Guardrails** | Híbrida, con filtro por cultivo y por régimen | La ficha verificada |

### Banco de consultas

| Tipo | Qué prueba | Cuántas |
| :--- | :--- | :-: |
| A. Con respuesta | Registro, dosis e intervalo correctos | 40 |
| B. Cultivo no autorizado | Que no recomiende un producto de otro cultivo | 20 |
| C. Régimen orgánico | Que no recomiende un producto no aprobado | 15 |
| D. Sin respuesta en el corpus | Que se abstenga | 15 |
| E. Premisa falsa | Que no confirme un dato equivocado | 10 |

Cada consulta tiene dos redacciones: una técnica y una como la escribiría un productor.

### Métricas de Evaluación

Se calculan sin otro modelo como juez, con intervalos de confianza por bootstrap y comparación pareada de McNemar:

* **Registro, dosis e intervalo de seguridad correctos** frente a la ficha esperada.
* **Recomendación fuera de etiqueta** y **violación de régimen orgánico.**
* **Abstención correcta** y **abstención indebida.**
* **Recuperación:** la ficha esperada está entre las recuperadas.
* **Costo, tiempo por consulta** y variación entre repeticiones.

La fidelidad con RAGAS queda como complemento opcional.

### Fuera del Artículo 1

El re-ranking, la comparación de modelos de embeddings, el régimen de exportación (LMR de EPA y USDA), la interfaz web y la validación con agrónomos o productores.

---

## 👥 3. Equipo, Roles y Ruta

Plan, fechas y forma de trabajo: **[Issue #9](https://github.com/Proyectos-UCOL/phytorag-tropical/issues/9)**.

| Rol | Estudiante | Responsabilidad Principal | Issues Vigentes |
| :--- | :--- | :--- | :--- |
| **Data, Corpus & Ground Truth Lead** | **Ricardo Mercado López** ([`@ricardo-lop`](https://github.com/ricardo-lop)) | Corpus de fichas con evidencia por campo y aprobación humana; banco de 100 consultas; análisis de errores. | [#7](https://github.com/Proyectos-UCOL/phytorag-tropical/issues/7) · [#3](https://github.com/Proyectos-UCOL/phytorag-tropical/issues/3) |
| **RAG Architecture & Evaluation Lead** | **Sofía Renata Silva Méndez** ([`@SOFIARENASM`](https://github.com/SOFIARENASM)) | Motor RAG en Python (ChromaDB, BM25, API con FastAPI), arquitecturas M1 a M4 por configuración y corredor de evaluación. | [#2](https://github.com/Proyectos-UCOL/phytorag-tropical/issues/2) · [#8](https://github.com/Proyectos-UCOL/phytorag-tropical/issues/8) |

**Criterio de evidencia del corpus:** una ficha se aprueba con la etiqueta publicada por el fabricante, la consulta de COFEPRIS que confirma el registro y la aprobación humana. Detalle en el [Issue #7](https://github.com/Proyectos-UCOL/phytorag-tropical/issues/7).

---

## 📦 4. Los 5 Entregables Mínimos Obligatorios

| # | Entregable | Descripción | Ubicación |
| :-: | :--- | :--- | :--- |
| **E1** | **Pipeline de Software (Código)** | Sistema RAG híbrido modular, documentado y tipado en Python + FastAPI. | [`src/`](src/) |
| **E2** | **Corpus Normativo Estructurado** | Fichas JSON aprobadas, con evidencia y trazabilidad por campo, y su base vectorial. | [`data/`](data/) |
| **E3** | **Benchmark Experimental y Resultados** | Banco de 100 consultas, tablas de métricas con intervalos de confianza y análisis de errores. | [`results/`](results/) |
| **E4** | **Reporte Técnico de Servicio Social** | Documento oficial de acreditación para la Universidad de Colima. | [`deliverables/reporte-tecnico/`](deliverables/reporte-tecnico/) |
| **E5** | **Manuscrito de Artículo Científico** | Manuscrito en formato internacional listo para revista indexada (JCR/Scopus). | [`deliverables/articulo-revista/`](deliverables/articulo-revista/) |

---

## 🗺️ 5. Estructura del Repositorio

```text
phytorag-tropical/
├── README.md                          # Este documento (Visión y arquitectura)
├── requirements.txt                  # Dependencias oficiales fijadas
├── .env.example                      # Plantilla de variables (API Keys)
├── AGENTS.md                         # Instrucciones para agentes de IA (Cursor/ChatGPT)
├── .cursorrules                      # Guardrails de desarrollo
├── CLAUDE.md                         # Contexto y directrices de ingeniería
├── docs/
│   ├── 01-guia-estudiantes.md         # Onboarding paso a paso para los 3 alumnos
│   ├── 02-protocolo-experimental.md   # Metodología científica y métricas RAGAS
│   ├── 03-guia-redaccion-humana.md    # Guía para redacción académica sin clichés IA
│   ├── 04-workflow-y-guardrails.md    # Reglas de Git y anti-colisiones
│   └── 05-sistema-de-diseno-y-tokens.md # Tokens UI Tailwind para la interfaz
├── data/
│   ├── raw/                          # Catálogos COFEPRIS, SENASICA, OMRI originales
│   ├── processed/                    # Documentos limpios y chunked en JSON
│   └── vector_store/                 # Base de datos vectorial ChromaDB
├── src/
│   ├── data_ingest.py                # Script de ingesta, chunking y metadatos
│   ├── rag_engine.py                 # Motor RAG Híbrido (BM25 + Dense + Rerank)
│   ├── eval_benchmark.py             # Framework de evaluación RAGAS y métricas
│   └── app.py                        # Servidor API FastAPI / Consultor
├── results/                          # Reportes estadísticos, tablas y gráficas
└── deliverables/
    ├── reporte-tecnico/               # Documento de Servicio Social UCol
    └── articulo-revista/              # Manuscrito del Paper
```

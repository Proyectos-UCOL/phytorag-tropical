# 🌿 PhytoRAG-Tropical: Sistema RAG Especializado en Cumplimiento Fitosanitario, Vademécum Oficial y Mitigación de Alucinaciones en Dosificación Agrícola

### **Director de Proyecto:** Dr. Carlos Flores
**Institución:** Facultad de Telemática — Universidad de Colima  
**Cuerpo Académico:** CA-54 Redes y Telecomunicaciones  
**Tipo de Proyecto:** Investigación Aplicada y Servicio Social Constitucional (480 horas)  
**Equipo:** 3 Estudiantes de Ingeniería Telemática / Software  
**Estado:** `activo`

---

## 🎯 1. Descripción del Proyecto

En la agricultura moderna de exportación y producción agroecológica (como el limón, mango, papaya y frutales tropicales en México), la aplicación de insumos fitosanitarios (plaguicidas, bioinsumos, fertilizantes foliares) está estrictamente regulada por normativas federales e internacionales:
1. **Regulación Federal (México):** Catálogo de Registros Sanitarios de Plaguicidas de **COFEPRIS** y **SENASICA**.
2. **Certificación Orgánica:** Listados oficiales **OMRI (Organic Materials Review Institute)** y **LPO (Ley de Productos Orgánicos de México)**.
3. **Exportación Internacional:** Límites Máximos de Residuos (**LMRs**) de la **EPA / USDA (EE.UU.)** y la **Unión Europea**.

Los modelos de lenguaje generalistas (LLMs comerciales como ChatGPT o Gemini sin RAG) presentan **alucinaciones críticas en dosificación numérica** y **contaminación regulatoria entre países**, recomendando con frecuencia productos cancelados, dosis tóxicas o químicos prohibidos para exportación u orgánicos.

**`PhytoRAG-Tropical`** es un sistema de **Generación Aumentada por Recuperación (RAG Híbrido con Guardrails Deterministas)** que actúa como un **Consultor Agronómico Digital de Máxima Fidelidad**, garantizando cero alucinaciones y estricto cumplimiento normativo.

---

## 🔬 2. El Experimento Científico (Objetivo del Paper)

El proyecto evalúa empíricamente 4 arquitecturas frente a un banco de evaluación estandarizado de 100+ consultas agronómicas adversarias de control:

| Arquitectura Evaluada | Descripción Técnica |
| :--- | :--- |
| **M1: Baseline LLM** | Modelo de lenguaje directo sin RAG (*Gemini 2.5 Flash / GPT-4o-mini*). |
| **M2: RAG Vectorial Simple** | Búsqueda semántica densa estándar con Embeddings en base vectorial (*ChromaDB*). |
| **M3: RAG Híbrido** | Recuperación combinada: Búsqueda léxica exact-match (*BM25*) + Embeddings densos + *Re-ranking* (*BGE / Cohere*). |
| **M4: RAG Híbrido + Guardrails Estructurados** | RAG Híbrido con filtrado determinista de metadatos (*COFEPRIS / OMRI / USDA*) y esquemas *Pydantic*. |

### Métricas de Evaluación (Framework RAGAS):
* **Fidelidad (*Faithfulness*):** Grado de apego al documento oficial (0% alucinación).
* **Precisión de Dosificación (*Dosage Accuracy %*):** Exactitud numérica en la dosis recomendada ($g/L$, $L/ha$).
* **Tasa de Violación Normativa (*Regulatory Violation Rate %*):** Porcentaje de recomendaciones que violan normativas orgánicas o de exportación.
* **Context Recall & Answer Relevance:** Calidad de la recuperación documental y relevancia de la respuesta.
* **Latencia y Costo Computacional por Consulta.**

---

## 👥 3. Distribución de Roles del Equipo (3 Estudiantes)

Para garantizar total autonomía y cero colisiones de código en Git (1 Ticket = 1 Alumno = 1 Rama):

| Rol | Estudiante | Responsabilidad Principal | Entregable Clave |
| :--- | :---: | :--- | :--- |
| **Data & Corpus Lead** | **Alumno 1** | Ingesta, limpieza, chunking estructurado y metadata tagging del catálogo COFEPRIS, SENASICA, fichas DEAQ y lista OMRI. | `data/processed/`, `src/data_ingest.py` |
| **RAG Architecture Lead** | **Alumno 2** | Implementación del motor RAG en Python (ChromaDB, BM25, embeddings, re-ranking y API con FastAPI). | `src/rag_engine.py`, `src/app.py` |
| **Evaluation & UI Lead** | **Alumno 3** | Benchmark experimental con RAGAS, cálculo de métricas estadísticas, matrices y frontend web con Tailwind CSS. | `src/eval_benchmark.py`, `ui/` |

---

## 📦 4. Los 5 Entregables Mínimos Obligatorios

| # | Entregable | Descripción | Ubicación |
| :-: | :--- | :--- | :--- |
| **E1** | **Pipeline de Software (Código)** | Sistema RAG híbrido modular, documentado y tipado en Python + FastAPI. | [`src/`](src/) |
| **E2** | **Corpus Normativo Estructurado** | Base de datos vectorial y fichas JSON de COFEPRIS, SENASICA y OMRI indexadas. | [`data/`](data/) |
| **E3** | **Benchmark Experimental y Resultados** | Tablas de métricas RAGAS, gráficas de alucinación y tiempos de respuesta. | [`results/`](results/) |
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

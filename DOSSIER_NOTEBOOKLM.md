# 📘 DOSSIER COMPLETO: Proyecto `PhytoRAG-Tropical`
### Sistema RAG Especializado en Cumplimiento Fitosanitario, Vademécum Oficial y Mitigación de Alucinaciones en Dosificación Agrícola

**Director de Proyecto:** Dr. Carlos Flores  
**Institución:** Facultad de Telemática — Universidad de Colima  
**Cuerpo Académico:** CA-54 Redes y Telecomunicaciones  
**Línea de Investigación:** Inteligencia Artificial Aplicada, AgTech & Recuperación Aumentada por Generación (RAG)  
**Revistas Objetivo:** *Computers and Electronics in Agriculture* (JCR Q1), *IEEE Access* (JCR Q2), *Agronomy* (JCR Q1)

---

## 🎯 1. Resumen y Contexto Agronómico

En la agricultura tropical de exportación y producción agroecológica en México (limón mexicano, limón persa, mango y papaya), la aplicación de insumos fitosanitarios está sujeta a una estricta triple regulación:
1. **Regulación Sanitaria Nacional (México):** Registros de plaguicidas autorizados por **COFEPRIS** y **SENASICA**.
2. **Normativa para Agricultura Orgánica:** Catálogos oficiales **OMRI (Organic Materials Review Institute)** y **LPO (Ley de Productos Orgánicos de México)**.
3. **Límites de Exportación Internacional:** Límites Máximos de Residuos (**LMRs**) de la **EPA / USDA (EE.UU.)** y la Unión Europea.

### El Problema de los LLMs Comerciales:
Los LLMs generalistas (ChatGPT, Gemini sin RAG) alucinan gravemente en dosificaciones numéricas ($g/ha$ vs $L/ha$) y sufren de **contaminación cross-jurisdiccional**, recomendando químicos prohibidos en México o no autorizados para exportación u orgánicos.

---

## 🔬 2. Diseño Experimental y Arquitecturas Comparadas

El benchmark experimental compara 4 arquitecturas frente a un conjunto de $N=100$ consultas agronómicas adversarias de control (*Ground Truth* derivado de documentos oficiales):

1. **$M_1$ (Baseline LLM):** Modelo directo sin recuperación contextual (*Gemini 2.5 Flash / GPT-4o-mini*).
2. **$M_2$ (Standard Dense RAG):** Búsqueda semántica densa con Embeddings sobre *ChromaDB*.
3. **$M_3$ (Hybrid RAG):** Búsqueda combinada BM25 (léxica exacta para nombres de plagas y químicos) + Embeddings densos + *Re-ranking* (*BGE-Reranker*).
4. **$M_4$ (Hybrid RAG + Structured Guardrails):** $M_3$ con filtrado determinista de metadatos oficiales (COFEPRIS/OMRI/USDA) y esquemas `Pydantic`.

### Métricas de Evaluación (Framework RAGAS y Métricas Agronómicas):
* **Fidelidad (*Faithfulness*):** Porcentaje de afirmaciones respaldadas 100% por el documento oficial.
* **Exactitud de Dosificación (*Dosage Accuracy %*):** Precisión exacta en el rango numérico de aplicación.
* **Tasa de Infracción Regulatoria (*Regulatory Violation Rate %*):** Recomendaciones que violan normas orgánicas o de exportación.
* **Context Recall & Answer Relevance.**

---

## 👥 3. Distribución del Equipo de Desarrollo (3 Estudiantes)

* **Alumno 1 (Data & Corpus Lead):** Ingesta, limpieza, chunking y metadatos del catálogo COFEPRIS, SENASICA y lista OMRI (`src/data_ingest.py`, `data/processed/`).
* **Alumno 2 (RAG Architecture Lead):** Motor RAG Híbrido en Python con ChromaDB, BM25 y API FastAPI (`src/rag_engine.py`, `src/app.py`).
* **Alumno 3 (Evaluation & UI Lead):** Benchmark experimental RAGAS, matrices de confusión, gráficas y frontend Tailwind (`src/eval_benchmark.py`).

---

## 🛡️ 4. Gobernanza y Guardrails de Código

* **Regla de Oro:** `main` protegida, 1 Ticket = 1 Alumno = 1 Rama independiente (`feature/issue-<NUMERO>-<nombre>`).
* **Inmutabilidad en CI:** `.github/workflows/guardrails.yml` bloquea automáticamente cualquier PR que modifique archivos de gobernanza sin autorización del Director.
* **CODEOWNERS:** Propiedad exclusiva de lineamientos asignada a `@cfcortesmx`.

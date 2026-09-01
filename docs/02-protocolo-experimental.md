# 🔬 Protocolo Experimental y Métricas Científicas: PhytoRAG-Tropical

Este documento define la metodología científica formal, el diseño experimental y las fórmulas de evaluación estadística para el artículo científico.

---

## 1. Diseño Experimental y Arquitecturas Comparadas

El estudio compara el rendimiento de **4 arquitecturas técnicas** frente a un conjunto de evaluación de $N=100$ consultas fitosanitarias de control:

1. **$M_1$ (Baseline LLM):** Modelo de lenguaje directo sin recuperación contextual (*Zero-Shot / Few-Shot*).
2. **$M_2$ (Standard Vector RAG):** Recuperación basada únicamente en similitud del coseno sobre embeddings densos en *ChromaDB*.
3. **$M_3$ (Hybrid RAG):** Recuperación combinada con *BM25* (coincidencia léxica exacta para nombres químicos y registros) + Embeddings densos + *Re-ranking* con modelo de ordenamiento (*BGE-Reranker*).
4. **$M_4$ (Hybrid RAG + Structured Guardrails):** $M_3$ complementado con esquemas Pydantic deterministas para validación de rangos numéricos de dosis y filtrado estricto por régimen (*Convencional*, *Orgánico OMRI*, *Exportación USDA*).

---

## 2. Métricas de Evaluación Científica (Framework RAGAS & Métricas Agronómicas)

### 2.1. Fidelidad al Documento Oficial (*Faithfulness / Zero-Hallucination Rate*)
Mide si todas las afirmaciones realizadas por el modelo se derivan matemáticamente del contexto oficial recuperado:

$$\text{Faithfulness} = \frac{|\text{Afirmaciones sustentadas por el contexto oficial}|}{|\text{Total de afirmaciones emitidas por la IA}|}$$

* **Objetivo:** $\ge 0.98$ en $M_4$.

### 2.2. Precisión en Dosificación Fitosanitaria (*Dosage Accuracy*)
Evalúa si la dosis recomendada ($D_{\text{pred}}$) coincide exactamente con el rango autorizado en la ficha oficial ($[D_{\min}, D_{\max}]$):

$$\text{Exactitud de Dosis} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(D_{\min}^{(i)} \le D_{\text{pred}}^{(i)} \le D_{\max}^{(i)})$$

### 2.3. Tasa de Infracción Regulatoria (*Regulatory Compliance Violation Rate - RCVR*)
Porcentaje de respuestas donde el modelo sugiere un ingrediente no autorizado para el mercado solicitado (ej. químico sintético en huerta orgánica o no aprobado por EPA para exportación):

$$\text{RCVR} = \frac{|\text{Consultas con recomendación infractora}|}{N} \times 100\%$$

* **Objetivo:** $0.0\%$ en $M_4$.

### 2.4. Recuperación de Contexto (*Context Recall & Precision*)
* **Context Recall:** Proporción de fichas técnicas relevantes recuperadas en el top-$k$.
* **Answer Relevance:** Grado de concordancia semántica directa entre la respuesta emitida y la duda del usuario.

---

## 3. Protocolo de Construcción del Banco de Evaluación (*Ground Truth*)

Para garantizar reproducibilidad absoluta y eliminar sesgos subjetivos:
1. Las 100 consultas de prueba se extraen y derivan **directamente de los registros oficiales de COFEPRIS, SENASICA, fichas DEAQ y lista OMRI**.
2. Cada caso de prueba incluye:
   - `id_consulta`: Identificador único.
   - `cultivo`: Limón, Mango o Papaya.
   - `problema_fitosanitario`: Plaga, enfermedad o deficiencia.
   - `regimen`: Convencional, Orgánico Certificado, Exportación EE.UU.
   - `ground_truth_producto`: Nombre comercial e ingrediente activo oficial.
   - `ground_truth_registro`: Número oficial COFEPRIS.
   - `ground_truth_dosis`: Rango exacto de aplicación ($g/ha$, $L/100L$).
   - `ground_truth_is`: Días de intervalo de seguridad.
   - `fuente_documental`: Ficha técnica oficial y página de referencia.

# 🤖 Instrucciones para Agentes de IA en PhytoRAG-Tropical
### (Antigravity, Cursor, Claude Code, GitHub Copilot)

Bienvenido, Agente de IA. Estás asistiendo a estudiantes de la Facultad de Telemática (Universidad de Colima) en el proyecto **PhytoRAG-Tropical**, dirigido por el **Dr. Carlos Flores**.

Tu rol es guiar al estudiante de forma pedagógica, respetar los estándares de ingeniería y escribir código modular en Python y RAG siguiendo las directrices del proyecto.

---

## 🛠️ 1. Setup Inicial del Entorno (Guía para el Agente)

Cuando el estudiante te pida inicializar el proyecto o ejecutar código por primera vez, ayúdale a correr estos pasos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Proyectos-UCOL/phytorag-tropical.git
cd phytorag-tropical

# 2. Crear y activar el entorno virtual de Python
python3 -m venv .venv
source .venv/bin/activate    # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias oficiales
pip install -r requirements.txt

# 4. Configurar APIs de Inteligencia Artificial
cp .env.example .env
# - Indicar al estudiante que configure su GEMINI_API_KEY gratuita (desde https://aistudio.google.com/)
# - Para modelos de pago (GPT-4o, Claude 3.5), instruir al estudiante que solicite la OPENROUTER_API_KEY al Dr. Carlos Flores

# 5. Probar el servidor backend inicial
python src/app.py
```

---

## 🧩 2. Skills y Herramientas que el Agente debe Activar / Utilizar

| Área | Skill / Herramienta Recomendada | Propósito y Uso |
| :--- | :--- | :--- |
| **Metodología y Especificación** | **`spec-kit` / Spec-Driven Development** | Escribir contratos de interfaz y esquemas Pydantic antes de implementar la lógica RAG. |
| **Diseño y Frontend** | **`modern-web-guidance` & `taste-skill`** | Implementar la interfaz web con Tailwind CSS siguiendo los tokens de `docs/05-sistema-de-diseno-y-tokens.md`. |
| **Calidad de Código Python** | **`ruff`** | Formatear con `ruff format .` y verificar lints con `ruff check .` antes de abrir cualquier Pull Request. |
| **Evaluación RAG** | **`ragas`** | Medir formalmente *Faithfulness*, *Answer Relevance* y *Context Recall*. Cero métricas alucinadas. |

---

## 🚫 3. Reglas y Guardrails Innegociables (Strict Rules)

1. **NUNCA hagas commits directos a `main`:**
   - Todo trabajo se realiza en ramas de feature siguiendo la convención:
     `feature/issue-<NUMERO>-<descripcion-corta>` (ej. `feature/issue-01-ingesta-senasica`).
2. **Revisión Obligatoria por Pull Request:**
   - Todo cambio debe integrarse mediante un **Pull Request (PR)** asignado al Dr. Carlos Flores (`@cfcortesmx`).
3. **Regla Anti-Colisiones (1 Ticket = 1 Alumno):**
   - Cada estudiante trabaja en su propio issue y archivo asignado. Nunca modifiques archivos ajenos sin coordinar.
4. **Calidad de Código y Linters:**
   - En Python: usar tipos explícitos (`Pydantic`), formato con `ruff` y docstrings en español.
   - En Frontend: usar Tailwind CSS respetando los tokens de diseño.
5. **No Alucinaciones Numéricas en Dosificación:**
   - Todo dato de dosis de agroquímicos debe venir obligatoriamente del documento recuperado por el RAG. Está estrictamente prohibido que el LLM invente valores de dosificación o registros sanitarios.

---

## 🏛️ 4. Estructura y Archivos Clave del Repositorio

* `requirements.txt`: Dependencias oficiales fijadas.
* `.env.example`: Plantilla de variables de entorno (`GEMINI_API_KEY`, `OPENROUTER_API_KEY`).
* `docs/01-guia-estudiantes.md`: Guía de onboarding y roles de los 3 estudiantes.
* `docs/02-protocolo-experimental.md`: Métricas de evaluación experimental y framework RAGAS.
* `docs/03-guia-redaccion-humana.md`: Directrices para redactar reportes y papers sin texto detectable de IA.
* `docs/04-workflow-y-guardrails.md`: Flujo de trabajo en Git y reglas anti-colisiones.
* `docs/05-sistema-de-diseno-y-tokens.md`: Tokens de diseño y micro-interacciones UI.
* `src/data_ingest.py`: Módulo de ingesta y chunking de normativas.
* `src/rag_engine.py`: Motor de búsqueda híbrida y generación RAG.
* `src/eval_benchmark.py`: Evaluador experimental con RAGAS.
* `src/app.py`: Servidor web FastAPI.

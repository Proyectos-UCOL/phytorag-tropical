# 🎨 Sistema de Diseño y Tokens de Interfaz: PhytoRAG-Tropical
### Basado en TasteSkill / Modern Web Guidance / Emil Kowalski

Este documento define la paleta semántica, tipografía, micro-interacciones y tokens de Tailwind CSS para la interfaz web del Consultor Fitosanitario.

---

## 🌿 1. Paleta de Colores Semántica (Tokens)

La paleta refleja rigor científico, naturaleza tropical y claridad de advertencias fitosanitarias:

| Token Semántico | Clase Tailwind | Valor Hex | Uso / Propósito |
| :--- | :--- | :--- | :--- |
| **`brand-primary`** | `emerald-600` | `#059669` | Identidad institucional, botones principales, estado saludable. |
| **`brand-accent`** | `lime-500` | `#84cc16` | Elementos interactivos, badges de certificación orgánica OMRI. |
| **`warning-phi`** | `amber-500` | `#f59e0b` | Alertas de Intervalo de Seguridad (PHI) y días antes del corte. |
| **`alert-danger`** | `rose-600` | `#e11d48` | Químicos restringidos, incompatibilidades de exportación o sobredosis. |
| **`surface-bg`** | `slate-50` | `#f8fafc` | Fondo de la aplicación. |
| **`surface-card`** | `white` | `#ffffff` | Tarjetas de respuesta del consultor con borde sutil `slate-200`. |
| **`text-primary`** | `slate-900` | `#0f172a` | Encabezados y títulos técnicos de patologías. |
| **`text-muted`** | `slate-500` | `#64748b` | Citas de registros COFEPRIS y metadatos secundarios. |

---

## 🧩 2. Componentes Clave de la Interfaz

1. **Panel de Consulta con Filtros de Cumplimiento (*Compliance Badges*):**
   * Selector rápido de cultivo: *Limón Persa*, *Limón Mexicano*, *Mango*, *Papaya*.
   * Toggle de régimen: *Convencional (México)*, *Orgánico Certificado (OMRI/LPO)*, *Exportación EE.UU. (USDA)*.
2. **Tarjeta de Recomendación Fitosanitaria Estructurada:**
   * **Badge de Registro:** Número COFEPRIS en chip monoespaciado (`font-mono text-xs bg-slate-100 px-2 py-1 rounded`).
   * **Indicador de Dosis:** Rango numérico destacado con unidades claras ($kg/ha$ o $ml/100L$).
   * **Semáforo de Seguridad (PHI):** Días de retiro antes de cosecha con aviso de advertencia.
   * **Cita del Documento Oficial:** Acordeón desplegable con el fragmento textual oficial recuperado por el RAG.

---

## ⚡ 3. Micro-interacciones y Accesibilidad
* **Transiciones:** Suaves (150ms a 200ms `ease-in-out`) en botones y hover states.
* **Accesibilidad:** Cumplimiento de contraste WCAG 2.2 AA en todos los textos y áreas táctiles mínimas de 44x44px.

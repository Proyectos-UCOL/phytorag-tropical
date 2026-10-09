"""
PhytoRAG-Tropical: API del Consultor Agronómico y Fitosanitario
Facultad de Telemática — Universidad de Colima
Director: Dr. Carlos Flores
"""

import os
import sys
from pathlib import Path

# Garantizar que la raíz del proyecto esté en sys.path para ejecuciones directas
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(
    title="PhytoRAG-Tropical API",
    description="Consultor Agronómico Especializado en Vademécum Oficial y Cumplimiento Normativo",
    version="0.1.0",
)


class ConsultaFitosanitaria(BaseModel):
    """Modelo de entrada para la consulta del agricultor o agrónomo."""

    cultivo: str = Field(
        ..., description="Cultivo analizado (ej. Limon, Mango, Papaya)"
    )
    problema_o_sintoma: str = Field(
        ..., description="Plaga, hongo o síntoma observado (ej. Cancro, Trips, HLB)"
    )
    regimen: str = Field(
        default="convencional",
        description="Régimen de producción: 'convencional', 'organico_omri' o 'exportacion_usda'",
    )
    etapa_fenologica: str | None = Field(
        default=None,
        description="Etapa del cultivo (ej. Floración, Brote vegetativo, Cosecha)",
    )


class RecomendacionTratamiento(BaseModel):
    """Esquema de salida estructurada de la recomendación fitosanitaria."""

    producto_comercial: str
    ingrediente_activo: str
    registro_sanitario_cofepris: str
    dosis_autorizada: str
    intervalo_seguridad_dias: int
    aprobacion_organica_omri: bool
    compatible_exportacion_usda: bool
    recomendacion_agronomica: str
    fragmento_oficial_citado: str
    fuente_documental: str


@app.get("/")
def estado_servicio():
    return {
        "sistema": "PhytoRAG-Tropical",
        "estado": "operativo",
        "director": "Dr. Carlos Flores",
        "institucion": "Facultad de Telemática — Universidad de Colima",
        "documentacion": "/docs",
    }


try:
    from src.rag_engine import MotorPhytoRAG
except ModuleNotFoundError:
    from rag_engine import MotorPhytoRAG

# Instancia global del Motor RAG Híbrido
motor_rag = MotorPhytoRAG()


@app.post("/consultar", response_model=RecomendacionTratamiento)
def consultar_fitosanidad(consulta: ConsultaFitosanitaria):
    """
    Endpoint principal para consultar recomendaciones fitosanitarias.
    Realiza recuperación híbrida (BM25 + ChromaDB) y generación con Gemini.
    """
    try:
        # Construir consulta contextualizada
        query = f"Cultivo: {consulta.cultivo}. Problema: {consulta.problema_o_sintoma}."
        if consulta.etapa_fenologica:
            query += f" Etapa: {consulta.etapa_fenologica}."

        # 1. Recuperar fragmentos normativos oficiales con filtro estricto por cultivo
        contexto_recuperado = motor_rag.recuperar_documentos(
            query=query, top_k=3, cultivo=consulta.cultivo
        )

        # 2. Generar dictamen fitosanitario con guardrails deterministas y anti off-label
        resultado = motor_rag.generar_recomendacion(
            consulta_texto=query,
            contexto=contexto_recuperado,
            regimen=consulta.regimen,
            cultivo=consulta.cultivo,
        )

        return RecomendacionTratamiento(**resultado)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la consulta fitosanitaria con el Motor RAG: {e!s}",
        ) from e


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    print(f"[INICIO] Servidor PhytoRAG-Tropical en http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

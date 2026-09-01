"""
PhytoRAG-Tropical: API del Consultor Agronómico y Fitosanitario
Facultad de Telemática — Universidad de Colima
Director: Dr. Carlos Flores
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PhytoRAG-Tropical API",
    description="Consultor Agronómico Especializado en Vademécum Oficial y Cumplimiento Normativo",
    version="0.1.0"
)


class ConsultaFitosanitaria(BaseModel):
    """Modelo de entrada para la consulta del agricultor o agrónomo."""
    cultivo: str = Field(..., description="Cultivo analizado (ej. Limon, Mango, Papaya)")
    problema_o_sintoma: str = Field(..., description="Plaga, hongo o síntoma observado (ej. Cancro, Trips, HLB)")
    regimen: str = Field(
        default="convencional",
        description="Régimen de producción: 'convencional', 'organico_omri' o 'exportacion_usda'"
    )
    etapa_fenologica: Optional[str] = Field(
        default=None,
        description="Etapa del cultivo (ej. Floración, Brote vegetativo, Cosecha)"
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
        "documentacion": "/docs"
    }


@app.post("/consultar", response_model=RecomendacionTratamiento)
def consultar_fitosanidad(consulta: ConsultaFitosanitaria):
    """Endpoint principal para consultar recomendaciones fitosanitarias."""
    # Este es el endpoint inicial que implementarán los estudiantes integrando rag_engine.py
    return RecomendacionTratamiento(
        producto_comercial="Oxicloruro de Cobre 50% PH (Ejemplo Semilla)",
        ingrediente_activo="Oxicloruro de Cobre",
        registro_sanitario_cofepris="RSCO-FUNG-0301-301-002-050",
        dosis_autorizada="2.0 a 3.0 kg/ha",
        intervalo_seguridad_dias=0,
        aprobacion_organica_omri=True,
        compatible_exportacion_usda=True,
        recomendacion_agronomica="Aplicar en aspersión foliar al detectar los primeros síntomas de cancro.",
        fragmento_oficial_citado="Autorizado para limonero contra Cancro Bacteriano (Xanthomonas citri) a dosis de 2-3 kg/ha.",
        fuente_documental="Catálogo Oficial COFEPRIS / Ficha Técnica DEAQ 2026"
    )


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Iniciando servidor PhytoRAG-Tropical en http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

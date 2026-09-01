"""
PhytoRAG-Tropical: Módulo de Ingesta, Limpieza y Chunking de Documentos
Responsable: Alumno 1 (Data & Corpus Lead)
Director: Dr. Carlos Flores | Facultad de Telemática — Universidad de Colima
"""

from pathlib import Path
from typing import List, Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"


def descargar_catalogos_oficiales():
    """Descarga y organiza los catálogos abiertos de COFEPRIS, SENASICA y OMRI."""
    print("🚀 [Alumno 1] Iniciando descarga de catálogos oficiales...")
    # TODO (Alumno 1): Implementar descarga automatizada desde datos.gob.mx y fuentes oficiales
    pass


def procesar_fichas_tecnicas() -> List[Dict]:
    """Lee los CSVs y PDFs oficiales, extrae los campos clave y genera fragmentos enriquecidos."""
    print("📝 [Alumno 1] Procesando y estructurando documentos normativos...")
    # TODO (Alumno 1): Implementar chunking y metadata tagging (cultivo, plaga, ingrediente, dosis, registro)
    return []


if __name__ == "__main__":
    descargar_catalogos_oficiales()
    procesar_fichas_tecnicas()

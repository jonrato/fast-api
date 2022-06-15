from typing import Optional
from pydantic import BaseModel

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int


cursos = [
    Curso(id=1, titulo='Programação em FAST-API', aulas=23, horas=8),
    Curso(id=2, titulo='Programação em FAST-API Avançado', aulas=62, horas=14)
    
]
from os import stat
from typing import Dict, List, Optional, Any
from fastapi.responses import JSONResponse
from distutils.log import debug
from fastapi import Path
from fastapi import Query
from fastapi import Header

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from models import Curso
from models import cursos

from time import sleep

def fake_db():
    try:
        print('Abrindo conexão com o banco de dados...')
        sleep(3)
    finally:
        print('Fechando conexão com o banco de dados...')
        sleep(2)

app = FastAPI(
    title='API de Aprendizado - Jonatas Ferreira',
    version='6.6.6',
    description='Uma API para estudo de FASTAPI'
    )



@app.get("/cursos", 
description='Retorna todos os cursos ou uma lista vazia', 
summary='Retorna todos os cursos',
response_model=List[Curso],
response_description='Cursos Encontrados com sucesso'
)
async def get_cursos(db: Any = Depends(fake_db) ):
    return cursos

@app.get("/cursos/{curso_id}")
async def get_curso(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 2', gt=0,lt=3),db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso,db: Any = Depends(fake_db)):

    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso

@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id

        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Não existe um curso com id {curso_id}')

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Não existe um curso com id {curso_id}')

@app.get('/calculadora')
async def calcular(a:int = Query(default=None,gt=5),b:int = Query(default=None, gt=10),x_geek: str = Header(default=None), c:Optional[int]=None):
    soma: int = a + b
    if c:
        soma = soma + c

    print(f'X-GEEK: {x_geek}')
    return {"resultado": soma}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000,
                 log_level="info", reload=True)
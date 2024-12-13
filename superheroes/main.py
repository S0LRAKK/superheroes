from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Importar el middleware de CORS
from database import SessionLocal, engine
from models import Base, Personaje, Usuario  # Agregar Usuario al importar los modelos

# Crear las tablas en la base de datos (solo si no existen)
Base.metadata.create_all(bind=engine)

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Configurar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes reemplazar "*" con una lista específica como ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo Pydantic para validación de datos de personaje
class PersonajeCreate(BaseModel):
    alias: str
    nombre: str
    edad: int

# Endpoint para obtener todos los personajes
@app.get("/personajes/")
def get_personajes(db: Session = Depends(get_db)):
    personajes = db.query(Personaje).all()
    return personajes

# Endpoint para agregar un nuevo personaje
@app.post("/personajes/")
def create_personaje(personaje: PersonajeCreate, db: Session = Depends(get_db)):
    nuevo_personaje = Personaje(alias=personaje.alias, nombre=personaje.nombre, edad=personaje.edad)
    db.add(nuevo_personaje)
    db.commit()
    db.refresh(nuevo_personaje)
    return nuevo_personaje

# Endpoint para obtener un personaje por su ID
@app.get("/personajes/{idpersonaje}")
def get_personaje(idpersonaje: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.idpersonaje == idpersonaje).first()
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return personaje

# Endpoint para actualizar un personaje
@app.put("/personajes/{idpersonaje}")
def update_personaje(idpersonaje: int, personaje: PersonajeCreate, db: Session = Depends(get_db)):
    personaje_db = db.query(Personaje).filter(Personaje.idpersonaje == idpersonaje).first()
    if personaje_db is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    personaje_db.alias = personaje.alias
    personaje_db.nombre = personaje.nombre
    personaje_db.edad = personaje.edad
    db.commit()
    db.refresh(personaje_db)
    return personaje_db

# Endpoint para eliminar un personaje
@app.delete("/personajes/{idpersonaje}")
def delete_personaje(idpersonaje: int, db: Session = Depends(get_db)):
    personaje_db = db.query(Personaje).filter(Personaje.idpersonaje == idpersonaje).first()
    if personaje_db is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    db.delete(personaje_db)
    db.commit()
    return {"detail": "Personaje eliminado"}

# Modelo Pydantic para validación de datos de usuario
class UsuarioCreate(BaseModel):
    usuario: str
    contraseña: str
    activa: bool

# Endpoint para agregar un nuevo usuario
@app.post("/usuarios/")
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(usuario=usuario.usuario, contraseña=usuario.contraseña, activa=usuario.activa)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Endpoint para obtener un usuario por su ID
@app.get("/usuarios/{idusuario}")
def get_usuario(idusuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.idusuario == idusuario).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Endpoint para actualizar un usuario
@app.put("/usuarios/{idusuario}")
def update_usuario(idusuario: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.idusuario == idusuario).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario_db.usuario = usuario.usuario
    usuario_db.contraseña = usuario.contraseña
    usuario_db.activa = usuario.activa
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

# Endpoint para eliminar un usuario
@app.delete("/usuarios/{idusuario}")
def delete_usuario(idusuario: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.idusuario == idusuario).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario_db)
    db.commit()
    return {"detail": "Usuario eliminado"}
from fastapi import FastAPI, Form, UploadFile, File
import os
import uuid

app = FastAPI()

@app.get('/')
def bienvenida():
    print("Atendiendo GET / ")
    respuesta = {"mensaje": "Bienvenido"}
    return respuesta

@app.post("/usuarios")
async def registrar_usuario(nombre: str = Form(...), direccion: str = Form(...), 
                            es_vip: bool = Form(False), fotografia: UploadFile = File(...)):
    
    home_usuario = os.path.expanduser("~")
    ruta_fotos_vip = os.path.join(home_usuario, "fotos-usuario-vip")
    ruta_fotos_no_vip = os.path.join(home_usuario, "fotos-usuarios")
    
    os.makedirs(ruta_fotos_vip, exist_ok=True)
    os.makedirs(ruta_fotos_no_vip, exist_ok=True)
    
    print(f"Nombre: {nombre}")
    print(f"Direccion: {direccion}")
    print(f"Usuario Vip: {es_vip}")
    
    carpeta_destino = ruta_fotos_vip if es_vip else ruta_fotos_no_vip
    
    nombre_archivo = f"{uuid.uuid4()}{os.path.splitext(fotografia.filename)[1]}"
    ruta_foto = os.path.join(carpeta_destino, nombre_archivo)
    
    with open (ruta_foto, "wb") as archivo:
        archivo.write(await fotografia.read())
        
    print (f"Foto guardada en: {ruta_foto}")
    
    #Respuesta Json
    respuesta = {
        "nombre": nombre,
        "direccion": direccion,
        "es_vip": es_vip,
        "ruta_foto": ruta_foto
    }
    return respuesta
    

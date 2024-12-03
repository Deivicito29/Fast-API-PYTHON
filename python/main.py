from fastapi import FastAPI, HTTPException
from typing import List
from models import Producto, ProductoCreate

app = FastAPI()

# Almacenamiento en memoria (simulando base de datos)
productos_db = []

# Ruta para crear un producto
@app.post("/productos/", response_model=Producto)
async def crear_producto(producto: ProductoCreate):
    id_nuevo = len(productos_db) + 1
    nuevo_producto = Producto(id=id_nuevo, **producto.dict())
    productos_db.append(nuevo_producto)
    return nuevo_producto

# Ruta para obtener todos los productos
@app.get("/productos/", response_model=List[Producto])
async def obtener_productos():
    return productos_db

# Ruta para obtener un producto por ID
@app.get("/productos/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: int):
    producto = next((p for p in productos_db if p.id == producto_id), None)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Ruta para actualizar un producto
@app.put("/productos/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: int, producto_actualizado: ProductoCreate):
    producto = next((p for p in productos_db if p.id == producto_id), None)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto.nombre = producto_actualizado.nombre
    producto.descripcion = producto_actualizado.descripcion
    producto.precio = producto_actualizado.precio
    return producto

# Ruta para eliminar un producto
@app.delete("/productos/{producto_id}", response_model=Producto)
async def eliminar_producto(producto_id: int):
    producto = next((p for p in productos_db if p.id == producto_id), None)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    productos_db.remove(producto)
    return producto
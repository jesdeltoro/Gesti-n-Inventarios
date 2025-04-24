class Producto:
    def __init__(self, id=None, nombre=None, cantidad=None, precio=None, categoria=None):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.categoria = categoria
        
    def __str__(self):
        return (f"Producto(id={self.id}, nombre={self.nombre}, " 
                f"cantidad={self.cantidad}, precio={self.precio}, categoria={self.categoria})")
from conexion import Conexion
from producto import Producto

import random

class ProductoDAO:
    SELECCIONAR = "SELECT * FROM productos ORDER BY id"
    INSERTAR = "INSERT INTO productos (nombre, cantidad, precio, categoria) VALUES (%s, %s, %s, %s)"
    ACTUALIZAR = "UPDATE productos SET nombre=%s, cantidad=%s, precio=%s, categoria=%s WHERE id=%s"
    ELIMINAR = "DELETE FROM productos WHERE id=%s"
    SELECCIONAR_POR_ID = "SELECT * FROM productos WHERE id=%s"
    SELECCIONAR_POR_NOMBRE = "SELECT * FROM productos WHERE nombre like %s"
    SELECCIONAR_CATEGORIAS = "SELECT DISTINCT categoria FROM productos"
    
    
    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            productos = []
            for registro in registros:
                producto = Producto(
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3],
                    registro[4]
                )
                productos.append(producto)
            return productos
        except Exception as e:
            print(f'Ocurrió un error al seleccionar los productos: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                print("Conexión liberada después de la selección.")
                
    @classmethod
    def insertar(cls, producto):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (producto.nombre, producto.cantidad, producto.precio, producto.categoria)  # Asegúrate de que los valores coincidan con las columnas
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            print(f'Producto insertado: {producto}')
        except Exception as e:
            print(f'Ocurrió un error al insertar el producto: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                print("Conexión liberada después de la inserción.")

    @classmethod
    def actualizar(cls, producto):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (producto.nombre, producto.cantidad, producto.precio,producto.categoria, producto.id)
            cursor.execute(cls.ACTUALIZAR, valores)
            conexion.commit()
            print(f'Producto actualizado: {producto}')
        except Exception as e:
            print(f'Ocurrió un error al actualizar el producto: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                print("Conexión liberada después de la actualización.")
                
    @classmethod
    def eliminar(cls, id_producto):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.ELIMINAR, (id_producto,))
            conexion.commit()
            print(f'Producto con ID {id_producto} eliminado.')
        except Exception as e:
            print(f'Ocurrió un error al eliminar el producto: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                print("Conexión liberada después de la eliminación.")
                
    @classmethod
    def seleccionar_por_id(cls, id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_POR_ID, (id,))
            registro = cursor.fetchone()
            if registro:
                return Producto(
                    id=registro[0],
                    nombre=registro[1],
                    cantidad=registro[2],
                    precio=registro[3],
                    categoria=registro[4]  # Asegúrate de que este índice corresponda a la categoría
                )
        except Exception as e:
            print(f'Ocurrió un error al seleccionar el producto por ID: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                
    @classmethod
    def seleccionar_por_nombre(cls, nombre):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_POR_NOMBRE, (nombre,))
            registro = cursor.fetchone()
            if registro:
                return Producto(
                    id=registro[0],
                    nombre=registro[1],
                    cantidad=registro[2],
                    precio=registro[3],
                    categoria=registro[4]
                )
        except Exception as e:
            print(f'Ocurrió un error al seleccionar un producto por nombre: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
        return None
        
                
                
if __name__ == '__main__':
    
    # Test listar todos los productos
    # productos = ProductoDAO.seleccionar()
    # for producto in productos:
    #     print(producto)
    
    # Test seleccionar un producto por ID
    # id_producto = 1  # Cambia esto por el ID que deseas buscar
    # producto = ProductoDAO.seleccionar_por_id(id_producto)
    # if producto:
    #     print(f'Producto encontrado: {producto}')
    # else:
    #     print(f'No se encontró el producto con ID {id_producto}')
    
    # Test seleccionar un producto por nombre
    nombre_producto = 'Producto A'  # Cambia esto por el nombre que deseas buscar
    producto = ProductoDAO.seleccionar_por_nombre(nombre_producto)
    if producto:
        print(f'Producto encontrado: {producto}')
    else:
        print(f'No se encontró el producto con nombre {nombre_producto}')

        
    
        

    # Test inserting new products
    # nombres = ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E', 
    #             'Producto F', 'Producto G', 'Producto H', 'Producto I', 'Producto J']
    # cantidades = [10, 20, 30, 40, 50]
    # precios = [100.0, 200.0, 300.0, 400.0, 500.0]
    # categorias = ['Categoría 1', 'Categoría 2', 'Categoría 3', 'Categoría 4', 'Categoría 5']

    # Seleccionar 10 nombres únicos
    # nombres_unicos = random.sample(nombres, 10)

    # lista_productos = [
    #     Producto(
    #         nombre=nombre,
    #         cantidad=random.choice(cantidades),
    #         precio=random.choice(precios),
    #         categoria=random.choice(categorias)
    #     )
    #     for nombre in nombres_unicos
    # ]

    # for producto in lista_productos:
    #     ProductoDAO.insertar(producto)
    #     print(f'Producto insertado: {producto}')


    # Test updating a product
    # producto_a_actualizar = Producto(
    #     id=1,  # Suponiendo que el ID 1 existe en la base de datos
    #     nombre='Producto Actualizado',
    #     cantidad=99,
    #     precio=999.99,
    #     categoria='Categoría Actualizada'
    # )
    # ProductoDAO.actualizar(producto_a_actualizar)
    # print(f'Producto actualizado: {producto_a_actualizar}')

# Test deleting a product
    # id_producto_a_eliminar = 18  # Suponiendo que el ID 1 existe en la base de datos
    # ProductoDAO.eliminar(id_producto_a_eliminar)
    # print(f'Producto con ID {id_producto_a_eliminar} eliminado.')

    # Test seleccionar categorías
    categorias = ProductoDAO.seleccionar_categorias()
    print(f'Categorías encontradas: {categorias}')










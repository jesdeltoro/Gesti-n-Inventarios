from flask import Flask, redirect, render_template, url_for, request, jsonify
from producto import Producto
from producto_forma import ProductoForma
from producto_dao import ProductoDAO  # Replace 'your_module' with the actual module name where ProductoDAO is defined
from waitress import serve # Importar waitress para servir la aplicación
from flask_cors import CORS # Importar CORS para habilitar CORS



app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

app.config['SECRET_KEY'] = 'llave_secreta_123'

titulo_app = 'Gestión de inventario'

@app.route('/')
def inicio():
    categorias = [
        ('alimentación', 'Alimentación'),
        ('droguería', 'Droguería'),
        ('menaje de cocina', 'Menaje de Cocina'),
        ('jardinería', 'Jardinería')
    ]  # Lista estática de categorías
    forma = ProductoForma()
    forma.cargar_categorias(categorias)  # Cargar las categorías en el formulario
    productos = ProductoDAO.seleccionar()  # Obtener productos
    return render_template('index.html', titulo=titulo_app, productos=productos, forma=forma)

@app.route('/index.html')
def inicio_index():
    app.logger.debug('Entramos al path de inicio /index.html')
    # Recuperamos los productos de la base de datos
    productos = ProductoDAO.seleccionar()
    # Creamos un objeto de formulario producto vacío
    producto = Producto()  # Asegúrate de que Producto() esté correctamente definido
    # Creamos un objeto de formulario producto vacío
    producto_forma = ProductoForma(obj=producto)
    
    return render_template('index.html', titulo=titulo_app, productos=productos, forma=producto_forma)

@app.route('/guardar', methods=['POST'])
def guardar():
    categorias = [
        ('alimentación', 'Alimentación'),
        ('droguería', 'Droguería'),
        ('menaje de cocina', 'Menaje de Cocina'),
        ('jardinería', 'Jardinería')
    ]
    producto = Producto()
    producto_forma = ProductoForma()
    producto_forma.cargar_categorias(categorias)
    if producto_forma.validate_on_submit():
        producto_forma.populate_obj(producto)
        # Verificar si el nombre ya existe en otro producto con un ID diferente
        if ProductoDAO.existe_nombre(producto.nombre, producto.id):
            app.logger.warning(f'El nombre del producto "{producto.nombre}" ya existe en otro producto.')
            mensaje = f'El nombre del producto "{producto.nombre}" ya está en uso por otro producto. Por favor, elija otro nombre.'
            productos = ProductoDAO.seleccionar()
            return render_template('index.html', titulo=titulo_app, productos=productos, forma=producto_forma, mensaje=mensaje)
        # Si no hay conflicto, guardar o actualizar el producto
        if not producto.id:
            ProductoDAO.insertar(producto)
            app.logger.debug(f'Producto guardado: {producto}')
        else:
            ProductoDAO.actualizar(producto)
            app.logger.debug(f'Producto actualizado: {producto}')
        return redirect(url_for('inicio'))
    else:
        app.logger.error('Error al validar el formulario')
        for field, errors in producto_forma.errors.items():
            for error in errors:
                app.logger.error(f'Error en el campo {field}: {error}')
        productos = ProductoDAO.seleccionar()
        return render_template('index.html', titulo=titulo_app, productos=productos, forma=producto_forma)

@app.route('/limpiar')
def limpiar():
    app.logger.debug('Limpiando la base de datos')
    # Limpiar la base de datos (eliminar todos los registros)
    return redirect(url_for('inicio'))

@app.route('/editar/<int:id>')
def editar(id):
    app.logger.debug(f'Editando producto con ID: {id}')
    producto = ProductoDAO.seleccionar_por_id(id)
    categorias = [
        ('alimentación', 'Alimentación'),
        ('droguería', 'Droguería'),
        ('menaje de cocina', 'Menaje de Cocina'),
        ('jardinería', 'Jardinería')
    ]  # Lista estática de categorías
    producto_forma = ProductoForma(obj=producto)
    producto_forma.cargar_categorias(categorias)  # Cargar categorías en el formulario
    producto_forma.categoria.data = producto.categoria
    productos = ProductoDAO.seleccionar()
    return render_template('index.html', titulo=titulo_app, productos=productos, forma=producto_forma)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    app.logger.debug(f'Eliminando producto con ID: {id}')
    # Eliminar el producto con el ID proporcionado
    ProductoDAO.eliminar(id)
    return redirect(url_for('inicio'))

@app.route('/producto', methods=['GET', 'POST'])
def producto():
    # Supongamos que ProductoDAO tiene un método llamado seleccionar_categorias
    categorias = ProductoDAO.seleccionar_categorias()  # Método para obtener las categorías
    form = ProductoForma()
    form.cargar_categorias(categorias)
    if form.validate_on_submit():
        # Procesar el formulario
        pass
    return render_template('producto.html', form=form)

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre_producto = request.form.get('nombre_buscar', '').strip()
    if not nombre_producto:
        app.logger.warning('El campo de búsqueda está vacío.')
        categorias = [
            ('alimentación', 'Alimentación'),
            ('droguería', 'Droguería'),
            ('menaje de cocina', 'Menaje de Cocina'),
            ('jardinería', 'Jardinería')
        ]
        forma = ProductoForma()
        forma.cargar_categorias(categorias)
        productos = ProductoDAO.seleccionar()
        mensaje = "Por favor, introduzca un nombre para buscar."
        return render_template('index.html', titulo=titulo_app, productos=productos, forma=forma, mensaje=mensaje)

    app.logger.debug(f'Buscando producto con nombre: {nombre_producto}')
    producto = ProductoDAO.seleccionar_por_nombre(f"%{nombre_producto}%")
    categorias = [
        ('alimentación', 'Alimentación'),
        ('droguería', 'Droguería'),
        ('menaje de cocina', 'Menaje de Cocina'),
        ('jardinería', 'Jardinería')
    ]
    forma = ProductoForma(obj=producto)
    forma.cargar_categorias(categorias)
    if producto:
        forma.categoria.data = producto.categoria
        app.logger.debug(f'Producto encontrado: {producto}')
    else:
        app.logger.warning(f'No se encontró producto con nombre: {nombre_producto}')
    productos = ProductoDAO.seleccionar()
    return render_template('index.html', titulo=titulo_app, productos=productos, forma=forma)

@app.route('/api/productos', methods=['GET'])
def api_listar_productos():
    productos = ProductoDAO.seleccionar()
    productos_json = [producto.__dict__ for producto in productos]
    return jsonify(productos_json)

@app.route('/api/productos/<int:id>', methods=['GET'])
def api_obtener_producto(id):
    producto = ProductoDAO.seleccionar_por_id(id)
    if producto:
        return jsonify(producto.__dict__)
    return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/api/productos', methods=['POST'])
def api_crear_producto():
    datos = request.json
    producto = Producto(
        nombre=datos.get('nombre'),
        cantidad=datos.get('cantidad'),
        precio=datos.get('precio'),
        categoria=datos.get('categoria')
    )
    ProductoDAO.insertar(producto)
    return jsonify({'mensaje': 'Producto creado exitosamente'}), 201

@app.route('/api/productos/<int:id>', methods=['PUT'])
def api_actualizar_producto(id):
    datos = request.json
    producto = ProductoDAO.seleccionar_por_id(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    producto.nombre = datos.get('nombre', producto.nombre)
    producto.cantidad = datos.get('cantidad', producto.cantidad)
    producto.precio = datos.get('precio', producto.precio)
    producto.categoria = datos.get('categoria', producto.categoria)
    ProductoDAO.actualizar(producto)
    return jsonify({'mensaje': 'Producto actualizado exitosamente'})

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def api_eliminar_producto(id):
    producto = ProductoDAO.seleccionar_por_id(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    ProductoDAO.eliminar(id)
    return jsonify({'mensaje': 'Producto eliminado exitosamente'})

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, threads=4)  # Cambia el puerto según sea necesario
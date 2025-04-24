from flask import Flask, redirect, render_template, url_for, request
from producto import Producto
from producto_forma import ProductoForma
from producto_dao import ProductoDAO  # Replace 'your_module' with the actual module name where ProductoDAO is defined

app = Flask(__name__)

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
    ]  # Lista estática de categorías
    producto = Producto()
    producto_forma = ProductoForma()
    producto_forma.cargar_categorias(categorias)  # Cargar categorías en el formulario
    if producto_forma.validate_on_submit():
        producto_forma.populate_obj(producto)
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

if __name__ == '__main__':
    app.run(debug=True)
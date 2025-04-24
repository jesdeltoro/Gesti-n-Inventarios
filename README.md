# Gestión de Inventarios

Este proyecto es una aplicación web para la gestión de inventarios, desarrollada con Flask y MySQL. Permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre productos almacenados en una base de datos.

## Estructura del Proyecto

### Archivos Principales

#### 1. `app.py`
Este archivo es el punto de entrada de la aplicación Flask. Contiene las rutas principales y la lógica para interactuar con el frontend y la base de datos.

- **Rutas principales**:
  - `/`: Página principal que muestra el formulario y la tabla de productos.
  - `/guardar`: Ruta para guardar o actualizar un producto.
  - `/limpiar`: Ruta para limpiar los datos (pendiente de implementación).
  - `/editar/<int:id>`: Ruta para editar un producto existente.
  - `/eliminar/<int:id>`: Ruta para eliminar un producto.

#### 2. `producto.py`
Define la clase `Producto`, que representa un producto en el inventario. Contiene los atributos básicos como `id`, `nombre`, `cantidad`, `precio` y `categoria`.

#### 3. `producto_forma.py`
Define el formulario `ProductoForma` utilizando Flask-WTF. Este formulario se utiliza para capturar los datos de los productos desde el frontend.

- Campos principales:
  - `id`: Campo oculto para identificar el producto.
  - `nombre`: Nombre del producto.
  - `cantidad`: Cantidad disponible.
  - `precio`: Precio del producto.
  - `categoria`: Categoría del producto (cargada dinámicamente).
  - `guardar`: Botón para guardar los datos.

#### 4. `producto_dao.py`
Contiene la clase `ProductoDAO`, que implementa las operaciones CRUD para interactuar con la base de datos.

- Métodos principales:
  - `seleccionar`: Obtiene todos los productos.
  - `insertar`: Inserta un nuevo producto.
  - `actualizar`: Actualiza un producto existente.
  - `eliminar`: Elimina un producto por su ID.
  - `seleccionar_por_id`: Obtiene un producto por su ID.
  - `seleccionar_por_nombre`: Busca un producto por su nombre.

#### 5. `conexion.py`
Implementa la clase `Conexion`, que gestiona el pool de conexiones a la base de datos utilizando `mysql.connector.pooling`.

- Métodos principales:
  - `obtener_pool`: Crea un pool de conexiones si no existe.
  - `obtener_conexion`: Obtiene una conexión del pool.
  - `liberar_conexion`: Libera una conexión al pool.

#### 6. `datosconexion.py`
Contiene las configuraciones de conexión a la base de datos, como el nombre de la base de datos, usuario, contraseña, host, puerto, y configuración del pool.

#### 7. `templates/index.html`
Archivo HTML que define la interfaz de usuario. Incluye:
- Un formulario para agregar o editar productos.
- Una tabla para listar los productos existentes.
- Botones para editar o eliminar productos.

#### 8. `backup_almacen.sql`
Archivo SQL que contiene la estructura y datos iniciales de la base de datos `almacen`. Incluye la tabla `productos` y algunos registros de ejemplo.

## Requisitos

- Python 3.8 o superior
- Flask
- Flask-WTF
- MySQL
- mysql-connector-python

## Configuración

1. **Base de Datos**:
   - Importa el archivo `backup_almacen.sql` en tu servidor MySQL para crear la base de datos y la tabla `productos`.

2. **Configuración de Conexión**:
   - Edita el archivo `datosconexion.py` con los datos de tu servidor MySQL.

3. **Instalación de Dependencias**:
   - Instala las dependencias necesarias ejecutando:
     ```bash
     pip install flask flask-wtf mysql-connector-python
     ```

## Ejecución

1. Inicia la aplicación ejecutando:
   ```bash
   python app.py
   ```
2. Accede a la aplicación en tu navegador en `http://127.0.0.1:5000`.

## Funcionalidades

- **Agregar Producto**: Completa el formulario y haz clic en "Guardar".
- **Editar Producto**: Haz clic en el botón de lápiz en la tabla, edita los datos y guarda.
- **Eliminar Producto**: Haz clic en el botón de basura en la tabla para eliminar un producto.
- **Listar Productos**: Los productos se muestran automáticamente en la tabla.

## Estructura de la Base de Datos

Tabla `productos`:
- `id`: Identificador único (INT, AUTO_INCREMENT).
- `nombre`: Nombre del producto (VARCHAR).
- `cantidad`: Cantidad disponible (INT).
- `precio`: Precio del producto (FLOAT).
- `categoria`: Categoría del producto (VARCHAR).



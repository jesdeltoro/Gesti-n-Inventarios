from mysql.connector import Error, pooling
import datosconexion  # Importamos los datos directamente

class Conexion:
    DATABASE = datosconexion.DATABASE
    USERNAME = datosconexion.USERNAME
    PASSWORD = datosconexion.PASSWORD
    DB_PORT = datosconexion.DB_PORT
    HOST = datosconexion.HOST
    POOL_SIZE = datosconexion.POOL_SIZE
    POOL_NAME = datosconexion.POOL_NAME
    pool = None

    @classmethod
    def obtener_pool(cls):
        if cls.pool is None:
            try:
                cls.pool = pooling.MySQLConnectionPool(
                    pool_name=cls.POOL_NAME,
                    pool_size=cls.POOL_SIZE,
                    host=cls.HOST,
                    port=cls.DB_PORT,
                    database=cls.DATABASE,
                    user=cls.USERNAME,
                    password=cls.PASSWORD
                )
            except Error as e:
                print(f"Ocurrió un error al obtener pool: {e}")
                print(f"Detalles: host={cls.HOST}, port={cls.DB_PORT}, database={cls.DATABASE}, user={cls.USERNAME}")
        return cls.pool

    @classmethod
    def obtener_conexion(cls):
        try:
            conexion = cls.obtener_pool().get_connection()
            return conexion
        except Error as e:
            print(f'Ocurrió un error al obtener la conexión: {e}')
            return None

    @classmethod
    def liberar_conexion(cls, conexion):
        if conexion:
            try:
                conexion.close()
            except Error as e:
                print(f'Ocurrió un error al liberar la conexión: {e}')
        else:
            print('No se puede liberar una conexión nula.')

if __name__ == '__main__':
    print("Variables cargadas desde datosconexion.py:")
    print(f"DATABASE: {Conexion.DATABASE}")
    print(f"USERNAME: {Conexion.USERNAME}")
    print(f"PASSWORD: {Conexion.PASSWORD}")
    print(f"DB_PORT: {Conexion.DB_PORT}")
    print(f"HOST: {Conexion.HOST}")
    print(f"POOL_SIZE: {Conexion.POOL_SIZE}")
    print(f"POOL_NAME: {Conexion.POOL_NAME}")

    pool = Conexion.obtener_pool()
    if pool:
        print("Pool de conexiones creado con éxito.")
    else:
        print("Error al crear el pool de conexiones.")

    conexion1 = pool.get_connection()
    if conexion1.is_connected():
        print("Conexión 1 obtenida con éxito.")
    else:
        print("Error al obtener la conexión 1.")

    Conexion.liberar_conexion(conexion1)

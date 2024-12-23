from decouple import config
from mysql import connector


db_name = config("SERVER_DB_NAME", cast=str)
db_user = config("SERVER_DB_USER", cast=str)
db_password = config("SERVER_DB_PASSWORD", cast=str)
db_host = config("SERVER_DB_HOST", cast=str)
db_port = config("SERVER_DB_PORT", cast=int)

table_name = "precondo"

def database_connector(
        name : str = db_name,
        user : str = db_user,
        password : str = db_password,
        host : str = db_host,
        port : int = db_port,
        autocommit = False
):
    try:
        print("Database-Name : ", name)
        db_connection = connector.connect(
            user = user,
            password = password,
            host = host,
            port = port,
            database = name,
            autocommit = autocommit,
            auth_plugin = "mysql-native-password"

        )
        db_connection.autocommit = autocommit
        cursor = db_connection.cursor(dictionary=True)

        return cursor, db_connection
    
    except Exception as e:
        print(f"Error occured while connecting to database : {e}")



import logging
from mysql.connector import pooling, Error as MySQLError


def load_config():
    return {
        "host": "172.16.4.8",
        "port": 3306,
        "user": "jmto",
        "password": "@jmt02024!#",
        "database": "",
    }


def create_connection_pool(config):
    try:
        pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,  # Adjust based on your requirements
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
        return pool
    except MySQLError as e:
        logging.error(f"Error creating connection pool: {e}")
        return None

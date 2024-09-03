import logging
import mysql.connector
from mysql.connector import Error


def load_config():
    # return {
    #     "host": "172.16.4.8",
    #     "port": 3306,
    #     "user": "jmto",
    #     "password": "@jmt02024!#",
    #     "database": "",
    # }
    return {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "",
        "database": "",
    }


def create_connection(config):
    """Create a MySQL database connection."""
    try:
        return mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
    except Error as e:
        logging.error(f"Connection error with mysql.connector: {e}")
        raise

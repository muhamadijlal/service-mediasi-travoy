import logging
import env
import mysql.connector

from database.query import get_data, insert_data, update_data
from database.config import loadConf
from database.map import mapping


def service_mediasi():
    dbSrc = env.dbSrc
    dbDst = env.dbDst
    db_sources = dbSrc.split(",")

    for dbSrc in db_sources:
        data = get_data(dbSrc)
        if data:
            result = mapping(data)
            config = loadConf()

            # Start transaction management
            conn = None

            try:
                conn = mysql.connector.connect(
                    host=config["host"],
                    port=config["port"],
                    user=config["user"],
                    password=config["password"],
                    database=config["database"],
                )

                # start the transactions
                conn.start_transaction()

                # Pass the connection to insert_data and update_data functions
                insert_data(result, dbDst, conn)
                update_data(data, dbSrc, conn)

                conn.commit()
                logging.info("Transaction committed successfully.")
                logging.info(
                    "======================================================================================"
                )
            except Exception as e:
                if conn:
                    conn.rollback()
                logging.error(f"Transaction failed: {e}")
                logging.info(
                    "======================================================================================"
                )

            finally:
                if conn:
                    conn.close()
        else:
            logging.info("Nothing to process")
            logging.info(
                "======================================================================================"
            )

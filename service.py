import env
import logging

from database.map import mapping
from mysql.connector import Error
from database.config import load_config, create_connection
from database.query import get_data, insert_data, update_data


def process_data(dbSrc, config1, config2):
    """Process data from source to destination databases."""
    data = get_data(dbSrc)
    if not data:
        logging.info("Nothing to process")
        logging.info("=" * 90)
        return

    result = mapping(data)

    try:
        with create_connection(config1) as conn1, create_connection(config2) as conn2:

            insert_data(result, conn2)
            update_data(data, conn1)

            conn2.commit()
            logging.info("Success Insert Data")
            conn1.commit()
            logging.info("Success flagging data")
            logging.info("=" * 90)

    except (Error, Exception) as e:
        logging.error(f"An error occurred: {e}")
        if "conn1" in locals():
            conn1.rollback()
        if "conn2" in locals():
            conn2.rollback()


def service_mediasi():
    """Main service function to mediate between source and destination databases."""
    dbSrc = env.dbSrc
    dbDst = env.dbDst
    db_sources = dbSrc.split(",")

    config = load_config()
    config1 = config.copy()
    config2 = config.copy()

    for db_sorce in db_sources:
        config1["database"] = db_sorce
        config2["database"] = dbDst

        process_data(db_sorce, config1, config2)

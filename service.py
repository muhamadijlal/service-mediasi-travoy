import env
import logging
from database.map import mapping
from database.config import load_config, create_connection_pool
from database.query import get_data, insert_data, update_data
from mysql.connector import Error as MySQLError


def process_data(dbSrc, config1, config2):
    """Process data from source to destination databases."""
    # Create connection pools
    pool1 = create_connection_pool(config1)
    pool2 = create_connection_pool(config2)

    if not pool1 or not pool2:
        logging.error("Failed to create connection pools")
        return

    data = get_data(dbSrc, pool1)  # Pass the pool to get_data

    if not data:
        logging.info("Nothing to process")
        logging.info("=" * 90)
        return

    result = mapping(data)

    conn2 = None
    conn1 = None

    try:
        # Start a transaction for the first connection (insert)
        conn2 = pool2.get_connection()
        conn2.start_transaction()  # Start transaction
        insert_data(result, conn2)

        # Start a transaction for the second connection (update)
        conn1 = pool1.get_connection()
        conn1.start_transaction()  # Start transaction
        update_data(data, conn1)

        # Commit both transactions
        conn2.commit()
        conn1.commit()
        logging.info("Data processing successful.")

    except (MySQLError, Exception) as e:
        logging.error(f"An error occurred: {e}")

        # Rollback for insert if conn2 is valid
        if conn2:
            conn2.rollback()  # Rollback on error for insert
            logging.info("Rolled back insert transaction.")

        # Rollback for update if conn1 is valid
        if conn1:
            conn1.rollback()  # Rollback on error for update
            logging.info("Rolled back update transaction.")

    finally:
        if conn2:
            conn2.close()  # Always close the connection
        if conn1:
            conn1.close()  # Always close the connection


def service_mediasi():
    """Main service function to mediate between source and destination databases."""
    dbSrc = env.dbSrc
    dbDst = env.dbDst
    db_sources = dbSrc.split(",")

    config = load_config()
    config1 = config.copy()
    config2 = config.copy()

    for db_source in db_sources:
        config1["database"] = db_source
        config2["database"] = dbDst

        process_data(db_source, config1, config2)

import logging
import env

from database.query import get_data, insert_data, update_data
from database.map import mapping


def service_mediasi():
    dbSrc = env.dbSrc
    dbDst = env.dbDst

    db_sources = dbSrc.split(",")

    for dbSrc in db_sources:
        data = get_data(dbSrc)

        if data is not None and len(data) > 0:
            result = mapping(data)

            insert_data(result, dbDst)
            update_data(data, dbSrc)

        else:
            logging.info("Data empty, no service is running")
            logging.info(
                "======================================================================================"
            )

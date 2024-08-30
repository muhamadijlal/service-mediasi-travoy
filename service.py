import logging
import env

from database.query import get_data, insert_data, update_data
from database.map import mapping


def service_mediasi():
    dbSrc = env.dbSrc
    dbDst = env.dbDst

    db_sources = dbSrc.split(",")

    data_each_db = {}
    data_flag = {}

    for db in db_sources:
        data = get_data(db)

        if data is not None:
            if len(data) > 0:
                result = mapping(data)

                data_each_db[db] = result
                data_flag[db] = data
            else:
                logging.info("Nothing to insert")
                logging.info(
                    "======================================================================================"
                )

    print(data)

    # for _, value in data_each_db.items():
    #     insert_data(value, dbDst)

    # for dbName, value in data_flag.items():
    #     update_data(value, dbName)

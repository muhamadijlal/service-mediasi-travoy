import logging
import mysql.connector
from database.config import loadConf


def get_data(dbSrc):
    """Retrieve data from db source"""

    config = loadConf("src")

    if config is None:
        logging.error("Failed to load database configuration.")
        return

    config["database"] = dbSrc

    conn = None
    logging.info("Getting data source ..")
    logging.info(f"Database source : {dbSrc}")

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
    except mysql.connector.Error as mysql_connector_error:
        logging.error(f"Connection error with mysql.connector: {mysql_connector_error}")

    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            f"""
                SELECT
                    id,
                    ruas_id,
                    asal_gerbang_id,
                    gerbang_id,
                    gardu_id,
                    tgl_lap,
                    shift,
                    perioda,
                    no_resi,
                    gol_sah,
                    etoll_id,
                    metoda_bayar_sah,
                    tgl_transaksi,
                    kspt_id,
                    pultol_id,
                    tarif,
                    sisa_saldo,
                    created_at
                FROM jid_transaksi_deteksi
                WHERE flag = 0
                AND tarif != 0
            """
        )

        rows = cur.fetchall()
        logging.info(f"Success getting data. data length: {len(rows)}")

        return rows

    except Exception as error:
        logging.error(f"Error while retrieving data: {error}")
        return None

    finally:
        if conn is not None:
            conn.close()


def insert_data(data, dbDst):
    """Insert data to db destination"""

    config = loadConf("dst")

    if config is None:
        logging.error("Failed to load database configuration.")
        return

    config["database"] = dbDst

    conn = None
    logging.info("Insert data into table destination ..")
    logging.info(f"Database destination : {dbDst}")

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
    except mysql.connector.Error as mysql_connector_error:
        logging.error(f"Connection error with mysql.connector: {mysql_connector_error}")

    try:
        cur = conn.cursor()

        query = """
                    INSERT INTO tx_card_toll_history(
                        tgl_report,
                        no_kartu,
                        nama_cabang,
                        gerbang,
                        kode_gardu,
                        tgl_transaksi,
                        bank,
                        shift,
                        periode,
                        tarif,
                        saldo,
                        no_resi,
                        id_pultol,
                        id_kspt,
                        kode_gerbang_asal,
                        golongan,
                        created_at,
                        nama_gerbang_asal
                    )VALUES(
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    ON DUPLICATE KEY UPDATE
                        tgl_report = VALUES(tgl_report),
                        no_kartu = VALUES(no_kartu),
                        nama_cabang = VALUES(nama_cabang),
                        gerbang = VALUES(gerbang),
                        kode_gardu = VALUES(kode_gardu),
                        tgl_transaksi = VALUES(tgl_transaksi),
                        bank = VALUES(bank),
                        shift = VALUES(shift),
                        periode = VALUES(periode),
                        tarif = VALUES(tarif),
                        saldo = VALUES(saldo),
                        no_resi = VALUES(no_resi),
                        id_pultol = VALUES(id_pultol),
                        id_kspt = VALUES(id_kspt),
                        kode_gerbang_asal = VALUES(kode_gerbang_asal),
                        golongan = VALUES(golongan),
                        created_at = VALUES(created_at),
                        nama_gerbang_asal = VALUES(nama_gerbang_asal)
                """

        cur.executemany(query, data)

        conn.commit()
        logging.info(f"Success insert {len(data)} data")

    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()


def update_data(data, dbSrc):
    """Update data to db source"""

    config = loadConf("src")

    if config is None:
        logging.error("Failed to load database configuration.")
        return

    config["database"] = dbSrc

    conn = None
    logging.info("Flaging data source ..")
    logging.info(f"Database source : {dbSrc}")

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
    except mysql.connector.Error as mysql_connector_error:
        logging.error(f"Connection error with mysql.connector: {mysql_connector_error}")

    try:
        cur = conn.cursor()

        # Prepare the SQL query with a placeholder
        sql_query = "UPDATE jid_transaksi_deteksi SET flag = %s WHERE id = %s"

        # Prepare the data for executemany
        update_values = [(1, x["id"]) for x in data]

        # Execute the query with the data
        cur.executemany(sql_query, update_values)

        conn.commit()
        logging.info(f"Success update {len(data)} data")
    except (Exception, mysql.connector.Error) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()

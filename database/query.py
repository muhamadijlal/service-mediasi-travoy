import logging
import mysql.connector
from database.config import load_config


def get_data(dbSrc):
    """Retrieve data from db source"""

    config = load_config()

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
        logging.error("=" * 90)

    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            f"""
                SELECT
                    a.id,
                    a.ruas_id,
                    a.asal_gerbang_id,
                    b.nama_asal_gerbang AS nama_asal_gerbang,
                    a.gerbang_id,
                    c.nama_asal_gerbang AS gerbang_nama,
                    a.gardu_id,
                    a.tgl_lap,
                    a.shift,
                    a.perioda,
                    a.no_resi,
                    a.gol_sah,
                    a.etoll_id,
                    a.metoda_bayar_sah,
                    a.tgl_transaksi,
                    a.kspt_id,
                    a.pultol_id,
                    a.tarif,
                    a.sisa_saldo
                FROM jid_transaksi_deteksi a
                LEFT JOIN asal_gerbang b ON a.asal_gerbang_id = b.id_asal_gerbang
                LEFT JOIN asal_gerbang c ON a.gerbang_id = c.id_asal_gerbang
                WHERE a.flag = 0
                AND a.tarif != 0
                ORDER BY a.tgl_transaksi ASC
                LIMIT 500
            """
        )

        rows = cur.fetchall()
        logging.info(f"Success getting data. data length: {len(rows)}")
        logging.info("=" * 90)

        return rows

    except Exception as error:
        logging.error(f"Error while retrieving data: {error}")
        logging.info("=" * 90)
        return None

    finally:
        if conn is not None:
            conn.close()


def insert_data(data, conn):
    """Insert data to db destination"""
    logging.info("Proccess insert data..")

    cur = conn.cursor()

    query = """
                INSERT INTO tx_card_toll_history(
                    tgl_report,
                    no_kartu,
                    kode_cabang,
                    nama_cabang,
                    gerbang,
                    nama_gerbang,
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
                    %s,
                    %s
                )
                ON DUPLICATE KEY UPDATE
                    tgl_report = VALUES(tgl_report),
                    no_kartu = VALUES(no_kartu),
                    kode_cabang = VALUES(kode_cabang),
                    nama_cabang = VALUES(nama_cabang),
                    gerbang = VALUES(gerbang),
                    nama_gerbang = VALUES(nama_gerbang),
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
                    nama_gerbang_asal = VALUES(nama_gerbang_asal)
            """

    cur.executemany(query, data)


def update_data(data, conn):
    """Update data to db source"""
    logging.info("Proccess flaging data..")
    logging.info("=" * 90)

    cur = conn.cursor()

    # Prepare the SQL query with a placeholder
    sql_query = "UPDATE jid_transaksi_deteksi SET flag = %s WHERE id = %s"

    # Prepare the data for executemany
    update_values = [(1, x["id"]) for x in data]

    # Execute the query with the data
    cur.executemany(sql_query, update_values)

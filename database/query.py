import logging
from mysql.connector import pooling
from database.config import load_config


def get_data(dbSrc, pool):
    """Retrieve data from db source using a connection from the pool"""
    logging.info("Getting data source ..")
    logging.info(f"Database source : {dbSrc}")

    conn = None
    try:
        conn = pool.get_connection()
        config = load_config()
        config["database"] = dbSrc

        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
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
        logging.info(f"Success getting data. Data length: {len(rows)}")
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
    logging.info("Process insert data..")

    try:
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
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                gerbang = VALUES(gerbang),
                tgl_report = VALUES(tgl_report),
                shift = VALUES(shift),
                kode_gardu = VALUES(kode_gardu),
                no_resi = VALUES(no_resi),
                no_kartu = VALUES(no_kartu)
        """
        cur.executemany(query, data)
        logging.info("Data insertion successful.")

    except Exception as error:
        logging.error(f"Error during data insertion: {error}")
        raise


def update_data(data, conn):
    """Update data to db source"""
    logging.info("Process flagging data..")
    logging.info("=" * 90)

    try:
        cur = conn.cursor()
        sql_query = "UPDATE jid_transaksi_deteksi SET flag = %s WHERE id = %s"
        update_values = [(1, x["id"]) for x in data]

        cur.executemany(sql_query, update_values)
        logging.info("Data update successful.")

    except Exception as error:
        logging.error(f"Error during data update: {error}")
        raise

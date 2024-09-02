import env


def mapping(data):
    new_array = []
    nama_cabang = env.namaCabang.upper()

    for index, _ in enumerate(data):
        asal_gerbang_id = (
            0
            if data[index]["asal_gerbang_id"] == ""
            else data[index]["asal_gerbang_id"]
        )

        result = [
            data[index]["tgl_lap"],  # tanggal report
            data[index]["etoll_id"],  # nomor kartu
            data[index]["ruas_id"],  # kode cabang
            nama_cabang,  # nama cabang
            data[index]["gerbang_id"],  # kode gerbang
            data[index]["gerbang_nama"],  # nama gerbang
            data[index]["gardu_id"],  # kode gardu
            data[index]["tgl_transaksi"],  # tanggal transaksi
            data[index]["metoda_bayar_sah"],  # bank
            data[index]["shift"],  # shift
            data[index]["perioda"],  # periode
            data[index]["tarif"],  # tarif
            data[index]["sisa_saldo"],  # saldo
            data[index]["no_resi"],  # no resi
            data[index]["pultol_id"],  # id_pultol
            data[index]["kspt_id"],  # id_kspt
            asal_gerbang_id,  # kode_gerbang_asal
            data[index]["gol_sah"],  # golongan
            data[index]["create_at"],  # created_at
            data[index]["nama_asal_gerbang"],  # nama_gerbang_asal
        ]

        new_array.append(result)

    data_tuples = [tuple(row) for row in new_array]

    return data_tuples

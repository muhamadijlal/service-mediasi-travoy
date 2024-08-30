def mapping(data):
    new_array = []

    for index, _ in enumerate(data):
        result = [
            data[index]["tgl_lap"],  # tanggal report
            data[index]["etoll_id"],  # nomor kartu
            data[index]["ruas_id"],  # nama cabang
            data[index]["gerbang_id"],  # nama gerbang
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
            data[index]["asal_gerbang_id"],  # kode_asal_gerbang
            data[index]["gol_sah"],  # golongan
            data[index]["create_at"],  # created_at
            data[index]["nama_asal_gerbang"],  # nama gerbang asal
        ]

        new_array.append(result)

    data_tuples = [tuple(row) for row in new_array]

    return data_tuples

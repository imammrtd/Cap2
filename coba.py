import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Imam12345",
    database="toko_db"
)
cursor = db.cursor()

# ===================== FUNGSI =====================

# 1. Read Table
def read_table():
    query = "SELECT * FROM penjualan"
    df = pd.read_sql(query, db)
    print("\n=== DATA PENJUALAN TOKO ===")
    print(df)

# 2. Show Statistik
def show_statistik():
    df = pd.read_sql("SELECT * FROM penjualan", db)
    print("\n=== STATISTIK DATA PENJUALAN ===")
    print("Rata-rata jumlah terjual:", df['jumlah'].mean())
    print("Rata-rata harga satuan:", df['harga_satuan'].mean())

# 3. Data Visualization
def data_visualization():
    while True:
        print("\n=== PILIH VISUALISASI DATA ===")
        print("1. Pie Chart Kategori")
        print("2. Histogram Jumlah Barang Terjual")
        print("3. Boxplot Harga Satuan per Kategori")
        print("4. Line Chart Penjualan per Tanggal")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih jenis chart: ")
        df = pd.read_sql("SELECT * FROM penjualan", db)
        if pilihan == "1":
            kategori_count = df['kategori'].value_counts()
            kategori_count.plot.pie(autopct='%1.1f%%', figsize=(6,6), title="Proporsi Kategori Barang")
            plt.show()
            plt.close()
            data_visualization()
        elif pilihan == "2":
            df['jumlah'].plot.hist(bins=5, rwidth=0.8, title="Distribusi Jumlah Barang Terjual")
            plt.xlabel("Jumlah")
            plt.show()
            plt.close()
            menu()
        elif pilihan == "3":
            sns.boxplot(x='kategori', y='harga_satuan', data=df)
            plt.title("Boxplot Harga Satuan Berdasarkan Kategori")
            plt.show()
            plt.close()
            menu()
        elif pilihan == "4":
            df['tanggal_transaksi'] = pd.to_datetime(df['tanggal_transaksi'])
            df_grouped = df.groupby('tanggal_transaksi').agg({'jumlah': 'sum'}).reset_index()
            df_grouped.plot(x='tanggal_transaksi', y='jumlah', title="Penjualan per Tanggal", kind='line')
            plt.xlabel("Tanggal")
            plt.ylabel("Jumlah Terjual")
            plt.show()
            plt.close()
            menu()
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")



# 4. Add Data
def add_data():
    nama = input("Masukkan nama barang: ")
    kategori = input("Masukkan kategori: ")
    jumlah = int(input("Masukkan jumlah: "))
    harga = float(input("Masukkan harga satuan: "))
    tanggal = input("Masukkan tanggal transaksi (YYYY-MM-DD): ")
    query = "INSERT INTO penjualan (nama_barang, kategori, jumlah, harga_satuan, tanggal_transaksi) VALUES (%s,%s,%s,%s,%s)"
    values = (nama, kategori, jumlah, harga, tanggal)
    cursor.execute(query, values)
    db.commit()
    print("Data berhasil ditambahkan!")
def delete_data():
    id_hapus = input("Masukkan ID data yang ingin dihapus: ")
    query = "DELETE FROM penjualan WHERE id_transaksi = %s"
    cursor.execute(query, (id_hapus,))
    db.commit()
    print("Data berhasil dihapus!")
def filter_data():
    print("\n=== FILTER DATA ===")
    filter_choice = input("Filter berdasarkan kategori (y/n)? ")
    if filter_choice.lower() == 'y':
        kategori = input("Masukkan kategori: ")
        query = f"SELECT * FROM penjualan WHERE kategori = '{kategori}'"
        df = pd.read_sql(query, db)
        print(df)
    else:
        print("Filter tidak diterapkan.")

    
def manage_data():
    while True:
        print("\n=== MENU DATA ===")
        print("1. Tambah Data")
        print("2. Hapus Data")
        print("3. Filter Data")
        print("4. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            add_data()
        elif pilihan == "2":
            delete_data()
        elif pilihan == "3":
            filter_data()
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

# ===================== MENU =====================

def menu():
    while True:
        print("\n=== APLIKASI PENJUALAN TOKO ===")
        print("1. Lihat Data Penjualan")
        print("2. Lihat Statistik")
        print("3. Visualisasi Data")
        print("4. Kelola Data Penjualan")
        print("5. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            read_table()
        elif pilihan == "2":
            show_statistik()
        elif pilihan == "3":
            data_visualization()
        elif pilihan == "4":
            manage_data()
        elif pilihan == "5":
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("Pilihan tidak valid!")

# Jalankan program
menu()
import psycopg2

# Veritabanı bağlantısı
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",  # Kendi veritabanı ismini yazdıysan onu kullan
    user="postgres",
    password="sifre123"  # Kendi şifren
)

cursor = connection.cursor()

# SQL SELECT sorgusu
select_query = "SELECT * FROM users;"

# Sorguyu çalıştır
cursor.execute(select_query)

# Sonuçları al
rows = cursor.fetchall()

# Satırları yazdır
for row in rows:
    print(row)

# Bağlantıyı kapat
cursor.close()
connection.close()


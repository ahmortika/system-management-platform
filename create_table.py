import psycopg2

# Veritabanı bağlantı bilgileri
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",  # Eğer farklı bir veritabanı oluşturduysan adını buraya yaz
    user="postgres",
    password="sifre123"  # Şifreni ne yaptıysan buraya onu yaz
)

cursor = connection.cursor()

# Tablo oluşturma SQL komutu
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
"""

# SQL komutunu çalıştır
cursor.execute(create_table_query)

# Değişiklikleri kaydet
connection.commit()

# Bağlantıyı kapat
cursor.close()
connection.close()

print("Tablo başarıyla oluşturuldu.")


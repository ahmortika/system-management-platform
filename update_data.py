import psycopg2

# Veritabanı bağlantısı
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="sifre123"  # Kendi şifren
)

cursor = connection.cursor()

# Güncellenecek veri
new_email = "ahmtsngll@hotmail.com"
name_to_update = "Ahmet Şengül"

# SQL UPDATE sorgusu
update_query = """
    UPDATE users
    SET email = %s
    WHERE name = %s;
"""

# Sorguyu çalıştır
cursor.execute(update_query, (new_email, name_to_update))

# Değişiklikleri kaydet
connection.commit()

print("Kullanıcının e-posta adresi güncellendi.")

# Bağlantıyı kapat
cursor.close()
connection.close()


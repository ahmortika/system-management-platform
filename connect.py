import psycopg2

# Bağlantı bilgilerini buraya yazıyoruz
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",  # varsayılan veritabanı
    user="postgres",
    password="sifre123"  # kendi belirlediğin şifre
)

# Cursor nesnesi ile sorgular gönderilir
cursor = connection.cursor()

# Basit bir SQL sorgusu çalıştırıyoruz
cursor.execute("SELECT version();")

# Sonuçları al
db_version = cursor.fetchone()
print("Veritabanı versiyonu:", db_version)

# Bağlantıyı kapat
cursor.close()
connection.close()


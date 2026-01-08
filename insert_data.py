import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="sifre123"
)

cursor = connection.cursor()

# Yeni kullanıcı verileri
users = [
    ("Cagri Sengül", "cagri.sngll@hotmail.com"),
    ("Baris Sengul", "bariscansss@hotmail.com"),
    ("Fahri Sensöz", "fahri.sensöz@gmail.com")
]

# Her kullanıcı için INSERT sorgusu çalıştır
for name, email in users:
    insert_query = "INSERT INTO users (name, email) VALUES (%s, %s);"
    cursor.execute(insert_query, (name, email))

# Değişiklikleri kaydet
connection.commit()

print("Yeni kullanıcılar başarıyla eklendi.")

cursor.close()
connection.close()


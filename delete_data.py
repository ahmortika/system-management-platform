import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="sifre123"
)

cursor = connection.cursor()

# Silmek istediğimiz e-posta
email_to_delete = "bariscansss@hotmail.com"

# DELETE sorgusu
delete_query = "DELETE FROM users WHERE email = %s;"
cursor.execute(delete_query, (email_to_delete,))

# Değişiklikleri kaydet
connection.commit()

print(f"{cursor.rowcount} kullanıcı silindi.")

cursor.close()
connection.close()


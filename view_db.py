import sqlite3

conn = sqlite3.connect('smartpick.db')
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Show users
cursor.execute("SELECT * FROM users;")
print("\nUsers:", cursor.fetchall())

# Show movie history
cursor.execute("SELECT * FROM user_movies;")
print("\nMovie History:", cursor.fetchall())

# Show grocery basket
cursor.execute("SELECT * FROM user_basket;")
print("\nGrocery Basket:", cursor.fetchall())

conn.close()
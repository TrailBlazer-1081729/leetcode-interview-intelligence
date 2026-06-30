import sqlite3

conn = sqlite3.connect("leetcode.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*), MAX(company_id) FROM companies")
print(cursor.fetchone())

conn.close()
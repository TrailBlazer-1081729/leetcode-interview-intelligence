import hashlib
from database.db import get_connection
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username,password):
    conn=get_connection()
    cursor=conn.cursor()
    hashed_pass=hash_password(password)
    try:
        cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
                       (username,hashed_pass))
        conn.commit()
        return "Signup successful"
    except:
        return "Username already exists"
    finally:
        conn.close()

def login_user(username,password):
    conn=get_connection()
    cursor=conn.cursor()

    hashed_pass=hash_password(password)
    cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?",
                   (username,hashed_pass))
    user=cursor.fetchone()
    conn.close()
    if user:
        return user[0]
    return None

if __name__ == "__main__":
    print(create_user("navin", "12345"))
    print(login_user("navin", "12345"))
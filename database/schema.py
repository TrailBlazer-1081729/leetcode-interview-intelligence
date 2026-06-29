from database.db import get_connection
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS problems(problem_id SERIAL PRIMARY KEY ,
    title TEXT UNIQUE NOT NULL,
    difficulty TEXT NOT NULL,
    frequency REAL,
    acceptance_rate REAL,
    leetcode_link TEXT)
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS companies(company_id SERIAL PRIMARY KEY ,
    name TEXT UNIQUE NOT NULL)
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS problem_companies(
    problem_id INTEGER,
    company_id INTEGER,
    PRIMARY KEY(problem_id,company_id),
    FOREIGN KEY(problem_id) REFERENCES problems(problem_id),
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS topics(
    topic_id SERIAL PRIMARY KEY ,
    name TEXT UNIQUE NOT NULL)
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS problem_topics(
    problem_id INTEGER,
    topic_id INTEGER,
    PRIMARY KEY(problem_id,topic_id),
    FOREIGN KEY(problem_id) REFERENCES problems(problem_id),
    FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
    )
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY ,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL)
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_solved_problems(
    user_id INTEGER,
    problem_id INTEGER,
    PRIMARY KEY(user_id,problem_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(problem_id) REFERENCES problems(problem_id)
    ) 
    """)

    conn.commit()
    conn.close()
    print("Data base schema created ")

if __name__ == "__main__":
    create_tables()
from database.db import get_connection
def mark_solved(user_id,problem_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""INSERT OR IGNORE INTO user_solved_problems(user_id,problem_id) VALUES(?,?)""",
                   (user_id,problem_id))
    conn.commit()
    conn.close()
def unmark_solved(user_id, problem_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM user_solved_problems
    WHERE user_id=? AND problem_id=?
    """, (user_id, problem_id))

    conn.commit()
    conn.close()
def get_solved(user_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""SELECT problem_id
    FROM user_solved_problems
    WHERE user_id=?""",(user_id,))
    solved=[row[0] for row in cursor.fetchall()]
    conn.close()
    return solved

def sync_solved_problems(user_id, selected_problem_ids):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM user_solved_problems
    WHERE user_id = ?
    """, (user_id,))

    for problem_id in selected_problem_ids:
        cursor.execute("""
        INSERT INTO user_solved_problems(user_id, problem_id)
        VALUES (?, ?)
        """, (user_id, problem_id))

    conn.commit()
    conn.close()



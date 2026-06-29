from database.db import get_connection
def mark_solved(user_id,problem_id):
    conn=get_connection()
    cursor=conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO user_solved_problems(user_id,problem_id) VALUES(%s,%s) ON CONFLICT DO NOTHING""",
            (user_id, problem_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        conn.close()

def unmark_solved(user_id, problem_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM user_solved_problems
            WHERE user_id=%s AND problem_id=%s
            """, (user_id, problem_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        conn.close()
def get_solved(user_id):
    conn=get_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("""SELECT problem_id
            FROM user_solved_problems
            WHERE user_id=%s""", (user_id,))
    except Exception as e:
        conn.rollback()
        print(e)
    solved=[row[0] for row in cursor.fetchall()]
    conn.close()
    return solved

def sync_solved_problems(user_id, selected_problem_ids):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM user_solved_problems
            WHERE user_id = %s
            """, (user_id,))
    except Exception as e:
        conn.rollback()
        print(e)


    for problem_id in selected_problem_ids:
        try:
            cursor.execute("""
                    INSERT INTO user_solved_problems(user_id, problem_id)
                    VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (user_id, problem_id))
        except Exception as e:
            conn.rollback()
            print(e)

    conn.commit()
    conn.close()



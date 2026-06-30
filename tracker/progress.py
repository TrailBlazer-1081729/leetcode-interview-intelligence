from database.db import get_connection
def sync_solved_problems(user_id, selected_problem_ids, visible_problem_ids):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM user_solved_problems
            WHERE user_id = %s AND problem_id = ANY(%s)
        """, (user_id, visible_problem_ids))

        for problem_id in selected_problem_ids:
            cursor.execute("""
                INSERT INTO user_solved_problems(user_id, problem_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (user_id, problem_id))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)

    finally:
        conn.close()



import sqlite3
from database.db import get_connection
from psycopg2.extras import execute_values


SQLITE_DB_PATH = "leetcode.db"   # Change if needed


def migrate_table(sqlite_cursor, pg_cursor, pg_conn, table_name, columns):
    print(f"\nMigrating {table_name}...")

    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    if not rows:
        print(f"{table_name}: No rows")
        return

    columns_str = ",".join(columns)

    query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES %s
        ON CONFLICT DO NOTHING
    """

    batch_size = 1000

    try:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]

            execute_values(
                pg_cursor,
                query,
                batch,
                page_size=batch_size
            )

            pg_conn.commit()

            print(
                f"{table_name}: inserted {min(i + batch_size, len(rows))}/{len(rows)} rows"
            )

        print(f"{table_name}: migration completed")

    except Exception as e:
        pg_conn.rollback()
        print(f"Error in {table_name}: {e}")
        raise


def migrate():
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()

    pg_conn = get_connection()
    pg_cursor = pg_conn.cursor()

    try:
        migrate_table(
            sqlite_cursor,
            pg_cursor,
            pg_conn,
            "companies",
            ["company_id", "name"]
        )

        migrate_table(
            sqlite_cursor,
            pg_cursor,
            pg_conn,
            "problems",
            [
                "problem_id",
                "title",
                "difficulty",
                "frequency",
                "acceptance_rate",
                "leetcode_link"
            ]
        )

        migrate_table(
            sqlite_cursor,
            pg_cursor,
            pg_conn,
            "topics",
            ["topic_id", "name"]
        )

        migrate_table(
            sqlite_cursor,
            pg_cursor,
            pg_conn,
            "problem_companies",
            ["problem_id", "company_id"]
        )

        migrate_table(
            sqlite_cursor,
            pg_cursor,
            pg_conn,
            "problem_topics",
            ["problem_id", "topic_id"]
        )

        migrate_table(
            sqlite_cursor,
            pg_cursor,
            pg_conn,
            "users",
            ["user_id", "username", "password"]
        )

        migrate_table(
            sqlite_cursor,
            pg_cursor,
            pg_conn,
            "user_solved_problems",
            ["user_id", "problem_id"]
        )

        print("\nMigration completed successfully")

    except Exception as e:
        print("\nMigration failed:", e)

    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == "__main__":
    migrate()
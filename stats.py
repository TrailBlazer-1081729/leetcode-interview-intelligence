from database.db import get_connection
def get_dashboard_stats():
    conn=get_connection()
    cursor=conn.cursor()
    stats={}
    cursor.execute("SELECT COUNT(*) FROM problems")
    stats["total_questions"]=cursor.fetchone()[0]

    cursor.execute("select count(*) from companies")
    stats["total_companies"]=cursor.fetchone()[0]

    cursor.execute("select count(*) from problems where difficulty='EASY'")
    stats["easy"]=cursor.fetchone()[0]

    cursor.execute("select count(*) from problems where difficulty='MEDIUM'")
    stats["medium"] = cursor.fetchone()[0]

    cursor.execute("select count(*) from problems where difficulty='HARD'")
    stats["hard"] = cursor.fetchone()[0]

    conn.close()
    return stats

def get_all_companies():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select name from companies order by name")
    companies=[row[0] for row in cursor.fetchall()]
    conn.close()
    return companies
def get_all_topics():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select name from topics order by name")
    topics=[row[0] for row in cursor.fetchall()]
    conn.close()
    return topics


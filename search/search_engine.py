
from database.db import get_connection
from tracker.progress import get_solved
def search(company=None,topic=None,difficulty=None,limit=50,user_id=None,show_solved=False):
    conn=get_connection()
    cursor=conn.cursor()
    query="""SELECT DISTINCT
    p.problem_id,
    p.title,
    p.difficulty,
    p.frequency,
    p.leetcode_link
    FROM problems p
    JOIN problem_companies pc on p.problem_id=pc.problem_id
    JOIN companies c on pc.company_id=c.company_id
    JOIN problem_topics pt on p.problem_id=pt.problem_id
    JOIN topics t on pt.topic_id=t.topic_id
    WHERE 1=1
    """

    params=[]

    if user_id is not None and show_solved==False:
        query +="""
        AND p.problem_id NOT IN (
        SELECT problem_id
        FROM user_solved_problems
        WHERE user_id=?)"""
        params.append(user_id)
    if company:
        query+=" AND c.name = ?"
        params.append(company)
    if topic:
        query+=" AND t.name= ?"
        params.append(topic)
    if difficulty:
        query+=" AND p.difficulty= ?"
        params.append(difficulty)

    query+="""ORDER BY COALESCE(p.frequency,0) DESC LIMIT ?"""
    params.append(limit)
    cursor.execute(query,params)
    results=cursor.fetchall()
    conn.close()
    solved_ids = set()

    if user_id:
        solved_ids = get_solved(user_id)

    return results,solved_ids



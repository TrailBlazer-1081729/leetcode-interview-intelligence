import os
import pandas as pd
from database.db import get_connection
Problems="../data/problems"
def ingest_data():
    conn=get_connection()
    cursor=conn.cursor()
    company_folders=os.listdir(Problems)
    for company in company_folders:
        company_path=os.path.join(Problems,company)
        if not os.path.isdir(company_path):
            print(f"not able to process {company}")
            continue
        csv_file=None
        for file in os.listdir(company_path):
            if file.endswith("All.csv"):
                csv_file=file
                break
        if csv_file is None:
            print("skip")
            continue

        csv_path=os.path.join(company_path,csv_file)
        print(f"Processing {company}")
        df=pd.read_csv(csv_path)
        for _,row in df.iterrows():
            
            title=row["Title"]
            difficulty=row["Difficulty"]
            frequency=row["Frequency"]
            acceptance=row["Acceptance Rate"]
            link=row["Link"]
            if pd.isna(row["Topics"]):
                topics = []
            else:
                topics = row["Topics"].split(",")
                topics = [topic.strip() for topic in topics]

            insert_company(cursor,company)
            insert_problem(cursor,title,difficulty,frequency,acceptance,link)
            company_id=get_company_id(cursor,company)
            problem_id=get_problem_id(cursor,title)
            insert_problem_company(cursor,problem_id,company_id)
            for topic in topics:
                insert_topic(cursor,topic)
                topic_id=get_topic_id(cursor,topic)
                insert_problem_topic(cursor,problem_id,topic_id)
        conn.commit()
    conn.close()

def insert_company(cursor,company):

    cursor.execute("""INSERT INTO companies(name)
    VALUES (%s)
    ON CONFLICT(name) DO NOTHING""",(company,))
def insert_problem(cursor,title,difficulty,frequency,acceptance,link):

    cursor.execute("""INSERT INTO problems(title,difficulty,frequency,acceptance_rate,leetcode_link) VALUES(%s,%s,%s,%s,%s) ON CONFLICT(title) DO NOTHING""",(title,difficulty,frequency,acceptance,link))

def get_company_id(cursor,company):

    cursor.execute("SELECT company_id FROM companies WHERE name=%s",(company,))
    return cursor.fetchone()[0]

def get_problem_id(cursor,title):

    cursor.execute("SELECT problem_id from problems WHERE title=%s",(title,))
    return cursor.fetchone()[0]

def insert_problem_company(cursor,problem_id,company_id):

    cursor.execute("""INSERT INTO problem_companies(problem_id,company_id) VALUES(%s,%s)
ON CONFLICT(problem_id, company_id) DO NOTHING""",(problem_id,company_id))

def insert_topic(cursor,topic):

    cursor.execute("""INSERT INTO topics(name)
VALUES(%s)
ON CONFLICT(name) DO NOTHING""",(topic,))

def get_topic_id(cursor,topic):

    cursor.execute("SELECT topic_id from topics WHERE name=%s",(topic,))
    return cursor.fetchone()[0]

def insert_problem_topic(cursor,problem_id,topic_id):

    cursor.execute("""INSERT INTO problem_topics(problem_id,topic_id) VALUES(%s,%s)
    ON CONFLICT(problem_id, topic_id) DO NOTHING""",(problem_id,topic_id))


ingest_data()
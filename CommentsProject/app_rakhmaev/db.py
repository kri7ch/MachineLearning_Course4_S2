import mysql.connector
from mysql.connector import Error


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="230606",
        database="comments_ml",
    )


def fetch_comments():
    query = "SELECT id, text, is_toxic, created_at FROM comments ORDER BY id DESC;"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                result = {"id": [], "text": [], "is_toxic": [], "created_at": []}
                for row in rows:
                    result["id"].append(row[0])
                    result["text"].append(row[1])
                    result["is_toxic"].append(row[2])
                    result["created_at"].append(row[3].isoformat() if row[3] is not None else None)
                return result
    except Error as e:
        raise e


def insert_comment(text: str, is_toxic: int):
    query = "INSERT INTO comments (text, is_toxic) VALUES (%s, %s);"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (text, is_toxic))
                conn.commit()
    except Error as e:
        raise e


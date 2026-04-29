from fastapi import FastAPI
from pymongo import MongoClient
import mysql.connector
import os

app = FastAPI()

#Mongo
mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client["blog_db"]

#MySQL
mysql_conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

@app.get("/posts")
def get_posts():
    posts = list(mongo_db.posts.find({}, {"_id": 0}))
    return posts

@app.get("/users")
def get_users():
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateurs")
    return cursor.fetchall()

@app.get("/health")
def health():
    try:
        mongo_db.posts.count_documents({})
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT 1")
        return {"status": "OK"}
    except:
        return {"status": "ERROR"}
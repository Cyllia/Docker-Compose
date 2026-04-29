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
    try:
        if not mysql_conn.is_connected():
            mysql_conn.reconnect(attempts=3, delay=2)
            
        # Ajoute buffered=True ici
        cursor = mysql_conn.cursor(dictionary=True, buffered=True) 
        cursor.execute("SELECT * FROM utilisateurs")
        result = cursor.fetchall()
        
        cursor.close() # Très important pour libérer la connexion
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    try:
        mongo_db.posts.count_documents({})
        # Utilise un curseur contextuel pour garantir la fermeture
        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone() # On lit le résultat pour vider le flux
        return {"status": "OK"}
    except Exception:
        return {"status": "ERROR"}
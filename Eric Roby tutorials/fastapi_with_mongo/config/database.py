from pymongo import MongoClient
client = MongoClient("mongodb+srv://anuragsingh1921:yzb6h6csvr3SFDlq@cluster0.gz7nl3l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = client.todo_db

collection_name = db["todo_collection"]
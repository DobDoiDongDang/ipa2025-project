from pymongo import MongoClient
import os

mongo_url = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("DB_NAME")
client = MongoClient(mongo_url)
mydb = client[mongo_db]
mycol = mydb["routers"]


def get_data(router_ip):
    return mycol.find_one({"ip": router_ip})

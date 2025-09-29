from pymongo import MongoClient
import datetime
import os

mongo_url = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("DB_NAME")
client = MongoClient(mongo_url)
mydb = client[mongo_db]
mycol = mydb["interface_status"]


def save_interface(router_ip, data):
    mycol.insert_one(
        {
            "router_ip": router_ip,
            "timestamp": str(datetime.datetime.now()),
            "interfaces": data,
        }
    )

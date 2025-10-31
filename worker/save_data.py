from pymongo import MongoClient
import datetime
import os
from bson import ObjectId

mongo_url = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("DB_NAME")
client = MongoClient(mongo_url)
mydb = client[mongo_db]
mycol = mydb["interface_status"]
myconf = mydb["config"]


def save_interface(router_ip, int_data, routing):
    print("saved")
    mycol.insert_one(
        {
            "router_ip": router_ip,
            "timestamp": str(datetime.datetime.now()),
            "interfaces": int_data,
            "routing": routing
        }
    )


def save_config(idx):
    myconf.update_one({"_id": ObjectId(idx)}, {"$set": {"status": "yah"}})

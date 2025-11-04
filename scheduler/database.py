import os
from bson import json_util
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

mongo_uri = os.environ.get("MONGO_URI")
#mongo_uri = "mongodb://mongo:mongo@localhost:27017/"
db_name = os.environ.get("DB_NAME")
print(mongo_uri, db_name)
client = MongoClient(mongo_uri)
db = client[db_name]


def get_router_info():
    routers = db["routers"]
    router_data = routers.find()
    return router_data


def get_router_config():
    config = db["config"]
    config_data = config.find({"status": "nah"})
    return config_data


if __name__ == "__main__":
    print("start")
    try:
        for i in get_router_info():
            print(i)
            data = json_util.dumps(i)
            print(data)
    except Exception as e:
        print("error",e)

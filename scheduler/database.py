import os
from pymongo import MongoClient
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")
client = MongoClient(mongo_uri)
db = client[db_name]
def get_router_info():
    routers = db["routers"]
    router_data = routers.find()
    return router_data

def get_router_config():
    config = db["config"]
    config_data = config.find({ "status" : "nah" })
    return config_data    

if __name__ == "__main__":
    get_router_info()

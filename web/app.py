from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

import os

mongo_url = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("DB_NAME")
client = MongoClient(mongo_url)
mydb = client[mongo_db]
myint = mydb["interface_status"]
mycol = mydb["routers"]
myconf = mydb["config_int"]
print(f"MONGO_URL {mongo_url}")
print(f"MONGO_DB {mongo_db}")


app = Flask(__name__)


@app.route("/")
def main():
    data = []
    for x in mycol.find():
        data.append(x)
    return render_template("index.html", data=data)


@app.route("/router/<ip>")
def router_details(ip):
    data = myint.find({"router_ip": ip})
    lastest_data = list(data.sort("timestamp", -1).limit(1))
    router_list = []
    for x in mycol.find():
        router_list.append(x)
    return render_template("router_detail.html", ip=ip, data=lastest_data, router_list=router_list)


@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    if ip and username and password:
        mycol.insert_one({"ip": ip, "username": username, "password": password})
    return redirect("/")


@app.route("/delete/<idx>", methods=["POST"])
def delete_router(idx):
    try:
        mycol.delete_one({"_id": ObjectId(idx)})
    except Exception:
        pass
    return redirect(url_for("main"))

@app.route("/config/<ip>", methods=["POST"])
def config_interface(ip):
    interface_list = []
    idx = 0
    while True:
        if not request.form.get(f"interface {idx}"):
            break
        interface_list.append({
            "interface" : request.form.get(f"interface {idx}"), 
            "ip" : request.form.get(f"ip {idx}"), 
            "subnet" : request.form.get(f"subnet {idx}"),
            "status" : request.form.get(f"status {idx}"),
            "description" : request.form.get(f"description {idx}")
        })
        idx += 1
    print(interface_list)
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId
import pymongo

import os

mongo_url = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("DB_NAME")
client = MongoClient(mongo_url)
mydb = client[mongo_db]
myint = mydb["interface_status"]
mycol = mydb["routers"]
myconf = mydb["config"]
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
    data = myint.find_one(
        {
            "router_ip": ip,
        },
        sort=[("created_at", pymongo.DESCENDING)],
    )
    router_list = []
    for x in mycol.find():
        router_list.append(x)
    return render_template(
        "router_detail.html",
        ip=ip,
        router_list=router_list,
        timestamp=data.get("timestamp").split(".")[0],
        interface=data.get("interfaces"),
    )


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
    config_list = []
    data = myint.find({"router_ip": ip})
    lastest_data = myint.find_one(
        {
            "router_ip": ip,
        },
        sort=[("created_at", pymongo.DESCENDING)],
    )
    for i in lastest_data["interfaces"]:
        idx = i["index"]
        changed = False
        if i["ip_address"] != request.form.get(f"ip {idx}"):
            changed = True
        if i["subnet"] != request.form.get(f"subnet {idx}"):
            changed = True
        if (i["status"]) != request.form.get(f"status {idx}"):
            changed = True
        if i["description"] != request.form.get(f"description {idx}"):
            changed = True
        if changed:
            interface_list.append(
                {
                    "interface": request.form.get(f"interface {idx}"),
                    "ip": request.form.get(f"ip {idx}"),
                    "subnet": request.form.get(f"subnet {idx}"),
                    "status": request.form.get(f"status {idx}"),
                    "description": request.form.get(f"description {idx}"),
                }
            )
    if interface_list:
        myconf.insert_one({"ip": ip, "task": "config_interfaces", "status": "nah", "data": interface_list})
    return redirect(url_for(f"router_details", ip=ip))


@app.route("/add_loopback/<ip>", methods=["POST"])
def add_loopback(ip):
    interface = {
            "interface": request.form.get(f"interface"), 
            "ip": request.form.get(f"ip"),
            "subnet": request.form.get(f"subnet"),
            "status": request.form.get(f"status"),
            "description": request.form.get(f"description"),
            }
    myconf.insert_one({"ip": ip, "task": "add_loopback", "status": "nah", "data": interface})
    return redirect(url_for("router_details", ip=ip))

@app.route("/del_loopback/<ip>", methods=["POST"])
def del_loopback(ip):
    data = request.get_json()
    myconf.insert_one({"ip": ip, "task": "del_loopback", "status": "nah", "data":{"interface": data["interface"]}})
    return redirect(url_for("router_details", ip=ip))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

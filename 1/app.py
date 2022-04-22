from flask import Flask, jsonify, render_template
import requests
import json
import logging
import socket

app = Flask(__name__)

def main(debug=False):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    if debug == True:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    return ip_address

@app.get("/api/countries")
def get_countries():
    logger.info(f"opening file")
    with open('salary_data.json') as local_file:
        local_data_list = json.load(local_file)["array"]
    logger.info(f"returned type {type(local_data_list)}")
    
    logger.info(f"request: get users data from api")
    response = requests.get("http://jsonplaceholder.typicode.com/users")
    api_data_list = response.json()
    logger.info(f"response: {response.status_code}")

    logger.info(f"request: get conv coef")
    response = requests.get("https://free.currconv.com/api/v7/convert?q=IDR_USD&compact=ultra&apiKey=1cdb35f5174a7c09bfbc")
    conv_coef = response.json()["IDR_USD"]
    logger.info(f"response: {response.status_code}")

    logger.info(f"Processing data")
    for i in range(len(api_data_list)):
        logger.info(f"get user salary by id")
        salary_idr = next((local_data['salaryInIDR'] for local_data in local_data_list if local_data["id"] == api_data_list[i]["id"]), None)
        logger.info(f"salary: {salary_idr}")

        logger.info(f"adding salary")
        api_data_list[i]['salary_idr'] = salary_idr
        api_data_list[i]['salary_usd'] = salary_idr*conv_coef
        logger.info(f"salary for id {api_data_list[i]['id']} added")

        logger.info(f"pop website & company")
        api_data_list[i].pop('website', None)
        api_data_list[i].pop('company', None)
    logger.info(f"Done Processing data")
    return jsonify(api_data_list)

@app.get("/countries")
def render_countries():
    response = requests.get(f"http://{ip_address}:5000/api/countries")
    return render_template("countries.html", data=response.json())

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    ip_address = main(debug=False)
    app.run(host="0.0.0.0", port=5000, use_reloader=True)
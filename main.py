from flask import Flask, jsonify, request
from flask_caching import Cache
from app.utils.response import process_token
from colorama import init
import warnings
from urllib3.exceptions import InsecureRequestWarning
import time
from dotenv import load_dotenv
import os
import logging

load_dotenv()



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ignore SSL warnings
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# Initialize Flask app
app = Flask(__name__)



cache = Cache(app, config={"CACHE_TYPE": "simple"})  # In-memory cache

@app.route("/")
def home():
    return "JWT Token Generator API is running!"

@app.route("/token", methods=["GET"])
async def get_responses():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if uid and password:

        response = process_token(uid, password)
        status_code=int(response.get("status_code", 500))
        region =response.get("server","NONE")
        level=response.get("level","NONE")
        nickname=response.get("nickname","NONE")
        accountID =response.get("account_id","NONE")
        if status_code == 200:
            try:
                level_int = int(level)
            except:
                level_int = 0



        # cache.set(
        #     cache_key, response, timeout=3600
        # )  
        return jsonify(response),status_code
    
            
    # Bulk retrieval logic removed as per request
    return jsonify({"message": "Bulk retrieval logic has been removed."})


if __name__ == "__main__":
    port =5002
    app.run(host="0.0.0.0", port=port )

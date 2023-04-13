import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# client = MongoClient('mongodb://randhyar955:Ardiansyah955@ac-xeuzkcq-shard-00-00.vr2df0r.mongodb.net:27017,ac-xeuzkcq-shard-00-01.vr2df0r.mongodb.net:27017,ac-xeuzkcq-shard-00-02.vr2df0r.mongodb.net:27017/?ssl=true&replicaSet=atlas-krshns-shard-0&authSource=admin&retryWrites=true&w=majority')
# db = client.dbrandhyar955
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

# @app.route("/bucket", methods=["POST"])
# def bucket_post():
#     sample_receive = request.form['sample_give']
#     print(sample_receive)
#     return jsonify({'msg': 'POST /bucket request!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    # sample_receive = request.form['sample_give']
    num_receive = request.form['num_give']
    db.buketlist.update_one(
        {'num' : int(num_receive)},
        {'$set' : {'done' : 1}}
    )
    return jsonify({'msg' : 'update done !'})

@app.route("/bucket/delet", methods=["POST"])
def bucket_delet() :
    num_delete = request.form['num_hapus']
    db.buketlist.delete_one(
        {'num' : int(num_delete)}
    )
    return jsonify({'msg' : 'delete !'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list =list(db.buketlist.find({},{'_id' : False}))
    return jsonify({'buckets': bucket_list})

# Server tidak membutuhkan informasi tambahan dari client. Server akan merespon setiap request GET dan ke dalam url /bucket dengan membaca semua item bucket list dari database dan dikembalikan ke pada client. 
@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.buketlist.count_documents({})
    num = count + 1
    delet = num - 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0,
        'delet' : 0        
    }
    db.buketlist.insert_one(doc)
    return jsonify({'msg':'data saved!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
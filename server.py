from flask import Flask,Response,request
from bson.objectid import ObjectId
from pymongo import MongoClient
import json



client = MongoClient('localhost', 27017)
db = client['movies']
movies_collection = db['movies']

app = Flask(__name__)

@app.route("/")
def root():
    return Response(
        response = json.dumps({'message':'Welcome to movies db collection'}),
        status = 200,
        mimetype = 'application/json')

@app.route("/movie/add",methods=['POST'])
def add_movie():
    split_starring = request.form['movie_starring'].split(',')
    movie = {"movie_name": request.form['movie_name'], "movie_director":request.form['movie_director'], "movie_starring": split_starring}
    db_response = movies_collection.insert_one(movie)
    return Response(
        response = json.dumps({'id':f'{db_response.inserted_id}'}),
        status = 201,
        mimetype = 'application/json')

@app.route("/movie/all",methods=['GET'])
def get_all_movies():
    movies_list = list(movies_collection.find())
    for movie in movies_list:
        movie['_id'] = str(movie['_id'])
    return Response(
        response = json.dumps(movies_list),
        status = 200,
        mimetype = 'application/json')

@app.route("/movie/<id>",methods=['PATCH'])
def update_movie_director(id):
    movie_director = request.form['movie_director']
    db_response = movies_collection.update_one(
        {'_id':ObjectId(id)},
        {'$set':{'movie_director':movie_director}})
    if db_response.modified_count >= 1:
        return Response(
        response = json.dumps({'message':f'updated {db_response.modified_count} documents(s)'}),
        status = 200,
        mimetype = 'application/json')
    else:
        return Response(
        response = json.dumps({'message':f'updated {db_response.modified_count} documents(s)'}),
        status = 200,
        mimetype = 'application/json')

@app.route("/movie/<id>",methods=['DELETE'])
def delete_movie(id):
    db_response = movies_collection.delete_one({'_id':ObjectId(id)})
    if db_response.deleted_count >= 1:
        return Response(
        response = json.dumps({'message':f'deleted {db_response.deleted_count} documents(s)'}),
        status = 200,
        mimetype = 'application/json')
    else:
        return Response(
        response = json.dumps({'message':f'deleted {db_response.deleted_count} documents(s)'}),
        status = 200,
        mimetype = 'application/json')

if __name__ == "__main__":
    app.run(port=8082,debug=True) 
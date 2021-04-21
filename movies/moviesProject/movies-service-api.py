from flask import Flask, json
import pandas as pd
from movies.moviesProject.algorithm import Algorithm
from movies.moviesProject.mongoService import MongoAPI
import os
os.getcwd()
import sys
sys.path.append('c:/dev/movies-project-py/movies')

api = Flask(__name__)


@api.route('/loadAllMovies', methods=['GET'])
def loadAllData():
    data = {
        "database": "movies",
        "collection": "movies",
    }
    mongo_obj = MongoAPI(data)
    try:
        allMovies = pd.read_csv("movies.csv")
        movieIds = allMovies.movieId
        titles = allMovies.title
        genres = allMovies.genres
        mongo_obj.deleteAll()
        for i in range(len(movieIds)):
            item = {"movieId": str(movieIds.values[i]), "title": titles[i], "genres": genres[i]}
            mongo_obj.insert_one(item)
        # Back to main collection predictedMovies
        data['collection'] = "predictedMovies";
        mongo_obj = MongoAPI(data);
        return 'Success'
    except ValueError:
        print("An exception occurred")
        return 'Failed to upload data Please check the integrity of your file' + ValueError


@api.route('/runAlogrithm', methods=['GET'])
def getMoviesRest():
    try:
        Algorithm.getMoviesBy_Recommender_Matrix_Factrization(mongo_obj)
        return 'The new data was successfully added to DB!!'
    except:
        return 'Exception'
        print("An exception occurred")


@api.route('/getAllMovies', methods=['GET'])
def getAllMovies():
    try:
        list = mongo_obj.read();
        return json.dumps(list);
    except:
        print("An exception occurred")
        return 'Failed to read data!'


@api.route('/getMovieById/<id>', methods=['GET'])
def getMovieById(id):
    try:
        list = mongo_obj.readById(id);
        return json.dumps(list);
    except:
        print("An exception occurred")
        return 'Failed to read data!'


if __name__ == '__main__':
    data = {
        "database": "movies",
        "collection": "predictedMovies",
    }
    mongo_obj = MongoAPI(data)
    # print(json.dumps(mongo_obj.read(), indent=4))
    api.run()

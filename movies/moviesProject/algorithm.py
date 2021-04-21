import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from flask import Flask, json
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Embedding, Input
from keras.layers import Reshape
from keras.layers import Dot
from keras.layers import Dense
from keras.layers import Concatenate
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot


# from keras.utils import plot_modelimport pydot
class Algorithm():
    @staticmethod
    def getMoviesBy_Recommender_Matrix_Factrization(mongoObj):
        ratings = pd.read_csv("ratings.csv")
        ratings.drop('timestamp', axis=1, inplace=True)
        X = ratings.iloc[:, :2]
        Y = ratings.iloc[:, 2]
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=66)
        user_id_input_layer = Input(shape=[1], name='user_input')
        movie_id_input_layer = Input(shape=[1], name='movie_input')

        latent_factors = 32
        user_embeddings = Embedding(input_dim=len(ratings.userId.unique()) + 1, output_dim=latent_factors,
                                    input_length=1, name='user_embedding')(user_id_input_layer)
        movie_embedding = Embedding(output_dim=latent_factors, input_dim=ratings.movieId.max() + 1,
                                    input_length=1, name='movie_embedding')(movie_id_input_layer)

        user_vecs = Reshape([latent_factors])(user_embeddings)
        movie_vecs = Reshape([latent_factors])(movie_embedding)

        concatenate = Concatenate()([user_vecs, movie_vecs])
        dense = Dense(128, activation='relu')(concatenate)
        dot_layer = Dense(1)(dense)

        model = Model(inputs=[user_id_input_layer, movie_id_input_layer], outputs=dot_layer)

        model.compile(loss='mse',
                      optimizer="adam"
                      )
        model.fit([x_train['userId'], x_train['movieId']], y_train, batch_size=128, epochs=1,
                  validation_data=([x_test['userId'], x_test['movieId']], y_test))
        userIdList = x_train['userId'].values.tolist()
        movieIdList = x_train['movieId'].values.tolist()
        # Delete all collection before inserting the new data
        mongoObj.deleteAll();
        for i in range(len(userIdList)):
            item = {"userId": userIdList[i], "movieId": movieIdList[i]}
            mongoObj.insert_one(item)

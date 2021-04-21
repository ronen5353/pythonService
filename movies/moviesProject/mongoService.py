import movies
from flask import Flask, request, json, Response
from pymongo import MongoClient


class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb://localhost:27017/")

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def readById(self, id):
        outPut = self.readById(id)
        return outPut;

    def insert_one(self, data):
        # log.info('Writing Data')
        new_document = data
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def insert_many(self, list):
        response = self.collection.insert_many(list)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self, updateData):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updateData)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def deleteAll(self):
        self.collection.drop();
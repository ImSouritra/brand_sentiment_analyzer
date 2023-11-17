from pymongo import MongoClient



class MongoDatabase:
    def __init__(self, database_name, connection_string):
        self.database_name = database_name
        self.connection_string = connection_string

    def get_database(self):
        client = MongoClient(self.connection_string)
        return client[self.database_name]

    def get_collection(self,database, collection_name):
        return database[collection_name]


    def is_user_db_exist(self, collection , userName):
        if collection.find_one(filter={"user_name":userName}):
            return True
        else:
            return False


    def is_brand_db_exist(self, collection, brandName):
        if collection.find_one(filter={"brand_name" : brandName}):
            return True
        else:
            return False


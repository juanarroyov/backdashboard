from pymongo import MongoClient
from bson.objectid import ObjectId
from local_config import pymongo_host_uri, pymongo_database

class Mongo:
    ''' 
    La clase recibe la colleccion y crea el objeto.
    La base de datos esta definida por defecto (api_admin)
    '''
    #Nombre de base de datos tiene mismo nombre que id_cliente
    def __init__(self, collection):
        self.client = MongoClient(pymongo_host_uri)

        database = pymongo_database
        cursor = self.client[database]
        instance_colleccion = cursor[collection]

        collection_list = cursor.list_collection_names()
        '''
        Modificacion para crear la Coleccion en caso de que no exista, ya que genera errores al implementar nuevos ambientes.
        '''
        if collection in collection_list:
            self.collection = cursor[collection]
            self.data = collection

        else:
            instance_colleccion.insert_one({})
            instance_colleccion.remove({})
            self.collection = instance_colleccion
            self.data = collection
        return 

#Esta clase es para instanciar y conectarse a la base de datos de xentric donde se encontraran los clientes, usuarios y funciones de la plataforma
class MongoXentric:

    def __init__(self, collection):
        self.client = MongoClient(pymongo_host_uri)

        database = pymongo_database
        cursor = self.client[database]
        instance_colleccion = cursor[collection]

        collection_list = cursor.list_collection_names()
        '''
        Modificacion para crear la Coleccion en caso de que no exista, ya que genera errores al implementar nuevos ambientes.
        '''
        if collection in collection_list:
            self.collection = cursor[collection]
            self.data = collection

        else:
            instance_colleccion.insert_one({})
            instance_colleccion.remove({})
            self.collection = instance_colleccion
            self.data = collection
        return 




    def find(self, query):
        ''' 
        La funcion recibe la consulta en formato json y retorna el resultado.
        '''
        return self.collection.find(query)

    def find_by_id(self, _id):
        ''' 
        La funcion recibe y buscar por el id y retorna el resultado.
        '''
        return self.collection.find_by_id({"_id": ObjectId(_id)})

    def find_one(self, query):
        ''' 
        La funcion recibe la consulta en formato json y retorna solo un elemento.
        '''
        return self.collection.find_one(query)

    def insert_one(self, document):
        ''' 
        La funcion recibe el documento (json) y lo ingresa a la base de datos.
        '''        
        return self.collection.insert_one(document)

    def inser_many(self, array_document):
        ''' 
        La funcion recibe los documentos (array de json) y los ingresa a la base de datos.
        '''
        return self.collection.inser_many(array_document)

    def update_by_id(self, _id, newvalues):
        ''' 
        La funcion busca por id y actualiza los valores.
        '''
        return self.collection.update_one({"_id": ObjectId(_id)}, newvalues)

    def update_one(self, query, newvalues):
        ''' 
        La funcion recibe la consulta y actualiza un documento.
        '''
        return self.collection.update_one(query, newvalues)

    def update_many(self, query, newvalues):
        ''' 
        La funcion recibe la consulta y actualiza varios documentos.
        '''
        return self.collection.update_many(query, newvalues)

    def delete_by_id(self, _id):
        ''' 
        La funcion busca por id y elimina el documento.
        '''
        return self.collection.delete_one({"_id": ObjectId(_id)})

    def delete_one(self, query):
        ''' 
        La funcion busca el documento y lo elimina.
        '''
        return self.collection.delete_one(query)

    def delete_many(self, query):
        ''' 
        La funcion recibe la consulta y elimina los documentos.
        '''
        return self.collection.delete_many(query)



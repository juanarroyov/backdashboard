import pymongo
from pymongo import IndexModel, ASCENDING, DESCENDING
from bson import json_util
from bson.objectid import ObjectId
from pprint import pprint
from db import Mongo
from v1.utils.paginated_list import get_paginated_list

global Mongo

class BotsModel:
    #Instancia coleccion y carga
    def __init__(self, valores_unicos=[]):
        self.coleccion = Mongo('API_BOTS').collection
        #Elimina todos los indices al instanciarce la api
        self.coleccion.drop_indexes()
        #Se le crea un indice a los campos con valores unicos para que lanze error cuando se ingrese un valor repetido.
        if valores_unicos:
            for campo in valores_unicos:
                self.coleccion.create_index([(campo, ASCENDING)], unique=True)
    
    def post(self, cliente, fecha_creacion, fecha_modificacion, recurso):
        
        #!si id de bot se repite tirar error
        #return False, 'El nombre del bot que eligió ya existe.'
        id_bot = recurso["id_bot"]
        documento = {"cliente":cliente, "fecha_creacion":fecha_creacion, "fecha_modificacion":fecha_modificacion, "id_bot":id_bot, "bot": recurso}
        self.coleccion.insert_one(documento)
        return True, ''

    def get(self, cliente, id_bot, url=None, start=None, limit=None):

        if id_bot:
            valid=True; error=''
            recurso = self.coleccion.find_one({'cliente':cliente, 'id_bot':id_bot}, {'_id':0, 'cliente':0})        
            if not recurso:
                valid=False
                error = 'No se encontró el bot identificado como "'+id_bot+'". Asegurese de llamar un valor que ya exista.'
            return recurso, valid, error        
        else:
            recurso = self.coleccion.find({'cliente':cliente}, {'_id':0, 'cliente':0})      
            resultado = get_paginated_list(recurso, url, start, limit)
            return resultado

    def exist_id(self, cliente, id_bot):
        recurso = self.coleccion.find_one({'cliente':cliente, 'id_bot':id_bot}, {'_id':1})  
        return bool(recurso)    

    def rename_id(self, cliente, id_bot, id_new):
        self.coleccion.update_one({'cliente':cliente, 'id_bot':id_bot}, {'$set': {'id_bot':id_new}})
        return

    def get_fecha_creacion(self, cliente, id_bot):
        dato = self.coleccion.find_one({'cliente':cliente, 'id_bot':id_bot}, {'_id':0, 'fecha_creacion':1})
        fecha = dato['fecha_creacion']
        return fecha        

    def delete(self, cliente, id_bot):
        valid=True; error=''
        if id_bot:
            result = self.coleccion.delete_one({'cliente':cliente, 'id_bot':id_bot})
            if not result.deleted_count:
                valid=False
                error = 'No se encontró el bot identificado como "'+id_bot+'". Asegurese de llamar un valor que ya exista.'
            return valid, error
        else:
            result = self.coleccion.delete_many({'cliente':cliente})
            deleted_count = result.deleted_count
            if not deleted_count:
                valid=False
                error='No existen recursos para ser borrados.'
                return valid, error
            return valid, deleted_count


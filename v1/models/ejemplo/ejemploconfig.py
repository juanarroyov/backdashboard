import pymongo
from pymongo import IndexModel, ASCENDING, DESCENDING
from bson import json_util
from bson.objectid import ObjectId
from pprint import pprint
from db import Mongo
from v1.utils.paginated_list import get_paginated_list

global Mongo

class Ejemploodel:
    #Instancia coleccion y carga
    def __init__(self, valores_unicos=[]):
        self.coleccion = Mongo('API_EJEMPLO').collection
        #Elimina todos los indices al instanciarce la api
        self.coleccion.drop_indexes()
        #Se le crea un indice a los campos con valores unicos para que lanze error cuando se ingrese un valor repetido.
        if valores_unicos:
            for campo in valores_unicos:
                self.coleccion.create_index([(campo, ASCENDING)], unique=True)
    
    def post(self, duracion, fecha_creacion, recurso):
        
        #!si id de bot se repite tirar error
        #return False, 'El nombre del bot que eligió ya existe.'
        id_ejemplo = recurso["id_ejemplo"]
        documento = {"duracion":duracion, "fecha_creacion":fecha_creacion,  "id_ejemplo":id_ejemplo, "bot": recurso}
        self.coleccion.insert_one(documento)
        return True, ''

    def get(self, duracion, id_ejemplo, url=None, start=None, limit=None):

        if id_ejemplo:
            valid=True; error=''
            recurso = self.coleccion.find_one({'duracion':duracion, 'id_ejemplo':id_ejemplo}, {'_id':0, 'duracion':0})        
            if not recurso:
                valid=False
                error = 'No se encontró el bot identificado como "'+id_ejemplo+'". Asegurese de llamar un valor que ya exista.'
            return recurso, valid, error        
        else:
            recurso = self.coleccion.find({'duracion':duracion}, {'_id':0, 'duracion':0})      
            resultado = get_paginated_list(recurso, url, start, limit)
            return resultado

    def exist_id(self, duracion, id_ejemplo):
        recurso = self.coleccion.find_one({'duracion':duracion, 'id_ejemplo':id_ejemplo}, {'_id':1})  
        return bool(recurso)    

    def rename_id(self, duracion, id_ejemplo, id_new):
        self.coleccion.update_one({'duracion':duracion, 'id_ejemplo':id_ejemplo}, {'$set': {'id_ejemplo':id_new}})
        return

    def get_fecha_creacion(self, duracion, id_ejemplo):
        dato = self.coleccion.find_one({'duracion':duracion, 'id_ejemplo':id_ejemplo}, {'_id':0, 'fecha_creacion':1})
        fecha = dato['fecha_creacion']
        return fecha        

    def delete(self, duracion, id_ejemplo):
        valid=True; error=''
        if id_ejemplo:
            result = self.coleccion.delete_one({'duracion':duracion, 'id_ejemplo':id_ejemplo})
            if not result.deleted_count:
                valid=False
                error = 'No se encontró el bot identificado como "'+id_ejemplo+'". Asegurese de llamar un valor que ya exista.'
            return valid, error
        else:
            result = self.coleccion.delete_many({'duracion':duracion})
            deleted_count = result.deleted_count
            if not deleted_count:
                valid=False
                error='No existen recursos para ser borrados.'
                return valid, error
            return valid, deleted_count


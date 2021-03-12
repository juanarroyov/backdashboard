from datetime import datetime
import hashlib
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
import json
from db import Mongo
from v1.models.conversaciones.conversaciones_config import ConversacionModel




#Modelo de datos para configuracion de bots
#campos_unicos = campos_con_valores_unicos(configuracion)
mongo_conversacion = ConversacionModel()


#curl en windows
#curl -X POST http://localhost:5000/bot -d "{\"id_bot\":\"config_4\",\"first_line_names\":true,\"fields_list\":[{\"field_name\":\"telefono\",\"datatype\":\"int\",\"fieldtype\":\"phone\",\"config_phone\":{\"prefix\":\"\",\"digits\":0},\"skip\":false},{\"datatype\":\"string\",\"fieldtype\":\"user\",\"skip\":false},{\"field_name\":\"fecha\",\"datatype\":\"datetime\",\"fieldtype\":\"other\",\"skip\":false},{\"field_name\":\"\",\"datatype\":\"string\",\"fieldtype\":\"other\",\"skip\":false}],\"file_format\":\"csv\",\"file_codec\":\"utf-8\",\"delimiter\":\";\"}"
class Conversacion(Resource):
    
    def post(self, id_conversacion=None, fecha=None, llamada=None):
        duracion = 'duracion_test' #Cliente debe salir de los datos de autentificacion
        #Recuperar argumentos de json en body del request
        argumentos = request.get_json(force=True)
        
        '''if id_bot: argumentos['id_bot'] = id_bot
        #Validar argumentos. Agregar los que son por default        
        recurso, valid, error = validar(configuracion, argumentos)'''
        
        #Valida campos obligatorios de configuracion
        valid, error = check_fieldlist(argumentos)
        #Retornar error si existe
        if not valid:
            return {"message": error}, 400

        recurso = argumentos
        #Crear y guardar recurso en base de datos
        #cliente, id_bot, numero, fecha_creacion, fecha_modificacion, recurso
        fecha_created = datetime.now() if not fecha else fecha
        fecha_mod = datetime.now()
        valid, error = mongo_conversacion.post(duracion=duracion, fecha=fecha, recurso=recurso,)
        if not valid:
            return {"message": error}, 400
        #Devolver datos del recurso creado.
        return recurso
        

    def get(self, id_conversacion):
        url = request.base_url
        args = request.args
        duracion = 'duracion_test'
        #Si existe un id la funcion retorna la configuracion correspondiente a esa lista 
        if id_conversacion:
            #validar que existe id_bot en la base de datos
            #retornar valores
            recurso, valid, error = mongo_conversacion.get(duracion, id_conversacion)
            if not valid:
                return {"message": error}, 400
            return jsonify(recurso)
        #! Si no existe id la funcion retorna todas las configuraciones de lista.
        #! Intentar usar paginacion.
        else:
            url = request.base_url
            args = request.args
            start = args['start'] if 'start' in args else 1
            limit = args['limit'] if 'limit' in args else 10
            fechaInicio = args['fechaInicio'] if 'fechaInicio' in args else None
            fechaTermino = args['fechaTermino'] if 'fechaTermino' in args else None
            #Al poner id_bot como None retorna toda los bots.
            results = mongo_conversacion.get(duracion, None, url, start, limit, fechaInicio, fechaTermino)        
            return jsonify(results)
   
          
    def put(self, id_conversacion):
        duracion = 'duracion_test'
        if not id_conversacion: 
            return {"message": "Debe agregar id del bot en la url."}, 400
        exist_idconfig = mongo_conversacion.exist_id(duracion, id_conversacion)
        if not exist_idconfig:
            return {"message": "No existe el id del bot que desea actualizar."}, 400
        #id existe
        #encontrar fecha de creacion
        fecha = mongo_conversacion.get_fecha(duracion, id_conversacion)
        #hash de id_bot
        id_conversacion_tmp = hashlib.sha1(id_conversacion.encode()).hexdigest()
        #remplazar id_bot en la base por el hash
        mongo_conversacion.rename_id(duracion, id_conversacion, id_conversacion_tmp)
        recurso = self.post(id_conversacion=id_conversacion, fecha=fecha)
        #!si configuracion no es valida enviar mensaje de error
        #!si actualizacion fue correcta, eliminar recurso temporal y retornar recurso con fechas de creacion y modificacion
        self.delete(id_conversacion_tmp)
        return recurso

        
    def delete(self, id_conversacion):
        duracion = 'duracion_test'
        #Si existe un id la funcion elimina la configuracion de lista del id 
        if id_conversacion:
            #validar que existe id_bot en la base de datos
            #eliminar recurso
            valid, error = mongo_conversacion.delete(duracion, id_conversacion)
            if not valid:
                return {"message": error}, 400
            return {"message": 'El bot "'+id_conversacion+'" fue eliminado.'}, 200
        #Si no existe id la funcion retorna todas las configuraciones de lista
        else:
            valid, error = mongo_conversacion.delete(duracion, id_conversacion)
            if not valid:
                return {"message": error}, 200
            else:
                deleted_count = error
                return {"message": 'Todos los bots fueron eliminados.', "deleted_count":deleted_count}, 200
        

def check_fieldlist(argumentos):
    valid=True; errores = ''
    if not "id_conversacion" in argumentos:
        valid = False
        errores = 'Debe agregar el id del bot.'

    return valid, errores
    

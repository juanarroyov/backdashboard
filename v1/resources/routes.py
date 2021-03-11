from .bots.bots import Bots
from .conversaciones.conversacion import Conversacion
from .ejemplo.ejemplo import Ejemplo


def initialize_routes(api):
    

    #Endpoints Api Bots    
    api.add_resource(Bots,'/bot', endpoint='bots_all', defaults={'id_bot': None},  methods=['GET','DELETE'])
    api.add_resource(Bots, '/bot', endpoint='bot_post', methods=['POST',])    
    api.add_resource(Bots,'/bot/<id_bot>', endpoint='bot_one',  methods=['GET', 'PUT', 'DELETE'])
    api.add_resource(Conversacion,'/conversacion', endpoint='conversacion_all', defaults={'id_conversacion': None},  methods=['GET','DELETE'])
    api.add_resource(Conversacion, '/conversacion', endpoint='conversacion_post', methods=['POST',])
    api.add_resource(Ejemplo,'/ejemplo', endpoint='ejemplo_all', defaults={'id_ejemplo': None},  methods=['GET','DELETE'])
    api.add_resource(Ejemplo, '/ejemplo', endpoint='ejemplo_post', methods=['POST',])   

    return

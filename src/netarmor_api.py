from enum import Enum
from tg import decode_params, expose, AppConfig
import tg
from tg.controllers import RestController, TGController
from tg.decorators import with_trailing_slash
from wsgiref.simple_server import make_server

def _get_exposed_func(func):
    @with_trailing_slash
    @expose()
    @decode_params("json")
    def exposed_func(self, *args, **kwards):
        return {"data" : func(*args, **kwards)}
    return exposed_func

class Endpoint(Enum):
    GET=1
    POST=2

def _allow_access_control(*args, **kwargs):
    tg.response.headers.update({'Access-Control-Allow-Origin': '*',
                                    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                                    'Access-Control-Allow-Methods' : 'GET, POST, PUT'})

class App:
    def __init__(self) -> None:
        self.endpoints = {}
    
    def register_endpoint(self, path:str, func, endpoint:Endpoint):
        path = str(path)
        path = path.split("/")
        path = [i for i in path if i != ""] 
        current_level = self.endpoints
        for level in path:
            if level not in current_level:
                current_level[level] = {}
            current_level = current_level[level]
        current_level[endpoint] = _get_exposed_func(func)


    def _create_controller(self, name, endpoint_level, base_type=RestController):
        endpoint_dict = {
            "_before" : _allow_access_control
        }
        if Endpoint.GET in endpoint_level:
            endpoint_dict["get"] = endpoint_level[Endpoint.GET]
            del endpoint_level[Endpoint.GET]
        if Endpoint.POST in endpoint_level:
            endpoint_dict["post"] = endpoint_level[Endpoint.POST]
            del endpoint_level[Endpoint.POST]

        endpoint_type = type("tg_" + name, (base_type, ), endpoint_dict)

        for endpoint_label in endpoint_level:
            controller = self._create_controller(endpoint_label, endpoint_level[endpoint_label])
            setattr(endpoint_type, endpoint_label, controller)
        return endpoint_type()
    
    def run(self, host, port, sql_alchemy_database_url= None, model_bunch=None):
        root_controller = self._create_controller("root", self.endpoints, TGController)
        config = AppConfig(minimal=True, root_controller=root_controller)
        if sql_alchemy_database_url is not None:
            config['use_sqlalchemy'] = True
            config['sqlalchemy.url'] = sql_alchemy_database_url
        if model_bunch is not None:
            config["model"] = model_bunch
        application = config.make_wsgi_app()
        httpd = make_server(host, port, application)
        httpd.serve_forever()
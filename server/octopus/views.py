from pyramid.view import view_config
import octopus_functions as o
from pymongo import *
from json import *

tmpl = "templates/"


@view_config(renderer="templates/servers.pt", route_name="home")
def index_view(request):
        nodes = o.retrieve_nodes_crud()
        logs = o.retrieve_logs_crud()
        return {"nodes":nodes,"logs":logs}

@view_config(renderer="string",name="cadastrar")
def cadastrar_view(request):
	r = o.insert_crud(request.json_body)
	return r

@view_config(renderer="string",name="output")
def output_view(request):
	r = o.insert_logs_crud(request.json_body)
	return r

@view_config(renderer="json", name="comando")
def comando_view(request):	
	a = request.json_body
	r = o.comandos(a)
	return r



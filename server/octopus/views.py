from pyramid.view import view_config
import octopus_functions as o
from pymongo import *
from json import *
import json

tmpl = "templates/"


@view_config(renderer="templates/servers.pt", route_name="home")
def index_view(request):
        s = o.retrieve_servers_crud("data")
        return {'servidores':s}

@view_config(renderer="string",name="cadastrar")
def cadastrar_view(request):
	print str(request.json_body)
	return "OK"

@view_config(renderer="string",name="output")
def output_view(request):
	print str(request.json_body)
	return "OK"

@view_config(renderer="string", name="teste")
def output_view(request):
	res = o.retorno_dict()
	return res

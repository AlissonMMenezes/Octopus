from pyramid.security import remember, forget, authenticated_userid
#from .models import pages
from .security import USERS
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, forbidden_view_config
import octopus_functions as o
from pymongo import *
from json import *

tmpl = "templates/"


class OctopusWeb(object):
	def __init__(self, request):
		self.request = request
		self.logged_in = authenticated_userid(request)

	@view_config(renderer="templates/servers.pt", route_name="home", permission='admin')
	def index_view(self):
		nodes = o.retrieve_nodes_crud()
		logs = o.retrieve_logs_crud()
		feet = o.retrieve_feet_crud()

		return {"nodes":nodes,"logs":logs,"feet":feet}

	@view_config(renderer="string",name="cadastrar")
	def cadastrar_view(self):
		request = self.request
		r = o.insert_crud(request.json_body)
		return r

	@view_config(renderer="json",name="new_group")
	def novo_grupo_view(self):
		request = self.request
		r = o.insert_grupo_crud(request.json_body)
		return r
	@view_config(renderer="json",name="delete_group")
	def delete_group_view(self):
		request = self.request
		data = request.json_body
		r = o.delete_group_crud(data)
		return r

	@view_config(renderer="templates/grupos.pt",name="grupos", permission="admin")
	def grupos_view(self):
		nodes = o.retrieve_nodes_crud()
		return {"nodes":nodes}

	@view_config(renderer="templates/feet.pt",name="feet", permission="admin")
	def feet_view(self):
		feet = o.retrieve_feet_crud()
		return {"feet":feet}

	@view_config(renderer="string",name="output")
	def output_view(self):
		request = self.request
		r = o.insert_logs_crud(request.json_body)
		return r

	@view_config(renderer="json", name="comando")
	def comando_view(self):	
		request = self.request
		a = request.json_body
		r = o.comandos(a)
		return r

	@view_config(renderer="json", name="find_foot")
	def find_foot_view(self):	
		request = self.request
		data = request.json_body
		r = o.find_foot_crud(data)
		return r

	@view_config(renderer="json", name="add_foot")
	def add_foot_view(self):	
		request = self.request
		data = request.json_body
		r = o.add_foot_crud(data)
		return r

	@view_config(renderer="templates/login.pt", route_name='login')
	@forbidden_view_config(renderer='templates/login.pt')
	def login(self):
	    request = self.request
	    login_url = request.route_url('login')
	    referrer = request.url
	    if referrer == login_url:
	            referrer = '/'
	    came_from = "/"
	    message = ''
	    login = ''
	    password = ''
	    if 'form.submitted' in request.params:
	            login = request.params['login']
	            password = request.params['password']
	            if USERS.get(login) == password:
	                    headers = remember(request, login)
	                    return HTTPFound(location=came_from, headers=headers)
	            message = "Failed login"

	    return dict(
	            title="Login",
	            message=message,
	            url=request.application_url+'/login',
	            came_from=came_from,
	            login=login,
	            password=password,
	    )


	@view_config(route_name='logout')
	def logout(self):
		request = self.request
		headers = forget(request)
		url = request.route_url('login')
		return HTTPFound(location=url,
						headers=headers)

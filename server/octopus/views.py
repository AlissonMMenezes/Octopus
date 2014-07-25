#
# Octopus - IT Automation Tool
# Coded by: Alisson Menezes
#		- alisson.copyleft@gmail.com
#		
# Date: 29/04/2014
#
# Rotas e templates
# Indice referente as funcoes do sistema 
# x00 - Configuracoes
# x01 - Servers
# x02 - Grupos
# x03 - Feet
# x04 - Nodes
# x05 - Virtualizacao
# x06 - Bacula
# x07 - Login


from pyramid.security import remember, forget, authenticated_userid
from .security import USERS
from pyramid.httpexceptions import HTTPFound

from pyramid.renderers import get_renderer
from pyramid.view import view_config, forbidden_view_config
import octopus_functions as o
import octopus_virt as v
from pymongo import *
from json import *
import json



tmpl = "templates/"


class OctopusWeb(object):
	#x00 Configs da autenticacao
	def __init__(self, request):
		self.request = request
		self.logged_in = authenticated_userid(request)

	#x00 Configs do Layout -
	def site_layout(self):
		renderer = get_renderer("templates/base.pt")
		layout = renderer.implementation().macros['base']
		return layout
	#x00 - Fim  das configuracoes -

	#x01 - Pagina principal -
	@view_config(renderer="templates/servers.pt", route_name="home", permission='admin')
	def index_view(self):
		nodes = o.retrieve_nodes_crud()
		logs = o.retrieve_logs_crud()
		feet = o.retrieve_feet_crud()
		return {"nodes":nodes,"logs":logs,"feet":feet,"layout":self.site_layout()}

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
	#x01 - Fim da sessao da pagina principal -

	#x02 - Grupos - 
	@view_config(renderer="templates/grupos.pt",name="grupos", permission="admin")
	def grupos_view(self):
		nodes = o.retrieve_nodes_crud()
		feet = o.retrieve_feet_crud()
		return {"layout":self.site_layout(),"nodes":nodes,"feet":feet}

	@view_config(renderer="json",name="new_group", permission="admin")
	def novo_grupo_view(self):
		request = self.request
		r = o.insert_grupo_crud(request.json_body)
		return r

	@view_config(renderer="json",name="delete_group", permission="admin")
	def delete_group_view(self):
		request = self.request
		data = request.json_body
		r = o.delete_group_crud(data)
		return r

	@view_config(renderer="json",name="add_foot_to_group", permission="admin")
	def add_foot_to_group_view(self):
		request = self.request
		r = o.add_foot_to_group(request.json_body)
		return r

	@view_config(renderer="json",name="remove_foot_from_group", permission="admin")
	def remove_foot_from_group_view(self):
		request = self.request
		r = o.remove_foot_from_group(request.json_body)
		return r
	#x02 - Fim da sessao de grupos

	#x03 - Feet -
	@view_config(renderer="templates/feet.pt",name="feet", permission="admin")
	def feet_view(self):
		feet = o.retrieve_feet_crud()
		return {"layout":self.site_layout(),"feet":feet}

	@view_config(renderer="json", name="find_foot", permission="admin")
	def find_foot_view(self):	
		request = self.request
		data = request.json_body
		r = o.find_foot_crud(data)
		return r

	@view_config(renderer="json", name="add_foot",permission="admin")
	def add_foot_view(self):	
		request = self.request
		data = request.json_body
		r = o.add_foot_crud(data)
		return r

	#x03 - Fim da sessao de Feet -
	
	#x04 - Nodes -
	@view_config(renderer="templates/nodes.pt",name="nodes", permission="admin")
	def nodes_view(self):
		nodes = o.retrieve_nodes_crud()
		feet = o.retrieve_feet_crud()
		return {"layout":self.site_layout(),"nodes":nodes, "feet":feet}
	
	@view_config(renderer="json",name="node_info", permission="admin")
	def node_info_view(self):
		request = self.request
		print request.json_body
		node = o.retrieve_node_info(request.json_body)
		return node


	@view_config(renderer="string",name="cadastrar")
	def cadastrar_view(self):
		request = self.request
		r = o.insert_crud(request.json_body)
		return r	

	@view_config(renderer="json",name="delete_foot", permission="admin")
	def delete_foot_view(self):
		request = self.request
		data = request.json_body
		r = o.delete_foot_crud(data)
		return r

	@view_config(renderer="json",name="add_foot_to_node", permission="admin")
	def add_foot_to_node_view(self):
		request = self.request
		r = o.add_foot_to_node(request.json_body)
		return r
	# x04 - Fim da sessao de Nodes -	

	#x05 - Virtualizacao - 
	@view_config(renderer="templates/virt.pt", name="virt",permission="admin")
	def virt_view(self):	
		request = self.request
		AllVms = v.get_Vms()
		return {"layout":self.site_layout(),"AllVms":AllVms}

	@view_config(renderer="json", name="vm_action",permission="admin")
	def vmaction_view(self):	
		request = self.request
		r = v.vm_action(request.json_body)
		return r
	
	@view_config(renderer="json", name="access_console",permission="admin")
	def vmconsole_view(self):	
		request = self.request
		r = v.access_console(request.json_body)
		print r
		return r

	@view_config(renderer="json", name="get_networks",permission="admin")
	def getnetworks_view(self):	
		request = self.request
		r = v.get_networks(request.json_body)
		return r

	#x05 - Fim da Sessao de Virtualizacao

	#x06 - Bacula -
	@view_config(renderer="templates/bacula.pt", name="bacula",permission="admin")
	def bacula_view(self):	
		request = self.request
		return {"layout":self.site_layout()}
	#x06 - Fim da Sessao da bacula -
	
	#x07 - Login -
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
	#x07 - Fim da Sessao de Login
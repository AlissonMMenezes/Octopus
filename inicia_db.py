#!/usr/bin/python
#
# Script para criar estrutura do banco de dados
#
# Por: Alisson Menezes
#
#

from pymongo import *

print "[+] Conectando com o banco de dados"
client = MongoClient('localhost',27017)
db = client["octopus"]
print "[+] Conectado ..."
print "[+] Criando estrutura do banco"
db.nodes.update({ "_id":"default", "feet":[], "nodes":[]},{ "_id":"default", "feet":[], "nodes":[]}, upsert=True)
print "[+] Estrutura criada!"
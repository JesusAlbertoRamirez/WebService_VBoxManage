#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess
import json

app = Flask(__name__)

lista = []

# 'VBoxManage list vms'
# curl -i http://localhost:5000/listarvm
#
@app.route('/listvm', methods=['GET'])
def get_vmListas():
 bashCommand = ['VBoxManage', 'list', 'vms']
 salida = subprocess.run( bashCommand, check=True, stdout=subprocess.PIPE).stdout
 salida = salida.decode('utf-8')
 # Elimina los caracteres indicados del string
 salida = salida.replace('\\', '').replace('\'', '').replace('\"', '')
 lista = salida.split() # El metodo .split() crea una lista en la que cada palabra es un elemento del String 
 dicionario = dict(lista[i:i+2] for i in range(0, len(lista), 2)) # Convierte una lista en un dict
 if len(dicionario) <= 1:
      dicionario = "No hay maquinas virtuales creadas."
 return jsonify({'vms': dicionario})

# 'VBoxManage list vms'
# curl -i http://localhost:5000/runningvm
#
@app.route('/runningvm', methods=['GET'])
def get_runing():
	output = subprocess.check_output(['VBoxManage', 'list' , 'runningvms'])
	str = output.decode('utf-8').splitlines()
	return jsonify({'list': str})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

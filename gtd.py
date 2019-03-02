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

# 'VBoxManage list runningvms'
# curl -i http://localhost:5000/runningvm
#
@app.route('/runningvm', methods=['GET'])
def get_runing():
 bashCommand = ['VBoxManage', 'list' , 'runningvms']
 salida = subprocess.run( bashCommand, check=True, stdout=subprocess.PIPE).stdout
 salida = salida.decode('utf-8').split()
 return jsonify({'running': salida})

# 'VBoxManage showvminfo'
# curl -i http://localhost:5000/infovm/<name vm>
#
@app.route('/infomv/<string:namevm>')
def showvminfo(namevm):
 bashCommand = ['VBoxManage', 'showvminfo', namevm ]
 salida = subprocess.run( bashCommand, check=True, stdout=subprocess.PIPE).stdout
 salida = salida.decode('utf-8').split()
 return jsonify({'infomv': salida})

# 'VBoxManage showvminfo'
# curl -i http://localhost:5000/infovm/<name vm>
#
@app.route('/vms/ram/<string:vm>')
def ram(vm):
 output = subprocess.Popen(['vboxmanage', 'showvminfo', vm ], stdout = subprocess.PIPE)
 tail = subprocess.check_output(['grep', 'Memory'], stdin = output.stdout)
 str = tail.decode('utf-8').splitlines()
 return jsonify({'list': str})

# 'VBoxManage showvminfo'
# curl -i http://localhost:5000/infovm/<name vm>
#
@app.route('/vms/nic/<string:vm>')
def nic(vm):
 output = subprocess.Popen(['vboxmanage', 'showvminfo', vm ], stdout = subprocess.PIPE)
 holi = subprocess.Popen(['grep', 'NIC'], stdin = output.stdout, stdout = subprocess.PIPE)
 tail = subprocess.Popen(['grep', 'MAC'], stdin = holi.stdout, stdout = subprocess.PIPE)
 out = subprocess.check_output(['wc', '-l'], stdin = tail.stdout).decode('utf-8')
 return jsonify({'list': out})

# 'vboxmanage', 'modifyvm', vm, '--cpus' , cpu 
# curl -i http://localhost:5000/infovm/<name vm>
#
@app.route('/vms/modifiy/<string:vm>/<string:cpu>')
def modif(vm, cpu):
 subprocess.run(['vboxmanage', 'modifyvm', vm, '--cpus' , cpu ])

 return "Se cambio a la maquina virtual "

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

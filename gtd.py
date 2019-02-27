#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess

app = Flask(__name__)

lista = {}

@app.route('/listar', methods=['GET'])
def get_vmListas():
 bashCommand = ['VBoxManage', 'list', 'vms']
 salida = subprocess.run( bashCommand, check=True, stdout=subprocess.PIPE).stdout
 print(salida)

 return jsonify({'listas': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

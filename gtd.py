
#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess
import vboxapi

app = Flask(__name__)

cmd_vmlist  = 'VBoxManage list vms'

tasks = [
 {
  'id': 1,
  'title': "Buy groceries",
  'description': "Milk, cheese, pizaa",
  'done': False
 },
 {
  'id': 2,
  'title': "Learn Python",
  'description': "Need a good tutorial on the web",
  'done': False
 }
]



@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
 return jsonify({'tasks': tasks})

@app.route('/listar', methods=['GET'])
def get_vmListas():
 virtualBoxManager = vboxapi.VirtualBoxManager(None, None)
 vbox = virtualBoxManager.vbox
 vboxVMList = virtualBoxManager.getArray(vbox, 'machines')
 salida = subprocess.call(["VBoxManage", "list", "vms"],shell = True)
 print(vboxVMList)

 return jsonify({'listas': salida})

@app.route('/')
def saludo():
	return "hola mundo"

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
 task = [task for task in tasks if task['id'] == task_id]
 if len(task) == 0:
  abort(404)
 return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
 if not request.json or not 'title' in request.json:
  abort(400)
 task = {
  'id': tasks[-1]['id'] + 1,
  'title': request.json['title'],
  'description': request.json.get('description', ""),
  'done': False
 }
 tasks.append(task)
 return jsonify({'task': task}), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

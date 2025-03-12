from flask import Flask, request, jsonify
from models.task import task

app = Flask(__name__)

tasks = []
taskIdControl = 1

# Post (endpoint: tasks)
@app.route("/tasks", methods=['POST'])
def createTask():
    global taskIdControl
    data = request.get_json()
    newTask = task(id=taskIdControl, title=data.get("title"), description=data.get("description", ""))
    taskIdControl += 1
    tasks.append(newTask)
    print(tasks)
    return jsonify({"mensagem": "Nova Tarefa criada com sucesso"})

@app.route("/tasks", methods=['GET'])
def getTasks():
    taskList = [task.to_dict() for task in tasks]

    if len(tasks) > 0:
        output={
            "tasks": taskList,
            "total_tasks": len(taskList)
        }
        return jsonify(output)
    
    return jsonify({"mensagem": "Nenhuma tarefa registrada na lista ainda"})

@app.route("/tasks/<int:id>", methods=['GET'])
def getTask(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"mensagem": "Não foi possível encontrar a atividade"}), 404

@app.route("/tasks/<int:id>", methods=['PUT'])
def updateTask(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    print(task)
    if task == None:
        return jsonify({"mensagem": "Não foi possível encontrar a atividade"}), 404

    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]
    print(task)
    return jsonify({"mensagem": "Tarefa atualizada com sucesso"})

@app.route("/tasks/<int:id>", methods=['DELETE'])
def deleteTask(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    print(task)
    if task == None:
        return jsonify({"mensagem": "Não foi possível encontrar a atividade"}), 404
    
    tasks.remove(task)
    return jsonify({"mensagem": "Tarefa deletada com sucesso"})



if __name__ == "__main__":
    app.run(debug=True)
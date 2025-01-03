from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
task_id_control = 1

class Task:
    def __init__(self, id, title, description, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

    def to_dict(self):
        # Converte a tarefa para um dicionário que pode ser transformado em JSON
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

@app.route("/tasks", methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({"Message": "Nova Tarefa criada com sucesso"}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"Message": "Tarefa não encontrada"}), 404

@app.route("/tasks/<int:id>", methods=['PUT'])
def update_tasks(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break  # Encontramos a tarefa, podemos sair do loop
    if task is None:
        return jsonify({"Message": "Tarefa não encontrada"}), 404

    data = request.get_json()
    task.title = data.get("title", task.title)  # Se não enviar "title", mantém o valor atual
    task.description = data.get("description", task.description)  # Mesma lógica para description
    task.completed = data.get("completed", task.completed)  # Se não enviar "completed", mantém o valor atual

    return jsonify({"Message": "Tarefa atualizada com sucesso"}), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break  # Encontramos a tarefa, podemos sair do loop

    if task is None:
        return jsonify({"Message": "Tarefa não encontrada"}), 404

    tasks.remove(task)
    return jsonify({"Message": "Tarefa removida com sucesso"}), 200  # Código de status 200 OK

if __name__ == "__main__":
    app.run(debug=True)

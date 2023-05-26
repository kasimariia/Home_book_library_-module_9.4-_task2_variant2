import json

class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)["library"]
        except FileNotFoundError:
            self.todos = []

    def all(self):
        return self.todos

    def get(self, id):
        return self.todos[id - 1]  # тут змінила індексацію для відповідності списку зі списком в HTML шаблоні

    def create(self, data):
        data["id"] = len(self.todos) + 1  # створимо новий id
        data["done"] = False  # треба додати значення для done
        self.todos.append(data)
        self.save_all()

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump({"library": self.todos}, f)

    def update(self, id, data):
        self.todos[id - 1] = data  # для зміни індексації для відповідності списку зі списком в HTML шаблоні
        self.save_all()

    def delete(self, id):  #для видалення книги
        todo = self.get(id)
        if todo:
            self.todos.remove(todo)
            self.save_all()
            return True
        return False



todos = Todos()

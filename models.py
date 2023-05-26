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
        return self.todos[id - 1]  # Змінено індексацію для відповідності списку зі списком в HTML шаблоні

    def create(self, data):
        data["id"] = len(self.todos) + 1  # Генеруємо новий ID
        data["done"] = False  # Додаємо значення для done
        self.todos.append(data)
        self.save_all()

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump({"library": self.todos}, f)

    def update(self, id, data):
        self.todos[id - 1] = data  # Змінено індексацію для відповідності списку зі списком в HTML шаблоні
        self.save_all()

    def delete(self, id):
        todo = self.get(id)
        if todo:
            self.todos.remove(todo)
            self.save_all()
            return True
        return False



todos = Todos()

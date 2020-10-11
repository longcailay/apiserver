from flask import Flask
app = Flask(__name__)


#combobox chọn khu vực
from areas import areas
app.register_blueprint(areas)


if __name__ == "__main__":
    app.run()
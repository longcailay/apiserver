import sys
sys.path.insert(0,'./../Connection')

from flask import Flask
app = Flask(__name__)


#combobox chọn khu vực
from areas import areas
app.register_blueprint(areas)

#giao duc
from giaoDuc import giaoDuc
app.register_blueprint(giaoDuc)

if __name__ == "__main__":
    app.run()
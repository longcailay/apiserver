# import sys
# sys.path.insert(0,'./Connection')

from flask import Flask
app = Flask(__name__)
from flask_cors import CORS

#combobox chọn khu vực
from areas import areas
app.register_blueprint(areas)

# #giao duc
# from giaoDuc import giaoDuc
# app.register_blueprint(giaoDuc)

#api tìm boder khu vực
from boder import boder
app.register_blueprint(boder)

#utilities
from utilities import utilities
app.register_blueprint(utilities)

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True, use_reloader=True)

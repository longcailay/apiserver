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

#utilities
from utilities import utilities
app.register_blueprint(utilities)

if __name__ == "__main__":
    CORS(app)
    app.run(host='0.0.0.0',debug=True, use_reloader=True)

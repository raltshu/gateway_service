from flask import Flask
from handlers.predict_proxy import PredictView
from handlers.home_proxy import HomeView


app = Flask(__name__)


HomeView.register(app, route_base='/')
PredictView.register(app, route_base='/predict')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)


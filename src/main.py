from flask import Flask
from handlers.predict_proxy import PredictView
from handlers.home_proxy import HomeView
from handlers.data_proxy import DataView
from handlers.admin_proxy import AdminView
from handlers.alerts_proxy import AlertsView



app = Flask(__name__)


HomeView.register(app, route_base='/')
PredictView.register(app, route_base='/predict')
DataView.register(app, route_base='/data')
AdminView.register(app, route_base='/admin')
AlertsView.register(app, route_base='/alerts')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)


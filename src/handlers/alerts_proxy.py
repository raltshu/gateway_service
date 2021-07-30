from flask_classful import FlaskView, route
from flask import render_template, request
import pandas as pd
import os, requests

dataservice = os.environ['dataservice_endpoint']


class AlertsView(FlaskView):

    @route('/show_table/<string:table_name>', methods=['GET'])
    def show_table(self, table_name):
        limit = request.args.get('limit')
        order_by = request.args.get('order_by')
        order_asc_desc = request.args.get('order_asc_desc')
        response = requests.get(url=f"{dataservice}/data/table_view/{table_name}?limit={limit}&order_by={order_by}&order_asc_desc={order_asc_desc}")  
        df = pd.read_json(response.text)
        return render_template('alerts/alerts.html', data_table = df, 
            table_name=table_name, limit=limit, order_by=order_by, order_asc_desc=order_asc_desc)  

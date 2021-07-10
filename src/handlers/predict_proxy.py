from flask_classful import FlaskView, route
from flask import request,render_template

class PredictView(FlaskView):

    @route('/', methods=['GET'])
    def index(self):
        #TODO: Data service get first 20 lines for display
        return render_template('predict.html')
    
    @route('/', methods=['POST'])
    def submit_prediction(self):
        return render_template('predict.html')



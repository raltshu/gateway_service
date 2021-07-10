from flask_classful import FlaskView, route
from flask import request,render_template

class HomeView(FlaskView):

    def index(self):
        #TODO: Data service get first 20 lines for display
        print('Hello')
        return render_template('main.html')
    
    @route('/predict', methods=['GET'])
    def predict_view(self):
        return render_template('predict.html')



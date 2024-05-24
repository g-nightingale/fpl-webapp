from flask import Flask, request, render_template
import plotly.express as px
import pandas as pd
import sys
import os

# Hack to use relative imports
utils_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../utilities'))
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

# Now you can import the module from the parent directory
from dynamodb_helpers import get_data_from_dynamo_db


app = Flask(__name__)


def query_database_for_player(player_name):
    return player_name

@app.route('/')
def home():

    TABLE_NAME = 'player_points_predictions'
    REGION_NAME = 'eu-west-2'
    results_list = get_data_from_dynamo_db(TABLE_NAME, region_name=REGION_NAME)
    return render_template('home.html', data=results_list)

@app.route('/search', methods=['POST'])
def search():
    player_name = request.form['player_name']
    player_data = query_database_for_player(player_name)
    
    # Assuming 'player_data' is a DataFrame or can be converted into one
    if not player_data.empty:
        fig = create_plot(player_data)
        plot_html = fig.to_html()
        return render_template('search_results.html', plot_html=plot_html)
    else:
        return "Player not found.", 404

if __name__ == '__main__':
    # Load config dict
    # config = ut.load_config()
    # app.run(host=config['host'], port=config['port'], debug=config['debug'])
    app.run(host='0.0.0.0', port='5000', debug=True)
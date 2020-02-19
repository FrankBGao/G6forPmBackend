from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.util import sorting
from pm4py.visualization.dfg import factory as dfg_vis_fact
from pm4py.algo.discovery.dfg import factory as dfg_factory
from werkzeug.utils import secure_filename
from converter.SImplification import uselog, rewritelog

import converter.dfg_to_g6 as dfg_to_g6
import converter.SImplification

import os
import logging
from flask import jsonify, request, flash, Flask, redirect, send_from_directory, session, url_for

app = Flask(__name__)

url_top = "/server/api"
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

# log_path = os.path.join("exportedLog.xes")
# log = xes_import_factory.apply(log_path)
# log = sorting.sort_timestamp(log)

graph_data = []
current_log_file_name = ""

# dfg = dfg_factory.apply(log)
# this_data = dfg_to_g6.dfg_to_g6(dfg)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route(url_top + '/gain_graph', methods=['GET'])
def gain_graph():
    # dfg = dfg_factory.apply(log)
    # this_data = dfg_to_g6.dfg_to_g6(dfg)
    global graph_data
    return jsonify(graph_data)


UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['csv', 'xes'])


@app.route(url_top + '/upload', methods=['GET', 'POST'])
def fileUpload():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('./' + filename))

        this_data = uselog(os.path.join("./" + filename))
        global graph_data, current_log_file_name
        graph_data = this_data
        print(graph_data)
        current_log_file_name = filename
        return jsonify(this_data)

    return ''


@app.route(url_top + '/group', methods=['POST'])
def group_activity():
    if request.method == 'POST':
        global current_log_file_name,graph_data
        group = request.get_json()
        newlog = rewritelog(current_log_file_name, group)
        # dfg = dfg_factory.apply(newlog)
        # this_data = dfg_to_g6.dfg_to_g6(dfg)
        #
        # graph_data = this_data
        return jsonify(newlog)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host="0.0.0.0")

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.util import sorting
from pm4py.visualization.dfg import factory as dfg_vis_fact
from pm4py.algo.discovery.dfg import factory as dfg_factory

import converter.dfg_to_g6 as dfg_to_g6
import converter.SImplification

import os
from flask import jsonify, request, flash, Flask, redirect, send_from_directory

app = Flask(__name__)

url_top = "/server/api"

log_path = os.path.join("exportedlog.xes")
log = xes_import_factory.apply(log_path)
log = sorting.sort_timestamp(log)

# dfg = dfg_factory.apply(log)
# this_data = dfg_to_g6.dfg_to_g6(dfg)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route(url_top + '/gain_graph', methods=['GET'])
def gain_graph():
    dfg = dfg_factory.apply(log)
    this_data = dfg_to_g6.dfg_to_g6(dfg)
    return jsonify(this_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

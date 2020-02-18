import os
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
import json


def dfg_to_g6(dfg):
    unique_nodes = []

    for i in dfg:
        unique_nodes.extend(i)
    unique_nodes = list(set(unique_nodes))

    unique_nodes_dict = {}

    for index, node in enumerate(unique_nodes):
        unique_nodes_dict[node] = "node_" + str(index)

    nodes = [{"id": unique_nodes_dict[i], "name": i, "infor": {}} for i in unique_nodes_dict]
    edges = [{"source": unique_nodes_dict[i[0]], "target": unique_nodes_dict[i[1]], "data": {"freq": dfg[i]}} for i in
             dfg]

    data = {
        "nodes": nodes,
        "edges": edges,
    }
    return data


if __name__ == '__main__':
    log = xes_importer.import_log(os.path.join("repairExample.xes"))

    this_dfg = dfg_factory.apply(log)
    this_data = dfg_to_g6(this_dfg)
    print(json.dumps(this_data))

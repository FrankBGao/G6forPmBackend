import pandas as pd
import time
import inspect
import os
import sys
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import factory as log_conv_factory
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.objects.log.util import sorting
from pm4py.objects.log.log import EventLog, Trace, Event
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.visualization.dfg import factory as dfg_vis_fact
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.algo.discovery.dfg import factory as dfg_factory
import converter.dfg_to_g6 as dfg_to_g6

from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))


def get_groups(log):
    grouplist = Counter()

    for trace in log:
        for i in range(len(trace) - 1):
            timestamp_i = trace[i]["time:timestamp"].timestamp()
            for j in range(i + 1, len(trace)):
                timestamp_j = trace[j]["time:timestamp"].timestamp()
                if (timestamp_j - timestamp_i) >= 3000:
                    break
            j = j - 1
            if j > i:
                pattern = tuple(sorted([x["concept:name"] for x in trace[i:j + 1]]))

                i = j + 1
                grouplist[pattern] += 1

    #print(grouplist)
    return grouplist


def rewritelog(newgrouplist):
    # newgrouplist = [["['MED_Arterenol         ml', 'MED_Lasix             ml']", "group1"],
    #                 ["['MED_Arterenol         ml', 'MED_Hydrocortison     ml']", "group2"],
    #                 ["['MED_Arterenol         ml', 'MED_Arterenol         ml']", "group3"],
    #                 ["['MED_Arterenol         ml', 'MED_Arterenol         ml', 'MED_Arterenol         ml']", "group6"],
    #                 [
    #                     "['MED_Arterenol         ml', 'MED_Arterenol         ml', 'MED_Arterenol         ml', 'MED_Arterenol         ml']",
    #                     "group7"],
    #                 ["['MED_Arterenol         ml', 'MED_Recuronium        ml']", "group4"],
    #                 ["['MED_Ciprobay', 'MED_Zienam']", "group5"]
    #                 ]
    newlog = EventLog()

    for trace in log:
        newTrace = Trace()
        for attr in trace.attributes:
            newTrace.attributes[attr] = trace.attributes[attr]
        replaced_something = False

        i = 0
        while i < len(trace):
            replace_event_index_i = False

            for group in newgrouplist:
                findpattern = eval(group[0])
                replacepattern = group[1]

                if len(findpattern) < (len(trace) - i):
                    corresponding_event_sequence = trace[i:i + len(findpattern)]
                    timestamp_i = trace[i]["time:timestamp"].timestamp()
                    timestamp_j = trace[i + len(findpattern) - 1]["time:timestamp"].timestamp()
                    diff = timestamp_j - timestamp_i
                    if diff < 3000:
                        corresponding_event_sequence = sorted([x["concept:name"] for x in corresponding_event_sequence])
                        if findpattern == corresponding_event_sequence:
                            '''
                            for attr in trace.attributes:
                                print("trace att = ", trace.attributes[attr], "pattern = ", corresponding_event_sequence)
                            '''
                            replace_event_index_i = True
                            replaced_something = True
                            new_event = Event()
                            new_event["concept:name"] = replacepattern
                            new_event["time:timestamp"] = trace[i]["time:timestamp"]
                            newTrace.append(new_event)
                            i = i + len(findpattern)
                            break

            if replace_event_index_i == False:
                newTrace.append(trace[i])
                i = i + 1

        newlog.append(newTrace)
    xes_exporter.export_log(newlog, os.path.join("SimplifiedLog.xes"))
    return newlog


def execute_script1():
    aa = time.time()
    inputFile = "C:\\Users\\shankar\\PycharmProjects\\InformScripts\\Data\\kngNew0.csv"
    df = pd.read_csv(inputFile, sep=";", quotechar="\"")
    bb = time.time()


if __name__ == "__main__":
    log_path = os.path.join("exportedlog.xes")
    log = xes_import_factory.apply(log_path)
    log = sorting.sort_timestamp(log)
    '''dataframe = log_conv_factory.apply(log, variant=log_conv_factory.TO_DATAFRAME)
    ddd = dataframe.groupby('case:concept:name')
    for group in ddd:

        print("dd = ",type(dd))
        dd.sort_values(['concept:name'])

        de_dup = dd['concept:name'].loc[(dd['concept:name'].shift() != dd['concept:name']).any(axis=1)]

    '''

def uselog(loginput):
    log = xes_import_factory.apply(loginput)
    log = sorting.sort_timestamp(log)
    print(log)
    dfg = dfg_factory.apply(log)
    dfg_gv = dfg_vis_fact.apply(dfg, log, parameters={"format": "svg"})
    this_data = dfg_to_g6.dfg_to_g6(dfg)

    dfg_vis_fact.view(dfg_gv)
    return this_data

    '''grouplist = get_groups(log)
    newlog = rewritelog(log)
    dfg = dfg_factory.apply(newlog)
    this_data = dfg_to_g6.dfg_to_g6(dfg)
    print(this_data)
    dfg_gv1 = dfg_vis_fact.apply(dfg, newlog, parameters={"format": "svg"})
    dfg_vis_fact.view(dfg_gv1)

    return this_data
    '''
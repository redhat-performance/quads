import yaml
import json
from datetime import datetime, timedelta
from pathlib2 import Path


def load_data_into_dict(data):
    """ Reads all the data stored in quads yaml file.
    converts it into a single dictionary object.
    """
    #import pdb; pdb.set_trace()
    if data.is_file():
        with open(data.as_posix(), 'r') as file:
            quads = yaml.safe_load(file)
    else:
        return "invalid file"
    return quads

def fetch_hosttype(fq_hostname):
    """ Takes as an input FQDN of the host.
    Extracts the type from the hostname.
    """

    short_host_name = fq_hostname.split(".")
    host_type = short_host_name[0].split("-")[-1]
    return host_type


def save_data_to_json(data, filename):
    """ Saves <data> (eg. dict, list etc) as json to <filename>. """
    with open(filename, 'w') as file_name:
        json.dump(data, file_name)

def calculate_availability(quads, date_obj):
    """ Calculate availability of nodes for one day given by <date_obj>
    Segregated node availability type wise
    Return it as <result> dictionary object 
    """
    result = {} # Today's node availability will be found here.
    now_timestamp = date_obj.strftime("%s")
    #print "DEBUG: Starting with total hosts: {}".format(len(quads['hosts']))
    for host in quads['hosts'].keys():
        host_name = host
        host_type = fetch_hosttype(host_name)
        host_dict = quads['hosts'][host]
        last_key = host_dict['schedule'].keys()[-1]
        end_date = host_dict['schedule'][last_key]['end']
        end_obj = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        end_timestamp = end_obj.strftime('%s')
        if now_timestamp > end_timestamp: # Node is available for scheduling
            # Adding node info to the results
            if host_type in result.keys():
                result[host_type].append(host)
            else:
                result[host_type] = [host]
            quads['hosts'].pop(host)
    return result


def merge_results(dict_1, dict_2):
    """ Takes as an input a dictionary with key: value format as
    <string>:[list of items]. Merges the item list for common keys
    from dict_2 to dict_1. Adds new keys from dict_2 to dict_1
    Returns a merged dictionary
    """
    dict_3 = dict_1.copy()
    for	item in	dict_2:
        if item	in dict_3.keys():
            dict_3[item] = dict_3[item] + dict_2[item]
	else:
            dict_3[item] = dict_2[item]
    return dict_3


def main():
    """ Find the current availability as of now. """
#    import pdb; pdb.set_trace()
    data = Path("schedule.yaml")
    quads = load_data_into_dict(data)

    date_obj = datetime(2018, 8, 15, 11, 34, 45, 247969)
    #date_obj = datetime.today() #date object set to current time.
    date_obj = date_obj.replace(microsecond=0)
    timestamp = date_obj.strftime("%s")
    avail_nodes = {} # node availability per day will be found here.
    busy_nodes = {}
    interval = 1
    total_nodes = len(quads['hosts'])
    upuntil_today = {}

    # Calculate all availability in the future:
#    import pdb; pdb.set_trace()
    while(len(quads['hosts']) > 0):
        #print "Day: {} -- {}".format(interval, date_obj.strftime('%c'))
        only_today = calculate_availability(quads, date_obj)
        upuntil_today = merge_results(upuntil_today, only_today)
        avail_nodes[timestamp] = upuntil_today
        busy_nodes[timestamp] = len(quads['hosts'])
        date_obj = date_obj + timedelta(days=interval)
        timestamp = date_obj.strftime("%s")


    #save_data_to_json(avail_nodes, "all_availabilty.json")
    return avail_nodes

def blockit():
    """
    timestamps.sort()

    days = []
    DellR630 = []
    DellR620 = []
    R620 = []
    misc = []
    type_1029p = []
    total_avail = []
    busy = []

    for timestamp in timestamps:
        dt_obj = datetime.fromtimestamp(float(timestamp))
        free_nodes = 0
        days.append(dt_obj.isoformat())
        misc.append(len(avail_nodes[timestamp]['misc']))
        free_nodes += len(avail_nodes[timestamp]['misc'])
        R620.append(len(avail_nodes[timestamp]['R620']))
        free_nodes += len(avail_nodes[timestamp]['R620'])
        DellR620.append(len(avail_nodes[timestamp]['DellR620']))
        free_nodes += len(avail_nodes[timestamp]['DellR620'])
        DellR630.append(len(avail_nodes[timestamp]['DellR630']))
        free_nodes += len(avail_nodes[timestamp]['DellR630'])
        type_1029p.append(len(avail_nodes[timestamp]['1029p']))
        free_nodes += len(avail_nodes[timestamp]['1029p'])
        total_avail.append(free_nodes)
        busy.append(340-free_nodes)


    print "*"*100
    print "                          **** Node availability per day, sorted per type. ****"
    print "*"*100

    print "{:20s} {:10s} {:10s} {:10s} {:10s} {:10s} {:12s} {:12s} ".format(
            "Days_time", "DellR630", "DellR620", "R620", "misc", "1029p", "Total_free", "Still Busy"
            )

    for day, x, y, z, m, t, free, not_free in zip(
            days, DellR630, DellR620, R620, misc, type_1029p, total_avail, busy
            ):
        print "{:20s} {:8d} {:10d} {:10d} {:10d} {:10d} {:12d} {:12d} ".format(
                day, x, y, z, m, t, free, not_free
                )

    
    print " "*100
    print "*"*100
    """
    pass


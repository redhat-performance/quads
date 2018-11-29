import yaml
import json
from datetime import datetime, timedelta
from pathlib2 import Path


def load_data_into_dict(data):
    """ Reads all the data stored in quads yaml file.
    converts it into a single dictionary object.
    """
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
    data = Path("schedule.yaml")
    quads = load_data_into_dict(data)
# For testing set the following date_obj to any date in past.
#    date_obj = datetime(2018, 8, 20, 11, 34, 45, 247969)
# For production use comment out the above line and uncomment the line below.
    date_obj = datetime.today() #date object set to current time.
    date_obj = date_obj.replace(microsecond=0)
    timestamp = date_obj.strftime("%s")
    avail_nodes = {} # node availability per day will be found here.
    busy_nodes = {}
    interval = 1
    total_nodes = len(quads['hosts'])
    upuntil_today = {}

    # Calculate all availability in the future:
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


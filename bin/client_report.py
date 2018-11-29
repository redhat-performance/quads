import datetime
import json

def report_all_availability(json_data):
    """
    Takes as an input either a dictionary 
    or a json file with dictionary.
    """

    if(type(json_data) == dict):
        data = json_data
    else: #we assume that it is a json file.
        with open(json_data) as json_file:
            data = json.load(json_file)

    timestamps = data.keys()
    timestamps.sort()
        ## Uncomment the following for loop to check if all types are reported correctly.
#    for timestamp in timestamps:
#        dt_obj = datetime.datetime.fromtimestamp(float(timestamp))
#        print " "
#        print "Availability on {}".format(dt_obj.strftime('%c'))
#        print "Node availability Type wise: "
#        for node_types in data[timestamp].keys():
#            print " {:20s} :   {:5d}".format(node_types, len(data[timestamp][node_types]))
#
#        print "*"*35
#        print " "

    days = []
    r620 = []
    r630 = []
    r730xd = []
    r930 = []
    type_6018r = []
    type_6048r = []
    type_1028r = []
    type_1029p = []
    total_avail = []
    busy = []
    print " "

    for timestamp in timestamps:
        dt_obj = datetime.datetime.fromtimestamp(float(timestamp))
        free_nodes = 0
        days.append(dt_obj.isoformat())
        if 'r620' in data[timestamp].keys():
            r620.append(len(data[timestamp]['r620']))
            free_nodes += len(data[timestamp]['r620'])
        else:
            r620.append(0)

        if 'r630' in data[timestamp].keys():
            r630.append(len(data[timestamp]['r630']))
            free_nodes += len(data[timestamp]['r630'])
        else:
            r630.append(0)

        if 'r730xd' in data[timestamp].keys():
            r730xd.append(len(data[timestamp]['r730xd']))
            free_nodes += len(data[timestamp]['r730xd'])
        else:
            r730xd.append(0)
        if 'r930' in data[timestamp].keys():
            r930.append(len(data[timestamp]['r930']))
            free_nodes += len(data[timestamp]['r930'])
        else:
            r930.append(0)

        if '6018r' in data[timestamp].keys():
            type_6018r.append(len(data[timestamp]['6018r']))
            free_nodes += len(data[timestamp]['6018r'])
        else:
            type_6018r.append(0)

        if '6048r' in data[timestamp].keys():
            type_6048r.append(len(data[timestamp]['6048r']))
            free_nodes += len(data[timestamp]['6048r'])
        else:
            type_6048r.append(0)

        if '1028r' in data[timestamp].keys():
            type_1028r.append(len(data[timestamp]['1028r']))
            free_nodes += len(data[timestamp]['1028r'])
        else:
            type_1028r.append(0)

        if '1029p' in data[timestamp].keys():
            type_1029p.append(len(data[timestamp]['1029p']))
            free_nodes += len(data[timestamp]['1029p'])
        else:
            type_1029p.append(0)

        total_avail.append(free_nodes)
        busy.append(340-free_nodes)

    print "*"*100
    print "                          **** Node availability per day, sorted per type. ****"
    print "*"*100

    print "{:20s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:10s} {:12s} {:12s} ".format(
            "Days_time", "r620", "r630", "r730xd", "r930", "6018r", "6048r", "1028r", "1029p",
            "Total_free", "Still Busy")
    for day, x, y, z, m, n, o, p, q, free, not_free in zip(
            days, r620, r630, r730xd, r930, type_6018r, type_6048r, type_1028r, type_1029p,
            total_avail, busy
            ):
        
        print "{:20s} {:8d} {:10d} {:10d} {:10d} {:10d} {:10d} {:10d} {:10d} {:12d} {:12d} ".format(day, x, y, z, m, n, o, p, q, free, not_free
                )


    print " "*100
    print "*"*100


if __name__ == "__main__":
    main()


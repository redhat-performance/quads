from mongoengine import ObjectIdField


def param_check(data, params, defaults={}):
    result = []
    # set defaults
    for k, v in defaults.items():
        data.setdefault(k, v)

    if data:
        # check for missing params
        for p in params:
            if p not in data:
                result.append("Missing required parameter: %s" % p)
            elif not (data[p] or data[p] is None):
                result.append("Could not parse %s parameter" % p)
            elif data[p] == 'None':
                data[p] = None
            if p == "_id":
                data["_id"] = ObjectIdField(data[p])

    return result, data

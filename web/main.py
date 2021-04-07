#!/usr/bin/env python3

from datetime import datetime, time
from mongoengine import Q
from app import app
from forms import ModelSearchForm
from flask import render_template, request, jsonify
from quads.model import Host, Schedule


@app.route("/", methods=["GET", "POST"])
def index():
    search = ModelSearchForm(request.form)
    if request.method == "POST":
        return search_results(search)

    return render_template("index.html", form=search, available_hosts=[])


@app.route("/results")
def search_results(search):
    available_hosts = available(search)

    return render_template("index.html", form=search, available_hosts=available_hosts)


@app.route("/available")
def available(search):
    models = search.data["model"]

    if models:
        query = None
        for model in models:
            if query:
                query = query | Q(model=model.upper())
            else:
                query = Q(model=model.upper())

        hosts = Host.objects.filter(query)
    else:
        hosts = Host.objects().all()

    broken_hosts = Host.objects(broken=True)

    available_hosts = []
    start = datetime.combine(search.data["start"], time(hour=22))
    end = datetime.combine(search.data["end"], time(hour=22))

    if hosts:
        for host in hosts:
            if (
                Schedule.is_host_available(host=host["name"], start=start, end=end)
                and host not in broken_hosts
            ):
                host_dict = {"name": host.name, "model": host.model}
                available_hosts.append(host_dict)

    return jsonify(available_hosts)


if __name__ == "__main__":
    # Gunicorn imports this file so this is ignored
    # Though one can run this file directly for debugging
    app.debug = True
    app.run(host="0.0.0.0", port=5001)

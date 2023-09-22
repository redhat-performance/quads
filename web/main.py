#!/usr/bin/python3

from datetime import datetime, time

from forms import ModelSearchForm
from flask import render_template, request, jsonify

from app import app
from quads.config import Config
from quads.quads_api import QuadsApi as Quads, APIServerException, APIBadRequest

quads = Quads(Config)


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
    try:
        start, end = [
            datetime.strptime(date, "%Y-%m-%d").date() for date in search.data["date_range"].split(" - ")
        ]
        start = datetime.combine(start, time(hour=22)).strftime("%Y-%m-%d %H:%M")
        end = datetime.combine(end, time(hour=22)).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify([])

    try:
        hosts = quads.filter_available(data={"start": start, "end": end})
        if models:
            models = [model.upper() for model in models]
            hosts = [host for host in hosts if host.model in models]

        available_hosts = []
        currently_scheduled = [schedule.host_id for schedule in quads.get_current_schedules()]
        for host in hosts:
            current = True if host.id in currently_scheduled else False
            host_dict = {"name": host.name, "cloud": host.cloud.name, "model": host.model, "current": current}
            available_hosts.append(host_dict)
    except (APIBadRequest, APIServerException):
        return jsonify({})

    return jsonify(available_hosts)


if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=5001)

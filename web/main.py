#!/usr/bin/python3
# main.py
import asyncio
from datetime import datetime, time

from mongoengine import Q

from app import app
from forms import ModelSearchForm
from flask import flash, render_template, request, redirect, jsonify

from quads.config import conf
from quads.model import Host, Schedule
from quads.tools.foreman import Foreman


@app.route('/', methods=['GET', 'POST'])
def index():
    search = ModelSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search, available_hosts=[])


@app.route('/results')
def search_results(search):
    available_hosts = available(search)

    return render_template('index.html', form=search, available_hosts=available_hosts)


@app.route('/available')
def available(search):
    models = search.data['model']

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

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        loop=loop,
    )
    broken_hosts = loop.run_until_complete(foreman.get_broken_hosts())

    available_hosts = []
    start = datetime.combine(search.data['start'], time.min)
    end = datetime.combine(search.data['end'], time.min)

    if hosts:
        for host in hosts:
            if Schedule.is_host_available(
                host=host["name"], start=start, end=end
            ) and not broken_hosts.get(host["name"], False):
                host_dict = {"name": host.name, "model": host.model}
                available_hosts.append(host_dict)

    return jsonify(available_hosts)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5001)

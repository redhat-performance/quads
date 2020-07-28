# main.py
import asyncio
from datetime import datetime, time

from app import app
from forms import ModelSearchForm
from flask import flash, render_template, request, redirect

from quads.config import conf
from quads.model import Host, Schedule
from quads.tools.foreman import Foreman


@app.route('/', methods=['GET', 'POST'])
def index():
    search = ModelSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    hosts = []
    model = search.data['model']

    if search.data['model'] != '':
        _filter = {"model": model}
        hosts = Host.objects(**_filter).all()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        loop=loop,
    )
    broken_hosts = loop.run_until_complete(foreman.get_broken_hosts())

    available = []
    start = datetime.combine(search.data['start'], time.min)
    end = datetime.combine(search.data['end'], time.min)

    if hosts:
        for host in hosts:
            if Schedule.is_host_available(
                host=host["name"], start=start, end=end
            ) and not broken_hosts.get(host["name"], False):
                available.append(host["name"])

    if not available:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)

# main.py

from app import app
from forms import ModelSearchForm
from flask import flash, render_template, request, redirect

from quads.model import Host


@app.route('/', methods=['GET', 'POST'])
def index():
    search = ModelSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    model = search.data['search']

    if search.data['search'] == '':
        filter = {"model": model}
        results = Host.objects(**filter).all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)

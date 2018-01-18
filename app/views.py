from app import app

from flask import render_template


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/awards', methods=['GET'])
def awards():
    return render_template('awards.html')


@app.route('/camps', methods=['GET'])
def camps():
    return render_template('camps.html')


@app.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')


@app.route('/robots', methods=['GET'])
def robots():
    return render_template('robots.html')


@app.route('/sponsors', methods=['GET'])
def sponsors():
    return render_template('sponsors.html')

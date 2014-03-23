import pandas
import random

from flask import render_template
from flask import Flask
app = Flask(__name__)

spell_list = pandas.read_csv("spell_full.csv")
spell_list = [dict(row) for i, row in spell_list.iterrows()]


@app.route('/spell/<spell_id>')
@app.route('/spell/<spell_id>?type=<classification>')
def index(spell_id,classification=None):
    if classification:
        print classification
    stuff = spell_list[int(spell_id)]
    return render_template('training_setr.html', **stuff)

@app.route('/classify/<spell_id>/<classification>')
def classify(spell_id,classification):
    print spell_id,classification
    return  spell_id,classification

if __name__ == '__main__':
    app.run(port=8889)

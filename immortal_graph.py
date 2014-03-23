import sys,os,random
import logging
import gensim
import nltk
import string
import json
import networkx as nx
from networkx.readwrite import json_graph

from gensim.models import Word2Vec

from flask import render_template
from flask import Flask
app = Flask(__name__)

replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))

class Corpus(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            fname = os.path.join(self.dirname, fname)
            if not os.path.isfile(fname):
                continue
            for line in open(fname):
                line = line.translate(replace_punctuation).lower()
                words = nltk.PunktWordTokenizer().tokenize(line.decode('utf-8','ignore'))
                if not words: # don't bother sending out empty sentences
                    continue
                yield words

def train(corpus_dir, model_file):
	model = Word2Vec(Corpus(corpus_dir), size=200, min_count=5, workers=4)
	model.save_word2vec_format(model_file + '.bin',binary=True)





model = Word2Vec.load_word2vec_format('immortals.bin', binary=True)


def form_graph():
	for node1 in G.nodes_iter():
		for node2 in G.nodes_iter():
			if (node1 != node2):
				try:
					w=model.similarity(node1,node2)
				except:
					pass
				if(w>.25): G.add_edge(node1,node2,weight=w)
				if(len(G.edges(node1))>5):
					cut_weakest_link(node1)
	for node in G.nodes_iter(): # kill the orphans
		if (len(G.edges(node))==0):
			G.remove_node(node)

def cut_weakest_link(node):
	edges = G.edges(node, data=True)
	weakest_link = min([edge[2]['weight'] for edge in edges])
	for edge in edges:
		if (edge[2]['weight']<=weakest_link):
			G.remove_edge(edge[0],edge[1])

def graph_to_json():
	graph = json_graph.node_link_data(G)
	return json.dumps(graph)

def save_graph():
	f = open('graph.json','w')
	f.write(json.dumps(json_graph.node_link_data(G)))

def load_graph():
	f = open('graph.json','r')
	g = f.read()
	G = json_graph.loads(g)
	return G

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

G = load_graph()
if G:
	print 'graph loaded'
else:
	G = nx.Graph()
	print 'no graph found, creating new one'

#train('./corpus','immortals')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_node/<string:node>')
def new_node(node):
    G.add_node(node)
    return "Added {}".format(node)

@app.route('/remove_node/<string:node>')
def kill_node(node):
    G.remove_node(node)
    return "killed {}".format(node)

@app.route('/data/')
def get_graph():
    form_graph()
    return graph_to_json()

@app.route('/save/')
def graph_save():
    save_graph()
    return "graph saved"

@app.route('/load/')
def graph_restore():
    load_graph()
    return "graph loaded"

if __name__=='__main__':
	app.run(port=8888,host='0.0.0.0')


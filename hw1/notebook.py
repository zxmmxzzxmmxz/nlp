from pcfg_parse_gen import Pcfg, PcfgGenerator, CkyParse
import nltk
from nltk.draw.tree import draw_trees
from nltk import tree, treetransforms
from copy import deepcopy

def print_tree(tree_string):
    tree_string = tree_string.strip()
    tree = nltk.Tree.fromstring(tree_string)
    tree.pretty_print()

def draw_tree(tree_string):
    tree_string = tree_string.strip()
    tree = nltk.Tree.fromstring(tree_string)
    tree.draw()

parse_gram = Pcfg(["S1.gr","S2.gr","Vocab.gr"])

parser = CkyParse(parse_gram, beamsize=0.00001)

ce, trees = parser.parse_file('devset.txt')
print("-cross entropy: {}".format(ce))
from nltk import tree


class Tree:
    _trees = []
    _root = None

    def __init__(self, sentence):
        while sentence.find("(") != -1:
            left_bracket_index = sentence.find("(")
            right_bracket_index = left_bracket_index
            number_of_open_brackets = 1
            for (i, each_char) in enumerate(sentence[left_bracket_index + 1:]):
                if each_char == '(':
                    number_of_open_brackets += 1
                elif each_char == ')':
                    number_of_open_brackets -= 1
                    if number_of_open_brackets == 0:
                        right_bracket_index = i + 1
                        break
            self._root = self.analyze_grammars(sentence[left_bracket_index: left_bracket_index + right_bracket_index + 1], True)
            self._trees.append(self.analyze_grammars(sentence[left_bracket_index: left_bracket_index + right_bracket_index + 1], True))
            sentence = sentence[left_bracket_index + right_bracket_index + 1:]

    def transformToCNF(self, sentence):
        t = tree.Tree.fromstring(sentence, remove_empty_top_bracketing=True)

        # convert the tree to CNF
        t.chomsky_normal_form()
        return str(t)

    # should return a tree's root node
    def analyze_grammars(self, sentence, top):
        #print(sentence)
        sentence = self.transformToCNF(sentence)
        #print("after CNF transform")
        #print(sentence)
        if len(sentence.split()) == 2:
            # this is a terminal grammar segment
            terminal_parts = sentence.replace("(", " ").replace(")", " ").split()
            if not terminal_parts:
                return None
            if terminal_parts[0] == terminal_parts[1]:
                terminal_parts[0] *= 2
            new_node = GrammarNode(terminal_parts[0], terminal_parts[1])
            new_node.set_is_terminal(True)
            return new_node

        # remove first ( and last )
        sentence_without_out_most_bracket = sentence[sentence.find("(") + 1: sentence.rfind(")")]
        # split it
        # first token is left hand side
        left_side = sentence_without_out_most_bracket.split()[0]
        # slice the next grammar by first ( and first ) until no more (
        right_side = []
        temp_sentence = sentence_without_out_most_bracket
        while temp_sentence.find("(") != -1:
            left_bracket_index = temp_sentence.find("(")
            right_bracket_index = left_bracket_index
            number_of_open_brackets = 1
            for (i, each_char) in enumerate(temp_sentence[left_bracket_index + 1:]):
                if each_char == '(':
                    number_of_open_brackets += 1
                elif each_char == ')':
                    number_of_open_brackets -= 1
                    if number_of_open_brackets == 0:
                        right_bracket_index = i + 1
                        break
            to_append = self.analyze_grammars(temp_sentence[left_bracket_index: left_bracket_index + right_bracket_index + 1],False)
            if to_append is not None:
                right_side.append(to_append)
            temp_sentence = temp_sentence[left_bracket_index + right_bracket_index + 1:]

        new_node = GrammarNode(left_side, right_side)
        if top:
            new_node = GrammarNode("S1", [new_node])
        return new_node

    def dump_to_grammars(self):
        grammars = {}
        for each_tree in self._trees:
            self.dump_to_grammars_internal(each_tree, grammars)
        return grammars

    def dump_to_grammars_internal(self, node, grammars):
        if node.is_terminal():
            left = node.get_left_hand_side()
            right = node.get_right_hand_side()
            a_grammar = Grammar(left, right)
            if grammars.get(a_grammar) is None:
                grammars[a_grammar] = 1
                #grammars[a_grammar] = 0
            else:
                grammars[a_grammar] += 1
                #grammars[a_grammar] = 0
            return

        left = node.get_left_hand_side()
        right = " ".join(map(lambda n: n.get_left_hand_side(), node.get_right_hand_side()))
        a_grammar = Grammar(left, right)
        if grammars.get(a_grammar) is None:
            grammars[a_grammar] = 1
            grammars[a_grammar] = 0
        else:
            grammars[a_grammar] += 1
            grammars[a_grammar] = 0
        for each in node.get_right_hand_side():
            self.dump_to_grammars_internal(each, grammars)




class GrammarNode:
    _left_hand_side = None
    _right_hand_side = []
    _isTerminal = False

    def __init__(self, left_hand_side=None, right_hand_side=[]):
        self._left_hand_side = left_hand_side
        self._right_hand_side = right_hand_side

    def set_left_hand_side(self, left_hand_side):
        self._left_hand_side = left_hand_side

    def set_right_hand_side(self, right_hand_side):
        self._right_hand_side = right_hand_side

    def set_is_terminal(self, is_terminal):
        self._isTerminal = is_terminal

    def get_left_hand_side(self):
        return self._left_hand_side

    def get_right_hand_side(self):
        return self._right_hand_side

    def is_terminal(self):
        return self._isTerminal

    def attach_node(self, node):
        self._children.push(node)

class Grammar:
    _left = ""
    _right = ""
    _prob = -1

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def __hash__(self):
        return hash((self._left, self._right))

    def __eq__(self, other):
        return other is not None and self._left == other._left and self._right == other._right

    def __str__(self):
        return self._left + "  " + self._right


with open("testdevset.trees", "r") as f:
    sentences = ''.join(f.readlines())
f.close()
# sentences = '''(TOP (S1 (NP (Proper Arthur) )
#              (_VP (VP (VerbT is)
#                       (NP (Det the)
#                           (Nbar (Noun king) )))
#                   (Punc .))) )
#
#             (TOP (S1 (NP (Proper Arthur) )
#              (_VP (VP (VerbT is)
#                       (NP (Det the)
#                           (Nbar (Noun king) (Noun king1))))
#                   (Punc .))) )
#             '''
#print("sentences are {0}".format(sentences))
stuff = Tree(sentences)
grammars_with_count = stuff.dump_to_grammars()

left_set = set()
for key in grammars_with_count.keys():
    left_set.add(key._left)

for each_left in left_set:
    filtered_keys = {k:v for (k,v) in grammars_with_count.items() if k._left == each_left}
    total_count = 0
    for each in filtered_keys:
        total_count += grammars_with_count.get(each)
    # for grammar_to_update in filtered_keys:
    #     grammar_to_update._prob = grammars_with_count.get(grammar_to_update) / float(total_count)

with open("T.gr", "w") as wf:
    for item in grammars_with_count.items():
        if item[1] is not 0:
            wf.write(str(item[1]) + " " + str(item[0]) + "\n")
wf.close()
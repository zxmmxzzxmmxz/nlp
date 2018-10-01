#testSentecne = "( (NP-TMP (NNP December) (CD 1998)))"
#testSentecne = "(NP-TMP (NNP December))"
'''sentence = (TOP (S1 (NP (Proper Arthur) )
             (_VP (VP (VerbT is)
                      (NP (Det the)
                          (Nbar (Noun king) )))
                  (Punc .))) )'''
#sentence = '''NP (Nbar (Noun king) )
 #                 (Det the) '''


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
            self._root = self.analyze_grammars(sentence[left_bracket_index: left_bracket_index + right_bracket_index + 1])
            self._trees.append(self.analyze_grammars(sentence[left_bracket_index: left_bracket_index + right_bracket_index + 1]))
            sentence = sentence[left_bracket_index + right_bracket_index + 1:]

    # should return a tree's root node
    def analyze_grammars(self, sentence):
        if len(sentence.split()) == 2:
            # this is a terminal grammar segment
            terminal_parts = sentence.replace("(", " ").replace(")", " ").split()
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
            right_side.append(self.analyze_grammars(temp_sentence[left_bracket_index: left_bracket_index + right_bracket_index + 1]))
            temp_sentence = temp_sentence[left_bracket_index + right_bracket_index + 1:]

        new_node = GrammarNode(left_side, right_side)
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
            else:
                grammars[a_grammar] += 1
            return

        left = node.get_left_hand_side()
        right = " ".join(map(lambda n: n.get_left_hand_side(), node.get_right_hand_side()))
        a_grammar = Grammar(left, right)
        if grammars.get(a_grammar) is None:
            grammars[a_grammar] = 1
        else:
            grammars[a_grammar] += 1
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
        return "Prob {0} ".format(self._prob) + self._left + "->" + self._right



sentence = '''(TOP (S1 (NP (Proper Arthur) )
             (_VP (VP (VerbT is)
                      (NP (Det the)
                          (Nbar (Noun king) )))
                  (Punc .))) )
                  
            (TOP (S1 (NP (Proper Arthur) )
             (_VP (VP (VerbT is)
                      (NP (Det the)
                          (Nbar (Noun king) (Noun king1))))
                  (Punc .))) )
            '''
print("sentence is {0}".format(sentence))
stuff = Tree(sentence)
grammars_with_count = stuff.dump_to_grammars()

left_set = set()
for key in grammars_with_count.keys():
    left_set.add(key._left)

for each_left in left_set:
    filtered_keys = {k:v for (k,v) in grammars_with_count.items() if k._left == each_left}
    total_count = 0
    for each in filtered_keys:
        total_count += grammars_with_count.get(each)
    for grammar_to_update in filtered_keys:
        grammar_to_update._prob = grammars_with_count.get(grammar_to_update) / float(total_count)

for item in grammars_with_count.items():
    print(item[0])
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
    _root = None

    def __init__(self, sentence):
        self.root = self.analyze_grammars(sentence)

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

    def is_terminal(self):
        return self._isTerminal

    def attach_node(self, node):
        self._children.push(node)


sentence = '''(TOP (S1 (NP (Proper Arthur) )
             (_VP (VP (VerbT is)
                      (NP (Det the)
                          (Nbar (Noun king) )))
                  (Punc .))) )'''
stuff = Tree(sentence)
print(stuff)

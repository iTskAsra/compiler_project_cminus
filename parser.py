from anytree import Node, RenderTree
import scanner
import re

parsed_tree = Node("Program")
token = []
parsed_tree_address = "parse-tree.txt"
syntax_errors_address = "syntax-errors.txt"
syntax_errors = []
error_raised = False
current_line = 1
token_popped = True

valid_first = re.compile(r'if|else|int|repeat|break|void|until|return|endif|ID|NUM')


def get_token_line():
    return token[0]


def get_token():
    return token[1]


def get_new_token():
    global token
    token = scanner.get_next_token()


def get_token_type():
    return token[2]


def save_parsed_tree(address):
    with open(address, 'w', encoding="utf-8") as f:
        for pre, fill, node in RenderTree(parsed_tree):
            f.write("%s%s\n" % (pre, node.name))


def initialize_errors_file(address):
    with open(address, 'w') as f:
        f.write("There is no syntax error.")


def update_syntax_errors(line, terminal, error_description):
    syntax_errors.append([line, terminal, error_description])


def save_syntax_errors(address):
    with open(address, 'w') as f:
        for error in syntax_errors:
            f.write(f"#{error[0]} : syntax error, {error[2]} {error[1]}\n")


class FirstAndFollowSets:
    first_and_follow_sets = [
        ('Program', ['EPSILON', 'int', 'void', '$'],
         ['$']),

        ('Declaration-list', ['int', 'void', 'EPSILON'],
         ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'repeat', 'return']),

        ('Declaration', ['int', 'void'],
         ['int', 'void', '$', '{', '}', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM']),

        ('Declaration-initial', ['int', 'void'],
         ['(', ')', ',', ';', '[']),

        ('Declaration-prime', [';', '[', '('],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}']),

        ('Var-declaration-prime', [';', '['],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}']),

        ('Fun-declaration-prime', ['('],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}']),

        ('Type-specifier', ['int', 'void'],
         ['ID']),

        ('Params', ['int', 'void'],
         [')']),

        ('Param', ['int', 'void'],
         [',', ')']),

        ('Param-list', ['int', 'void', 'EPSILON'],
         [')']),

        ('Param-prime', ['[', 'EPSILON'],
         [',', ')']),

        ('Compound-stmt', ['{'],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
          'until']),

        ('Statement-list', ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'EPSILON'],
         ['}']),

        ('Statement', ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'EPSILON'],
         ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until']),

        ('Expression-stmt', ['ID', ';', 'NUM', '(', 'break', ],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Selection-stmt', ['if'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Else-stmt', ['endif', 'else'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Iteration-stmt', ['repeat'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Return-stmt', ['return'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Return-stmt-prime', ['ID', ';', 'NUM', '('],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Expression', ['ID', 'NUM', '('],
         [";", ")", "]", ","]),

        ('B', ['ID', '[', 'NUM', '(', '<', '==', '+', '-', '*', 'EPSILON'],
         [";", ")", "]", ","]),

        ('H', ['ID', 'NUM', '(', '<', '==', '+', '-', '*', 'EPSILON'],
         [";", ")", "]", ","]),

        ('Simple-expression-zegond', ['NUM', '('],
         [";", ")", "]", ","]),

        ('Simple-expression-prime', ['(', '<', '+', '-', '*', '==', 'EPSILON'],
         [";", ")", "]", ","]),

        ('C', ['<', '==', 'EPSILON'],
         [";", ")", "]", ","]),

        ('Relop', ['<', '=='],
         ["(", "ID", "NUM"]),

        ('Additive-expression', ['ID', 'NUM', '('],
         [";", ")", "]", ","]),

        ('Additive-expression-prime', ['(', '+', '-', '*', 'EPSILON'],
         ["<", "==", ";", ")", "]", ","]),

        ('Additive-expression-zegond', ['NUM', '('],
         ["<", "==", ";", ")", "]", ","]),

        ('D', ['+', '-', 'EPSILON'],
         ["<", "==", ";", ")", "]", ","]),

        ('Addop', ['+', '-'],
         ["(", "ID", "NUM"]),

        ('Term', ['ID', 'NUM', '('],
         ["+", "-", ";", ")", "<", "==", "]", ","]),

        ('Term-prime', ['(', '*', 'EPSILON'],
         ["+", "-", "<", "==", ";", ")", "]", ","]),

        ('Term-zegond', ['NUM', '('],
         ["+", "-", "<", "==", ";", ")", "]", ","]),

        ('G', ['*', 'EPSILON'],
         ["+", "-", "<", "==", ";", ")", "]", ","]),

        ('Factor', ['ID', 'NUM', '('],
         ["*", "+", "-", ";", ")", "<", "==", "]", ","]),

        ('Var-call-prime', ['[', '{', 'EPSILON'],
         ["*", "+", "-", ";", ")", "<", "==", "]", ","]),

        ('Var-prime', ['[', 'EPSILON'],
         ["*", "+", "-", ";", ")", "<", "==", "]", ","]),

        ('Factor-prime', ['(', 'EPSILON'],
         ["*", "+", "-", "<", "==", ";", ")", "]", ","]),

        ('Factor-zegond', ['NUM', '('],
         ["*", "+", "-", "<", "==", ";", ")", "]", ","]),

        ('Args', ['ID', 'NUM', '(', 'EPSILON'],
         [')']),

        ('Arg-list', ['ID', 'NUM', '('],
         [')']),

        ('Arg-list-prime', [',', 'EPSILON'],
         [')'])
    ]

    def is_token_in_firsts(self, non_terminal, terminal):
        result = False
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                for first in pair[1]:
                    if first == terminal:
                        result = True

        if terminal == non_terminal:
            result = True
        return result

    def is_token_in_follows(self, non_terminal, terminal):
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                for follow in pair[2]:
                    if follow == terminal:
                        return True

        return False

    def get_a_first(self, non_terminal):
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                return pair[1][0]


# in this compiler, the prediction sets are not used but the class is implemented anyways.
class PredictSets:
    prediction_sets = [
        ('Program', []),
        ('Declaration-list', []),
        ('Declaration', []),
        ('Declaration-initial', []),
        ('Declaration-prime', []),
        ('Var-declaration-prime', []),
        ('Fun-declaration-prime', []),
        ('Type-specifier', []),
        ('Params', []),
        ('Param', []),
        ('Param-list', []),
        ('Param-prime', []),
        ('Compound-stmt', []),
        ('Statement-list', []),
        ('Statement', []),
        ('Expression-stmt', []),
        ('Selection-stmt', []),
        ('Else-stmt', []),
        ('Iteration-stmt', []),
        ('Return-stmt', []),
        ('Return-stmt-prime', []),
        ('Expression', []),
        ('B', []),
        ('H', []),
        ('Simple-expression-zegond', []),
        ('Simple-expression,prime', []),
        ('C', []),
        ('Relop', []),
        ('Additive-expression', []),
        ('Additive-expression-prime', []),
        ('Additive-expression-zegond', []),
        ('D', []),
        ('Addop', []),
        ('Term', []),
        ('Term-prime', []),
        ('Term-zegond', []),
        ('G', []),
        ('Factor', []),
        ('Var-call-prime', []),
        ('Var-prime', []),
        ('Factor-prime', []),
        ('Factor-zegond', []),
        ('Args', []),
        ('Args-list', []),
        ('Args-list-prime', [])
    ]

    def is_token_in_predicts(self, non_terminal, terminal):
        for pair in self.prediction_sets:
            if pair[0] == non_terminal:
                for prediction in pair[1]:
                    if prediction == terminal:
                        return True

        return False


class TransitionDiagrams:
    diagram_tuples = [
        ('Program', [(('Declaration-list', 'NT'), ('$', 'T'))]),
        ('Declaration-list', [(('Declaration', 'NT'), ('Declaration-list', 'NT')),
                              (('EPSILON', 'T'),)]),
        ('Declaration', [(('Declaration-initial', 'NT'), ('Declaration-prime', 'NT'))]),
        ('Declaration-initial', [(('Type-specifier', 'NT'), ('ID', 'T'))]),
        ('Declaration-prime', [(('Fun-declaration-prime', 'NT'),),
                               (('Var-declaration-prime', 'NT'),)]),
        ('Var-declaration-prime', [(('[', 'T'), ('NUM', 'T'), (']', 'T'), (';', 'T')),
                                   ((';', 'T'),)]),
        ('Fun-declaration-prime', [(('(', 'T'), ('Params', 'NT'), (')', 'T'), ('Compound-stmt', 'NT'))]),
        ('Type-specifier', [(('int', 'T'),),
                            (('void', 'T'),)]),
        ('Params', [(('int', 'T'), ('ID', 'T'), ('Param-prime', 'NT'), ('Param-list', 'NT')),
                    (('void', 'T'),)]),
        ('Param-list', [((',', 'T'), ('Param', 'NT'), ('Param-list', 'NT')),
                        (('EPSILON', 'T'),)]),
        ('Param', [(('Declaration-initial', 'NT'),)]),
        ('Param-prime', [(('[', 'T'), (']', 'T')),
                         (('EPSILON', 'T'),)]),
        ('Compound-stmt', [(('{', 'T'), ('Declaration-list', 'NT'), ('Statement-list', 'NT'), ('}', 'T'))]),
        ('Statement-list', [(('Statement', 'NT'), ('Statement-list', 'NT')),
                            (('EPSILON', 'T'),)]),
        ('Statement',
         [(('Expression-stmt', 'NT'),)
             , (('Compound-stmt', 'NT'),)
             , (('Selection-stmt', 'NT'),)
             , (('Iteration-stmt', 'NT'),)
             , (('Return-stmt', 'NT'),)]),
        ('Expression-stmt', [(('Expression', 'NT'), (';', 'T')),
                             (('break', 'T'), (';', 'T')),
                             ((';', 'T'),)]),
        ('Selection-stmt', [(('if', 'T'), ('(', 'T'), ('Expression', 'NT'), (')', 'T'), ('Statement', 'NT'), ('Else-stmt', 'NT'))]),
        ('Else-stmt', [(('else', 'T'), ('Statement', 'NT'), ('endif', 'T')),
                       (('endif', 'T'),)]),
        ('Iteration-stmt', [(('repeat', 'T'), ('Statement', 'NT'), ('until', 'T'), ('(', 'T'), ('Expression', 'NT'), (')', 'T'))]),
        ('Return-stmt', [(('return', 'T'), ('Return-stmt-prime', 'NT'))]),
        ('Return-stmt-prime', [(('Expression', 'NT'), (';', 'T')),
                               ((';', 'T'),)]),
        ('Expression', [(('ID', 'T'), ('B', 'NT')),
                        (('Simple-expression-zegond', 'NT'),)]),
        ('B', [(('[', 'T'), ('Expression', 'NT'), (']', 'T'), ('H', 'NT')),
               (('=', 'T'), ('Expression', 'NT')),
               (('Simple-expression-prime', 'NT'),)]),
        ('H', [(('=', 'T'), ('Expression', 'NT')),
               (('G', 'NT'), ('D', 'NT'), ('C', 'NT'))]),
        ('Simple-expression-zegond', [(('Additive-expression-zegond', 'NT'), ('C', 'NT'))]),
        ('Simple-expression-prime', [(('Additive-expression-prime', 'NT'), ('C', 'NT'))]),
        ('C', [(('Relop', 'NT'), ('Additive-expression', 'NT')),
               (('EPSILON', 'T'),)]),
        ('Relop', [(('<', 'T'),),
                   (('==', 'T'),)]),
        ('Additive-expression', [(('Term', 'NT'), ('D', 'NT'))]),
        ('Additive-expression-prime', [(('Term-prime', 'NT'), ('D', 'NT'))]),
        ('Additive-expression-zegond', [(('Term-zegond', 'NT'), ('D', 'NT'))]),
        ('D', [(('Addop', 'NT'), ('Term', 'NT'), ('D', 'NT')),
               (('EPSILON', 'T'),)]),
        ('Addop', [(('+', 'T'),),
                   (('-', 'T'),)]),
        ('Term', [(('Factor', 'NT'), ('G', 'NT'))]),
        ('Term-prime', [(('Factor-prime', 'NT'), ('G', 'NT'))]),
        ('Term-zegond', [(('Factor-zegond', 'NT'), ('G', 'NT'))]),
        ('G', [(('*', 'T'), ('Factor', 'NT'), ('G', 'NT')),
               (('EPSILON', 'T'),)]),
        ('Factor', [(('(', 'T'), ('Expression', 'NT'), (')', 'T')),
                    (('ID', 'T'), ('Var-call-prime', 'NT')),
                    (('NUM', 'T'),)]),
        ('Var-call-prime', [(('(', 'T'), ('Args', 'NT'), (')', 'T')),
                            (('Var-prime', 'NT'),)]),
        ('Var-prime', [(('[', 'T'), ('Expression', 'NT'), (']', 'T')),
                       (('EPSILON', 'T'),)]),
        ('Factor-prime', [(('(', 'T'), ('Args', 'NT'), (')', 'T')),
                          (('EPSILON', 'T'),)]),
        ('Factor-zegond', [(('(', 'T'), ('Expression', 'NT'), (')', 'T')),
                           (('NUM', 'T'),)]),
        ('Args', [(('Arg-list', 'NT'),),
                  (('EPSILON', 'T'),)]),
        ('Arg-list', [(('Expression', 'NT'), ('Arg-list-prime', 'NT'))]),
        ('Arg-list-prime', [((',', 'T'), ('Expression', 'NT'), ('Arg-list-prime', 'NT')),
                            (('EPSILON', 'T'),)])
    ]


fafs = FirstAndFollowSets()
td = TransitionDiagrams()




def initiate_parsing():
    scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
    scanner.get_input_stream_from_input(scanner.input_address)
    children = []
    for edge in td.diagram_tuples[0][1][0]:
        if edge is not None:
            new_node = parse_diagram(edge)
            if new_node is not None:
                children.append(new_node)
    parsed_tree.children = children


def parse_diagram(diagram):
    print(f'parsing: {diagram}')
    global token_popped
    if token_popped:
        get_new_token()
        print(f'new token is: {get_token()}')
        token_popped = False
    diagram_node = Node(f'{diagram[0]}')
    if diagram[1] == 'T':
        if diagram[0] == 'EPSILON':
            diagram_node.children = [Node('epsilon')]
            return diagram_node
        if get_token() == diagram[0] or get_token_type() == diagram[0]:
            print(f'parsed {get_token()}')
            if get_token() == '$':
                diagram_node.name = '$'
                token_popped = True
                return diagram_node
            else:
                diagram_node.name = f'({get_token_type()}, {get_token()})'
                token_popped = True
                return diagram_node
        else:
           update_syntax_errors(get_token_line(), diagram[0], 'missing')
           return None
    else:
        children = []
        for sequence in td.diagram_tuples:
            if diagram[0] == sequence[0]:
                for route in sequence[1]:
                    if fafs.is_token_in_firsts(route[0][0], get_token()) or fafs.is_token_in_firsts(route[0][0], get_token_type()):
                        for edge in route:
                            new_node = parse_diagram(edge)
                            if new_node is not None:
                                children.append(new_node)

                        if children:
                            diagram_node.children = children
                            return diagram_node

                for route in sequence[1]:
                    if fafs.is_token_in_follows(diagram[0], get_token()) or fafs.is_token_in_follows(diagram[0], get_token_type()):
                        if fafs.is_token_in_firsts(diagram[0], 'EPSILON'):
                            if route[0][0] == 'EPSILON':
                                diagram_node.children = [Node('epsilon')]
                                return diagram_node

                for route in sequence[1]:
                    if fafs.is_token_in_firsts(route[0][0], 'EPSILON'):
                        for edge in route:
                            new_node = parse_diagram(edge)
                            if new_node is not None:
                                children.append(new_node)
                        diagram_node.children = children
                        return diagram_node

                if fafs.is_token_in_follows(sequence[0], get_token()) or fafs.is_token_in_follows(sequence[0], get_token_type()):
                    update_syntax_errors(get_token_line(), fafs.get_a_first(sequence[0]), 'missing')
                    return None

                if get_token_type() == 'NUM' or get_token_type() == 'ID':
                    update_syntax_errors(get_token_line(), get_token_type(), 'illegal')
                else:
                    update_syntax_errors(get_token_line(), get_token(), 'illegal')
                    token_popped = True
                    return None


initiate_parsing()

save_parsed_tree(parsed_tree_address)
save_syntax_errors(syntax_errors_address)


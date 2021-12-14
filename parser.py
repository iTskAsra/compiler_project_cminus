from anytree import Node, RenderTree
import scanner
import re

parsed_tree = Node("Program")
token = []
parsed_tree_address = "parse_tree.txt"
syntax_errors_address = "syntax_errors.txt"
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
        ('Program', ['EPSILON', 'int', 'void'],
         ['$']),

        ('Declaration_list', ['int', 'void', 'EPSILON'],
         ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'repeat', 'return']),

        ('Declaration', ['int', 'void'],
         ['int', 'void', '$', '{', '}', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM']),

        ('Declaration_initial', ['int', 'void'],
         ['(', ')', ',', ';', '[']),

        ('Declaration_prime', [';', '[', '('],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}']),

        ('Var_declaration_prime', [';', '['],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}']),

        ('Fun_declaration_prime', ['('],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}']),

        ('Type_specifier', ['int', 'void'],
         ['ID']),

        ('Params', ['int', 'void'],
         [')']),

        ('Param', ['int', 'void'],
         [',', ')']),

        ('Param_list', ['int', 'void', 'EPSILON'],
         [')']),

        ('Param_prime', ['[', 'EPSILON'],
         [',', ')']),

        ('Compound_stmt', ['{'],
         ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
          'until']),

        ('Statement_list', ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'EPSILON'],
         ['}']),

        ('Statement', ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'EPSILON'],
         ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until']),

        ('Expression_stmt', ['ID', ';', 'NUM', '(', 'break', ],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Selection_stmt', ['if'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Else_stmt', ['endif', 'else'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Iteration_stmt', ['repeat'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Return_stmt', ['return'],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Return_stmt_prime', ['ID', ';', 'NUM', '('],
         ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until"]),

        ('Expression', ['ID', 'NUM', '('],
         [";", ")", "]", ","]),

        ('B', ['ID', '[', 'NUM', '(', '<', '==', '+', '-', '*', 'EPSILON'],
         [";", ")", "]", ","]),

        ('H', ['ID', 'NUM', '(', '<', '==', '+', '-', '*', 'EPSILON'],
         [";", ")", "]", ","]),

        ('Simple_expression_zegond', ['NUM', '('],
         [";", ")", "]", ","]),

        ('Simple_expression,prime', ['(', '<', '+', '-', '*', '==', 'EPSILON'],
         [";", ")", "]", ","]),

        ('C', ['<', '==', 'EPSILON'],
         [";", ")", "]", ","]),

        ('Relop', ['<', '=='],
         ["(", "ID", "NUM"]),

        ('Additive_expression', ['ID', 'NUM', '('],
         [";", ")", "]", ","]),

        ('Additive_expression_prime', ['(', '+', '-', '*', 'EPSILON'],
         ["<", "==", ";", ")", "]", ","]),

        ('Additive_expression_zegond', ['NUM', '('],
         ["<", "==", ";", ")", "]", ","]),

        ('D', ['+', '-', 'EPSILON'],
         ["<", "==", ";", ")", "]", ","]),

        ('Addop', ['+', '-'],
         ["(", "ID", "NUM"]),

        ('Term', ['ID', 'NUM', '('],
         ["+", "-", ";", ")", "<", "==", "]", ","]),

        ('Term_prime', ['(', '*', 'EPSILON'],
         ["+", "-", "<", "==", ";", ")", "]", ","]),

        ('Term_zegond', ['NUM', '('],
         ["+", "-", "<", "==", ";", ")", "]", ","]),

        ('G', ['*', 'EPSILON'],
         ["+", "-", "<", "==", ";", ")", "]", ","]),

        ('Factor', ['ID', 'NUM', '('],
         ["*", "+", "-", ";", ")", "<", "==", "]", ","]),

        ('Var_call_prime', ['[', '{', 'EPSILON'],
         ["*", "+", "-", ";", ")", "<", "==", "]", ","]),

        ('Var_prime', ['[', 'EPSILON'],
         ["*", "+", "-", ";", ")", "<", "==", "]", ","]),

        ('Factor_prime', ['(', 'EPSILON'],
         ["*", "+", "-", "<", "==", ";", ")", "]", ","]),

        ('Factor_zegond', ['NUM', '('],
         ["*", "+", "-", "<", "==", ";", ")", "]", ","]),

        ('Args', ['ID', 'NUM', '(', 'EPSILON'],
         [')']),

        ('Arg_list', ['ID', 'NUM', '('],
         [')']),

        ('Arg_list_prime', [',', 'EPSILON'],
         [')'])
    ]

    def is_token_in_firsts(self, non_terminal, terminal):
        print(non_terminal, terminal)
        print('\n')
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                for first in pair[1]:
                    if first == terminal:
                        return True
        return False

    def is_token_in_follows(self, non_terminal, terminal):
        for pair in self.first_and_follow_sets:
            if pair[0] == non_terminal:
                for follow in pair[2]:
                    if follow == terminal:
                        return True

        return False


# in this compiler, the prediction sets are not used but the class is implemented anyways.
class PredictSets:
    prediction_sets = [
        ('Program', []),
        ('Declaration_list', []),
        ('Declaration', []),
        ('Declaration_initial', []),
        ('Declaration_prime', []),
        ('Var_declaration_prime', []),
        ('Fun_declaration_prime', []),
        ('Type_specifier', []),
        ('Params', []),
        ('Param', []),
        ('Param_list', []),
        ('Param_prime', []),
        ('Compound_stmt', []),
        ('Statement_list', []),
        ('Statement', []),
        ('Expression_stmt', []),
        ('Selection_stmt', []),
        ('Else_stmt', []),
        ('Iteration_stmt', []),
        ('Return_stmt', []),
        ('Return_stmt_prime', []),
        ('Expression', []),
        ('B', []),
        ('H', []),
        ('Simple_expression_zegond', []),
        ('Simple_expression,prime', []),
        ('C', []),
        ('Relop', []),
        ('Additive_expression', []),
        ('Additive_expression_prime', []),
        ('Additive_expression_zegond', []),
        ('D', []),
        ('Addop', []),
        ('Term', []),
        ('Term_prime', []),
        ('Term_zegond', []),
        ('G', []),
        ('Factor', []),
        ('Var_call_prime', []),
        ('Var_prime', []),
        ('Factor_prime', []),
        ('Factor_zegond', []),
        ('Args', []),
        ('Args_list', []),
        ('Args_list_prime', [])
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
        ('Program', [(('Declaration_list', 'NT'), ('$', 'T'))]),
        ('Declaration_list', [(('Declaration', 'NT'), ('Declaration_list', 'NT')),
                              (('EPSILON', 'T'),)]),
        ('Declaration', [(('Declaration_initial', 'NT'), ('Declaration_prime', 'NT'))]),
        ('Declaration_initial', [(('Type_specifier', 'NT'), ('ID', 'T'))]),
        ('Declaration_prime', [(('Fun_declaration_prime', 'NT'),),
                               (('Var_declaration_prime', 'NT'),)]),
        ('Var_declaration_prime', [(('[', 'T'), ('NUM', 'T'), (']', 'T'), (';', 'T')),
                                   ((';', 'T'),)]),
        ('Fun_declaration_prime', [(('(', 'T'), ('Params', 'NT'), (')', 'T'), ('Compound_stmt', 'NT'))]),
        ('Type_specifier', [(('int', 'T'),),
                            (('void', 'T'),)]),
        ('Params', [(('int', 'T'), ('ID', 'T'), ('Param_prime', 'NT'), ('Param_list', 'NT')),
                    (('void', 'T'),)]),
        ('Param_list', [((',', 'T'), ('Param', 'NT'), ('Param_list', 'NT')),
                        (('EPSILON', 'T'),)]),
        ('Param', [(('Declaration_initial', 'NT'),)]),
        ('Param_prime', [(('[', 'T'), (']', 'T')),
                         (('EPSILON', 'T'),)]),
        ('Compound_stmt', [(('{', 'T'), ('Declaration_list', 'NT'), ('Statement_list', 'NT'), ('}', 'T'))]),
        ('Statement_list', [(('Statement', 'NT'), ('Statement_list', 'NT')),
                            (('EPSILON', 'T'),)]),
        ('Statement',
         [(('Expression_stmt', 'NT'), ('Compound_stmt', 'NT'), ('Selection_stmt', 'NT'), ('Iteration_stmt', 'NT'), ('Return_stmt', 'NT'))]),
        ('Expression_stmt', [(('Expression', 'NT'), (';', 'T')),
                             (('break', 'T'), (';', 'T')),
                             ((';', 'T'),)]),
        ('Selection_stmt', [(('if', 'T'), ('(', 'T'), ('Expression', 'NT'), (')', 'T'), ('Statement', 'NT'), ('Else_stmt', 'NT'))]),
        ('Else_stmt', [(('else', 'T'), ('Statement', 'NT'), ('endif', 'T')),
                       (('endif', 'T'),)]),
        ('Iteration_stmt', [(('repeat', 'T'), ('Statement', 'NT'), ('until', 'T'), ('(', 'T'), ('Expression', 'NT'), (')', 'T'))]),
        ('Return_stmt', [(('return', 'T'), ('Return_stmt_prime', 'NT'))]),
        ('Return_stmt_prime', [(('Expression', 'NT'), (';', 'T')),
                               ((';', 'T'),)]),
        ('Expression', [(('ID', 'T'), ('B', 'NT')),
                        (('Simple_expression_zegond', 'NT'),)]),
        ('B', [(('[', 'T'), ('Expression', 'NT'), (']', 'T'), ('H', 'NT')),
               (('=', 'T'), ('Expression', 'NT')),
               (('Simple_expression_prime', 'NT'),)]),
        ('H', [(('=', 'T'), ('Expression', 'NT')),
               (('G', 'NT'), ('D', 'NT'), ('C', 'NT'))]),
        ('Simple_expression_zegond', [(('Additive_expression_zegond', 'NT'), ('C', 'NT'))]),
        ('Simple_expression_prime', [(('Additive_expression_prime', 'NT'), ('C', 'NT'))]),
        ('C', [(('Relop', 'NT'), ('Additive_expression', 'NT')),
               (('EPSILON', 'T'),)]),
        ('Relop', [(('<', 'T'),),
                   (('==', 'T'),)]),
        ('Additive_expression', [(('Term', 'NT'), ('D', 'NT'))]),
        ('Additive_expression_prime', [(('Term_prime', 'NT'), ('D', 'NT'))]),
        ('Additive_expression_zegond', [(('Term_zegond', 'NT'), ('D', 'NT'))]),
        ('D', [(('Addop', 'NT'), ('Term', 'NT'), ('D', 'NT')),
               (('EPSILON', 'T'),)]),
        ('Addop', [(('+', 'T'),),
                   (('-', 'T'),)]),
        ('Term', [(('Factor', 'NT'), ('G', 'NT'))]),
        ('Term_prime', [(('Factor_prime', 'NT'), ('G', 'NT'))]),
        ('Term_zegond', [(('Factor_prime', 'NT'), ('G', 'NT'))]),
        ('G', [(('*', 'T'), ('Factor', 'NT'), ('G', 'NT')),
               (('EPSILON', 'T'),)]),
        ('Factor', [(('(', 'T'), ('Expression', 'NT'), (')', 'T')),
                    (('ID', 'T'), ('Var_call_prime', 'NT')),
                    (('NUM', 'T'),)]),
        ('Var_call_prime', [(('(', 'T'), ('Args', 'NT'), (')', 'T')),
                            (('Var_prime', 'NT'),)]),
        ('Var_prime', [(('[', 'T'), ('Expression', 'NT'), (']', 'T')),
                       (('EPSILON', 'T'),)]),
        ('Factor_prime', [(('(', 'T'), ('Args', 'NT'), (')', 'T')),
                          (('EPSILON', 'T'),)]),
        ('Factor_zegond', [(('(', 'T'), ('Expression', 'NT'), (')', 'T')),
                           (('NUM', 'T'),)]),
        ('Args', [(('Args_list', 'NT'),),
                  (('EPSILON', 'T'),)]),
        ('Arg_list', [(('Expression', 'NT'), ('Args_list_prime', 'NT'))]),
        ('Arg_list_prime', [((',', 'T'), ('Expression', 'NT'), ('Arg_list_prime', 'NT')),
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
    global token_popped
    if token_popped:
        get_new_token()
        token_popped = False
    diagram_node = Node(f'{diagram[0]}')
    if diagram[1] == 'T':
        if get_token() == diagram[0] or get_token_type() == diagram[0]:
            if get_token() == diagram[0] or get_token_type() == diagram[0]:
                diagram_node.name = f'{get_token_type()}, {get_token()}'
                token_popped = True
                return diagram_node
            else:
                diagram_node.name = '$'
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
                    if route[0][1] == 'NT':
                        if fafs.is_token_in_firsts(route[0][0], get_token()) or fafs.is_token_in_firsts(route[0][0], get_token_type()):
                            for edge in route:
                                if edge is not None:
                                    new_node = parse_diagram(edge)
                                    # print(edge)
                                    # print(new_node)
                                    # print(token)
                                    # print('\n')
                                    if new_node is not None:
                                        children.append(new_node)
                            if children:
                                diagram_node.children = children
                                return diagram_node
                        elif fafs.is_token_in_follows(route[0][0], get_token()) or fafs.is_token_in_follows(route[0][0], get_token_type()):
                            if fafs.is_token_in_firsts(route[0][0], 'EPSILON'):
                                diagram_node.children = [Node('epsilon')]
                                return diagram_node
                            else:
                                update_syntax_errors(get_token_line(), route[0][0], 'missing')
                                return None
                        else:
                            if get_token_type() == 'NUM' or get_token_type() == 'ID':
                                update_syntax_errors(get_token_line(), get_token_type(), 'illegal')
                            else:
                                update_syntax_errors(get_token_line(), get_token(), 'illegal')
                            token_popped = True
                            return None



initiate_parsing()
# print(RenderTree(parsed_tree))


save_parsed_tree(parsed_tree_address)

print(fafs.is_token_in_firsts('Fun_declaration_prime', '('))
print(fafs.is_token_in_firsts('(', '('))

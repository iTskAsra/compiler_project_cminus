from anytree import Node, RenderTree
import scanner

parsed_tree = Node("Program")
token = []
parsed_tree_address = "parse_tree.txt"
syntax_errors_address = "syntax_errors.txt"
syntax_errors = []
error_raised = False
current_line = 1


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
    with open(address, 'w') as f:
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
        ('Program', [], []),
        ('Declaration_list', [], []),
        ('Declaration', [], []),
        ('Declaration_initial', [], []),
        ('Declaration_prime', [], []),
        ('Var_declaration_prime', [], []),
        ('Fun_declaration_prime', [], []),
        ('Type_specifier', [], []),
        ('Params', [], []),
        ('Param', [], []),
        ('Param_list', [], []),
        ('Param_prime', [], []),
        ('Compound_stmt', [], []),
        ('Statement_list', [], []),
        ('Statement', [], []),
        ('Expression_stmt', [], []),
        ('Selection_stmt', [], []),
        ('Else_stmt', [], []),
        ('Iteration_stmt', [], []),
        ('Return_stmt', [], []),
        ('Return_stmt_prime', [], []),
        ('Expression', [], []),
        ('B', [], []),
        ('H', [], []),
        ('Simple_expression_zegond', [], []),
        ('Simple_expression,prime', [], []),
        ('C', [], []),
        ('Relop', [], []),
        ('Additive_expression', [], []),
        ('Additive_expression_prime', [], []),
        ('Additive_expression_zegond', [], []),
        ('D', [], []),
        ('Addop', [], []),
        ('Term', [], []),
        ('Term_prime', [], []),
        ('Term_zegond', [], []),
        ('G', [], []),
        ('Factor', [], []),
        ('Var_call_prime', [], []),
        ('Var_prime', [], []),
        ('Factor_prime', [], []),
        ('Factor_zegond', [], []),
        ('Args', [], []),
        ('Args_list', [], []),
        ('Args_list_prime', [], []),
        ('Args_list_prime', [], [])
    ]

    def is_token_in_firsts(self, non_terminal, terminal):
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
        ('Args_list_prime', []),
        ('Args_list_prime', [])
    ]

    def is_token_in_predicts(self, non_terminal, terminal):
        for pair in self.prediction_sets:
            if pair[0] == non_terminal:
                for prediction in pair[1]:
                    if prediction == terminal:
                        return True

        return False

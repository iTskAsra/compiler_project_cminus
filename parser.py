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
            f.write("%s%s\n" % (pre,node.name))


def initialize_errors_file(address):
    with open(address, 'w') as f:
        f.write("There is no syntax error.")


def update_syntax_errors(line, terminal, error_description):
    syntax_errors.append([line, terminal, error_description])


def save_syntax_errors(address):
    with open(address, 'w') as f:
        for error in syntax_errors:
            f.write(f"#{error[0]} : syntax error, {error[2]} {error[1]}\n")




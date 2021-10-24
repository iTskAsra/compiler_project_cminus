tokens_address = "tokens.txt"
lex_errors_address = "lexical_errors.txt"
symbol_table_address = "symbol_table.txt"
input_address = "input.txt"
current_line = 1
error_raised = 'false'
symbol_table_elements = [
    "if", "else", "void", "int", "repeat", "return", "until", "break"
]
lexical_errors = [[]]
tokens = [[]]


def initiate_new_line(current_line):
    tokens.append([])
    lexical_errors.append([])
    return current_line + 1


def update_symbol_table(element):
    for i in range(len(symbol_table_elements)):
        if element == symbol_table_elements[i]:
            return 1

    symbol_table_elements.append(element)
    return 0


def update_tokens(line, token, ttype):
    tokens[line - 1].append((token, ttype))


def update_errors(line, error, error_description):
    lexical_errors[line - 1].append((error, error_description))


def save_symbol_table(address):
    with open(address, 'w') as f:
        for i in range(len(symbol_table_elements)):
            f.write(f"{i + 1}.\t{symbol_table_elements[i]}\n")


def save_errors(address):
    if error_raised:
        with open(address, 'w') as f:
            for i in range(current_line - 1):
                if not lexical_errors[i]:
                    continue
                f.write(f"{i + 1}.\t{lexical_errors[i]}\n")


def save_tokens(address):
    with open(address, 'w') as f:
        for i in range(current_line - 1):
            if not tokens[i]:
                continue
            f.write(f"{i + 1}.\t{tokens[i]}\n")


def initiate_lexical_errors_file(address):
    with open(address, 'w') as f:
        f.write("There is no lexical error.")


save_symbol_table(symbol_table_address)
initiate_lexical_errors_file(lex_errors_address)
with open(input_address, 'rb') as f:
    input_stream = (f.read(50000)).decode()

test_array = [[("hello", 23), ("dayum", 33)], [], [], [("yo", 13)]]
for i in range(4):
    if not test_array[i]:
        continue
    print(f"{i+1}.\t{test_array[i]}")
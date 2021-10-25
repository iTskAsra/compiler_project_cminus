import re

tokens_address = "tokens.txt"
lex_errors_address = "lexical_errors.txt"
symbol_table_address = "symbol_table.txt"
input_address = "input.txt"
current_line = 1
input_stream_pointer = 0
error_raised = True
symbol_table_elements = [
    "if", "else", "void", "int", "repeat", "return", "until", "break"
]
lexical_errors = [[]]
tokens = [[]]

# rexp compilations:
white_space_rexp = re.compile(r'\n|\t|\f|\r|\v|\s')
symbol_rexp = re.compile(r'/|;|:|,|{|}|\[|]|=|==|\+|-|(|)|\*|<')
alphabet_rexp = re.compile(r'[A-Za-z]')
num_rexp = re.compile(r'[0-9]')
valid_inputs = re.compile(r"[A-Za-z]|[0-9]|;|:|,|\[|\]|\(|\)|{|}|\+|-|\*|=|<|==|/|\n|\r|\t|\v|\f|\s")
keywords = (r'if|else|int|repeat|break|void|until')


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


# test_array = [[("hello", 23), ("dayum", 33)], [], [], [("yo", 13)]]
# for i in range(4):
#    if not test_array[i]:
#        continue
#    for arr in test_array[i]:
#        x, y = arr
#        print

def check_white_space(char):
    if char == "\n":
        global current_line
        current_line += 1
    return re.match(white_space_rexp, char)


def start_state():
    global error_raised, input_stream_pointer
    while input_stream[input_stream_pointer]:
        if check_white_space(input_stream[input_stream_pointer]):
            input_stream_pointer += 1
            continue
        if re.match(input_stream[input_stream_pointer], symbol_rexp):
            symbol_state()
            break
        elif re.match(input_stream[input_stream_pointer], num_rexp):
            num_state()
            break
        elif re.match(input_stream[input_stream_pointer], alphabet_rexp):
            keyword_or_id_state()
            break
        elif input_stream[input_stream_pointer] == "/":
            comment_state()
            break
        else:
            update_errors(current_line, input_stream[input_stream_pointer], "Invalid input")
            error_raised = True


def symbol_state():
    global input_stream_pointer
    if input_stream[input_stream_pointer] == "=":
        if input_stream[input_stream_pointer + 1]:
            if input_stream[input_stream_pointer + 1] == "=":
                update_tokens(current_line, "==", "SYMBOL")
                input_stream_pointer += 2
                return
    else:
        update_tokens(current_line, input_stream[input_stream_pointer], "SYMBOL")
        input_stream_pointer += 1
        return


def num_state():
    global input_stream_pointer, error_raised
    num = ""
    num += (input_stream[input_stream_pointer])
    input_stream_pointer += 1
    while True:
        if re.match(input_stream[input_stream_pointer], num_rexp):
            num += (input_stream[input_stream_pointer])
            input_stream_pointer += 1
            continue
        elif re.match(alphabet_rexp, input_stream[input_stream_pointer]):
            update_errors(current_line, num + input_stream[input_stream_pointer], "Invalid number")
            error_raised = True
            input_stream_pointer += 1
            return
        elif re.match(valid_inputs, input_stream[input_stream_pointer]):
            if check_white_space(input_stream[input_stream_pointer]):
                input_stream_pointer += 1
            update_tokens(current_line, num, "NUM")
            # input_stream_pointer += 1
            return
        else:
            update_tokens(current_line, num, "NUM")
            update_errors(current_line, input_stream[input_stream_pointer], "Invalid input")
            error_raised = True
            input_stream_pointer += 1
            return


def keyword_or_id_state():
    global input_stream_pointer, error_raised
    keyword_or_id = ""
    keyword_or_id += input_stream[input_stream_pointer]
    input_stream_pointer += 1
    while True:
        if re.match(alphabet_rexp, input_stream[input_stream_pointer]) or re.match(num_rexp,
                                                                                   input_stream[input_stream_pointer]):
            keyword_or_id += input_stream[input_stream_pointer]
            input_stream_pointer += 1
            continue
        elif re.match(symbol_rexp, input_stream[input_stream_pointer]) or check_white_space(
                input_stream[input_stream_pointer]):
            if re.match(keywords, keyword_or_id):
                update_tokens(current_line, keyword_or_id, "KEYWORD")
            else:
                update_tokens(current_line, keyword_or_id, "ID")
            update_symbol_table(keyword_or_id)
            if re.match(white_space_rexp, input_stream[input_stream_pointer]):
                input_stream_pointer += 1
            return
        else:
            if re.match(keywords, keyword_or_id):
                update_tokens(current_line, keyword_or_id, "KEYWORD")
            else:
                update_tokens(current_line, keyword_or_id, "ID")
            update_symbol_table(keyword_or_id)
            update_errors(current_line, input_stream[input_stream_pointer], "Invalid input")
            error_raised = True
            input_stream_pointer += 1
            return


def comment_state():
    global input_stream_pointer

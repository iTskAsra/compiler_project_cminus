import re

# regular expression compilations:
white_space_rexp = re.compile(r'\n|\t|\f|\r|\v|\s')
symbol_rexp = re.compile(r'/|;|:|,|{|}|\[|]|=|==|\+|-|(|)|\*|<')
alphabet_rexp = re.compile(r'[A-Za-z]')
num_rexp = re.compile(r'[0-9]')
valid_inputs = re.compile(r"[A-Za-z]|[0-9]|;|:|,|\[|\]|\(|\)|{|}|\+|-|\*|=|<|==|/|\n|\r|\t|\v|\f|\s")
keywords = re.compile(r'if|else|int|repeat|break|void|until')

# scanner variables
tokens_address = "tokens.txt"
lex_errors_address = "lexical_errors.txt"
symbol_table_address = "symbol_table.txt"
input_address = "input.txt"
current_line = 1
input_stream_pointer = 0
new_token = ""
input_stream = ""
eof_flag = False
unseen_token = False
error_raised = False
lexical_errors = [[]]
tokens = [[]]
symbol_table_elements = [
    "if", "else", "void", "int", "repeat", "return", "until", "break"
]


def update_symbol_table(element):
    for i in range(len(symbol_table_elements)):
        if element == symbol_table_elements[i]:
            return 1

    symbol_table_elements.append(element)
    return 0


def update_tokens(line, token, ttype):
    global unseen_token, new_token
    tokens[line - 1].append((token, ttype))
    unseen_token = True
    new_token = str(f"({token}, {ttype})")


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


def get_input_stream_from_input(address):
    global input_stream
    with open(address, 'rb') as f:
        input_stream = (f.read(50000)).decode()


def check_white_space(char):
    if char == "\n":
        global current_line
        current_line += 1
    return re.match(white_space_rexp, char)


def start_state():
    global error_raised, input_stream_pointer, new_token, eof_flag
    if not input_stream[input_stream_pointer]:
        eof_flag = True
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
            break


def symbol_state():
    global input_stream_pointer, error_raised
    if input_stream[input_stream_pointer] == "=":
        if input_stream[input_stream_pointer + 1]:
            if input_stream[input_stream_pointer + 1] == "=":
                update_tokens(current_line, "==", "SYMBOL")
                input_stream_pointer += 2
                return
    elif input_stream[input_stream_pointer] == "*" and input_stream[input_stream_pointer + 1] == "/":
        update_errors(current_line, "*/", "Unmatched comment")
        error_raised = True
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
    global input_stream_pointer, error_raised
    comment = ""
    input_stream_pointer += 1
    if input_stream[input_stream_pointer] == "/":
        input_stream_pointer += 1
        while True:
            if (input_stream[input_stream_pointer] == "\n") or (not input_stream[input_stream_pointer]):
                check_white_space(input_stream[input_stream_pointer])
                input_stream_pointer += 1
                return
            else:
                comment += input_stream[input_stream_pointer]
                input_stream_pointer += 1
                continue
    elif input_stream[input_stream_pointer] == "*":
        input_stream_pointer += 1
        while True:
            if input_stream[input_stream_pointer] == "*" and input_stream[input_stream_pointer + 1] == "/":
                input_stream_pointer += 2
                return
            elif not input_stream[input_stream_pointer]:
                update_errors(current_line, f"{comment[0:7]}...", "Unclosed comment")
                error_raised = True
                return
            else:
                comment += input_stream[input_stream_pointer]
                check_white_space(input_stream[input_stream_pointer])
                input_stream_pointer += 1


def get_next_token():
    global unseen_token, new_token
    while not unseen_token:
        start_state()
    if eof_flag:
        return ''
    unseen_token = False
    return new_token

# Created by: Kasra Amani
# Student ID: 98101171
#کسری امانی
import scanner

scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
scanner.get_input_stream_from_input(scanner.input_address)
tokens = []
while True:
    if scanner.eof_flag:
        break
    token = scanner.get_next_token()
    tokens.append(token)

print(scanner.get_next_token())
print(scanner.get_next_token())

print(scanner.get_next_token())

print(scanner.get_next_token())

if scanner.error_raised:
    scanner.save_errors(scanner.lex_errors_address)

with open(scanner.tokens_address, 'w') as f:
    current_line = 1
    lines_first_token = True
    no_line_written_yet = True
    for token in tokens:
        if not token:
            break
        line_number = token[0]
        token_name = token[1]
        token_type = token[2]
        while line_number != current_line:
            current_line += 1
            lines_first_token = True
        if lines_first_token:
            lines_first_token = False
            if current_line != 1 and (not no_line_written_yet):
                f.write("\n")
            f.write(f"{current_line}.\t")
        f.write(f"({token_type}, {token_name}) ")
        no_line_written_yet = False

scanner.save_symbol_table(scanner.symbol_table_address)

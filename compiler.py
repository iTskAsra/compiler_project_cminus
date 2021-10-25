import scanner
import parser

scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
scanner.get_input_stream_from_input(scanner.input_address)
tokens = []
while True:
    token = scanner.get_next_token()
    tokens.append(token)
    #print(token)
    if not token:
        break

print("hello")
if scanner.error_raised:
    scanner.save_errors(scanner.lex_errors_address)

with open(scanner.tokens_address, 'w') as f:
    print("hello2")
    current_line = 1
    lines_first_token = True
    for token in tokens:
        if not token:
            break
        line_number = token[0]
        token_name = token[1]
        token_type = token[2]
        print(token_name)
        print(token)
        while line_number != current_line:
            current_line += 1
            lines_first_token = True
        if lines_first_token:
            lines_first_token = False
            if current_line != 1:
                f.write(f"\n{current_line}.\t")
        f.write(f"({token_type}, {token_name}) ")

scanner.save_symbol_table(scanner.symbol_table_address)

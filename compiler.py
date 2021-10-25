import scanner
import parser

scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
scanner.get_input_stream_from_input(scanner.input_address)
while True:
    result = scanner.get_next_token()
    if not result:
        break
    print(result)

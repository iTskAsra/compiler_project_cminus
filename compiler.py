# Created by: Kasra Amani
# Student ID: 98101171

import scanner
import parser

scanner.initiate_lexical_errors_file(scanner.lex_errors_address)
scanner.get_input_stream_from_input(scanner.input_address)


if scanner.error_raised:
    scanner.save_errors(scanner.lex_errors_address)

scanner.save_symbol_table(scanner.symbol_table_address)

parser.initiate_parsing()
parser.save_syntax_errors(parser.syntax_errors_address)
parser.save_parsed_tree(parser.parsed_tree_address)

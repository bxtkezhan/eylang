#! /usr/bin/env python3
from eylanglexer import lexer
from eylangparser import parser

import fire


def main(filename):
    with open(filename, encoding='utf-8') as f:
        code = f.read()
    parser.parse(lexer.lex(code)).eval()

if __name__ == '__main__':
    fire.Fire(main)

# -*- coding: utf-8 -*-
import argparse


def main():
    arg_parser = argparse.ArgumentParser(prog='ggrupus', description='Clone gitlab repositories by group ID')
    arg_parser.add_argument('-r', '--recursive', help='Recursively clone repositories')
    arg_parser.add_argument('_gitlab_session', help='Gitlab session cookie')
    arg_parser.add_argument('group_id', help='The gitlab group ID we want to scrape')
    args = arg_parser.parse_args()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import requests
import subprocess
import argparse
import sys
import os

GITLAB_API = '/api/v4'


def clone_repo(url, path):
    os.makedirs(path, exist_ok=True)
    subprocess.run(['git', 'clone', url, path])


def get_subgroups_for_group(domain, cookies, group_id, recursive, insecure):
    try:
        r = requests.get('https://{}{}/groups/{}/subgroups'.format(domain, GITLAB_API, group_id), cookies=cookies, verify=not insecure)
        if r.status_code != 200:
            print('Wrong group id {}...'.format(group_id))
            return []
        for subgroup in r.json():
            get_repos_for_group(domain, cookies, subgroup['id'], recursive, insecure)
    except requests.exceptions.SSLError:
        print('[x] SSL error, you\'re either being MitM\'d or the target domain uses a self-signed certificate.')
        print('    If it is the latter, consider using -i/--insecure...')


def get_repos_for_group(domain, cookies, group_id, recursive, insecure):
    print('Checking repos for {}...'.format(group_id))
    try:
        r = requests.get('https://{}{}/groups/{}'.format(domain, GITLAB_API, group_id), cookies=cookies, verify=not insecure)
        if r.status_code != 200:
            print('Wrong group id or invalid session...')
            sys.exit(-1)
        for project in r.json()['projects']:
            clone_repo(project['ssh_url_to_repo'], project['path_with_namespace'])
        if recursive:
            get_subgroups_for_group(domain, cookies, group_id, recursive, insecure)
    except requests.exceptions.SSLError:
        print('[x] SSL error, you\'re either being MitM\'d or the target domain uses a self-signed certificate.')
        print('    If it is the latter, consider using -i/--insecure...')


def main():
    arg_parser = argparse.ArgumentParser(prog='ggrupus', description='Clone gitlab repositories by group ID')
    arg_parser.add_argument('-r', '--recursive', help='Recursively clone repositories', default=False, action='store_true')
    arg_parser.add_argument('-u', '--url', help='Set domain (defaults to gitlab.com)', default='gitlab.com')
    arg_parser.add_argument('-i', '--insecure', help='Disable TLS certificate check', default=False, action='store_true')
    arg_parser.add_argument('_gitlab_session', help='Gitlab session cookie')
    arg_parser.add_argument('group_id', help='The gitlab group ID we want to scrape')
    args = arg_parser.parse_args()
    cookies = {'_gitlab_session': args._gitlab_session}
    get_repos_for_group(args.url, cookies, args.group_id, args.recursive, args.insecure)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import requests
import subprocess
import argparse
import sys
import os

GITLAB_URL = 'https://gitlab.com/api/v4'


def clone_repo(url, path):
    os.makedirs(path, exist_ok=True)
    subprocess.run(['git', 'clone', url, path])


def get_subgroups_for_group(cookies, group_id, recursive):
    r = requests.get('{}/groups/{}/subgroups'.format(GITLAB_URL, group_id), cookies=cookies)
    if r.status_code != 200:
        print('Wrong group id {}...'.format(group_id))
        return []
    for subgroup in r.json():
        get_repos_for_group(cookies, subgroup['id'], recursive)


def get_repos_for_group(cookies, group_id, recursive):
    print('Checking repos for {}...'.format(group_id))
    r = requests.get('{}/groups/{}'.format(GITLAB_URL, group_id), cookies=cookies)
    if r.status_code != 200:
        print('Wrong group id or invalid session...')
        sys.exit(-1)
    for project in r.json()['projects']:
        clone_repo(project['ssh_url_to_repo'], project['path_with_namespace'])
    if recursive:
        get_subgroups_for_group(cookies, group_id, recursive)


def main():
    arg_parser = argparse.ArgumentParser(prog='ggrupus', description='Clone gitlab repositories by group ID')
    arg_parser.add_argument('-r', '--recursive', help='Recursively clone repositories', default=False, action='store_true')
    arg_parser.add_argument('_gitlab_session', help='Gitlab session cookie')
    arg_parser.add_argument('group_id', help='The gitlab group ID we want to scrape')
    args = arg_parser.parse_args()

    cookies = {'_gitlab_session': args._gitlab_session}
    get_repos_for_group(cookies, args.group_id, args.recursive)


if __name__ == '__main__':
    main()

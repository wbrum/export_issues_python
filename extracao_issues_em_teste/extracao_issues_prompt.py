#!/usr/bin/env python
# export github issues to a csv file
import json
import requests
import csv
import getpass
from StringIO import StringIO
import argparse
import sys


def get_issues(user, repo, org, password):
    data = []
    url = "https://api.github.com/repos/gems-uff/noworkflow/issues".format(org=org, repo=repo)
    while True:
        response = requests.get(url, auth=(user,password))
        if response.ok:
            decoded = json.load(StringIO(response.text))
            new_data = [[issue['number'], issue['title'], issue['body'], ' '.join([label['name'] for label in issue['labels']]), issue['user']['login']] for issue in decoded]
            data = data + new_data
            pr('.')
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            raise requests.HTTPError("{status_code}: {message}".format(status_code=response.status_code, message=response.json['message']))
        pr('\n\n')
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Get issues from a github repo, and export them as csv")
    parser.add_argument('-u', '--user', dest='user', help="The github user to log in as")
    parser.add_argument('-p', '--password', dest='password', help="The password for said user")
    parser.add_argument('-z', '--org', dest='org', help="The organization the repo belongs to")
    parser.add_argument('-r', '--repo', dest='repo', help="the repo to query for issues")
    parser.add_argument('-q', '--quiet', dest='q', action='store_true', help="quiet output - no progress prompts")
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-o', '--output', dest='output', help="output file (default is <repo>_issues.csv).")
    output_group.add_argument('--stdout', dest='stdout', action='store_true')
    parsed_args = parser.parse_args()
    user = parsed_args.user if parsed_args.user else raw_input("Github User: ")
    password = parsed_args.password if parsed_args.password else getpass.getpass(prompt="Github password: ")
    org = parsed_args.org if parsed_args.org else raw_input("Github org: ")
    repo = parsed_args.repo if parsed_args.repo else raw_input("Github repo: ")
    if parsed_args.q:
        pr = lambda x: None
    else:
        def pr(msg):
            sys.stdout.write(msg)
            sys.stdout.flush()
    if not parsed_args.stdout:
        output_filename = "{repo}_issues.csv".format(repo=repo)
        fp = open(output_filename, 'wb')
    else:
        fp = sys.stdout

    pr("Getting data: \n")
    data = get_issues(user, 'media-pop', 'mediapop', password)
    headers = ['issue_no', 'title', 'body', 'labels', 'user']
    try:
        output = csv.writer(fp, delimiter=',')
        output.writerow(headers)
        output.writerows(data)
    finally:
        fp.close()
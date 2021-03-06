"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests


GITHUB_USER = 'wbrum'
GITHUB_PASSWORD = 'TSIrkBq0XvNH5fvuIz3L'
REPO = 'gems-uff/noworkflow'  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?state=all' % REPO
STATE = "?state=all"
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    "output a list of issues to csv"
    if not response.status_code == 200:
        raise Exception(response.status_code)
    for issue in r.json():
        labels = issue['labels']
        for label in labels:
                csvout.writerow([issue['number'], issue['title'].encode('utf-8'), issue['body'].encode('utf-8'),issue['state'], issue['created_at'], issue['updated_at'],issue['closed_at'], ' '.join([label['name'] for label in issue['labels']]), issue['user']['login']])


r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'wb'))
csvout.writerow(('id', 'Title', 'Body', 'State', 'Created At', 'Updated At','Closed At', 'Labels', 'User'))
write_issues(r)

if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    print "***"
    print pages
    while 'last' in pages and 'next' in pages:
        print pages['next']
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)
        if pages['next'] == pages['last']:
            break
        pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
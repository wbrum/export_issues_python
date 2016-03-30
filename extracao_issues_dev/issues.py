import csv
import github3

# api settings for github
git_username = 'wbrum'
git_api_token = 'd3f89dd7214b90ac3718a013bcd574f9864c75b9'
git_repo = 'https://github.com/gems-uff/noworkflow'
state = 'open' # 'open' or 'closed'

# csv name
csv_name = "git_hub_issues.csv"

def run_csv():
    """
    Export github issues into a csv format
    """
    output_csv = csv.writer(open(csv_name, 'wb'), delimiter=',')
    github = github3.login(username=git_username, token=git_api_token)

    # csv headers
    headers = [
        'id',
        'title',
        'body',
        'state',
        'creator',
        'labels',
        'created_at',
        'updated_at',
        'closed_at',
    ]

    # write header rows
    output_csv.writerow(headers)

    # get the git issues and write the rows to the csv
    git_issues = github.iter_repo_issues('gems-uff','noworkflow','*')
    for git_issue in git_issues:
        print git_issue.title
        labels = ' '.join(git_issue.labels)

        # alot of these are blank because they are not really 
        # needed but if you need them just fill them out
        issue = [
            git_issue.number,
            git_issue.title.encode('utf8'),
            git_issue.body.encode('utf8'),
            git_issue.state, 
            git_issue.user, 
            labels,
            git_issue.created_at,
            git_issue.updated_at,
            git_issue.closed_at,
        ]
        output_csv.writerow(issue)

if __name__ == '__main__':
    run_csv()
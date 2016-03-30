# coding=utf-8
import csv
import github3

git_username = 'wbrum'
git_api_token = '1d031b21a0a9cd15803ef7f7b32e3627d0f666e1'
git_repo = 'https://github.com/gems-uff/noworkflow'
state = 'all'  # 'open','closed' ou 'all'

# csv name
csv_name = "git_hub_issues.csv"


def run_csv():
    # Exporta issues de um repositório em formato CSV

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
        'assignee',
    ]

    # escreve header rows
    output_csv.writerow(headers)

    # pega issues e transcreve para csv
    git_issues = github.iter_repo_issues('gems-uff', 'noworkflow', '', state)
    for git_issue in git_issues:
        print git_issue.title
        #   labels = ' '.join(git_issue.labels.color) #problema aqui

        issue = [
            git_issue.number,
            git_issue.title.encode('utf8'),
            git_issue.body.encode('utf8'),
            git_issue.state,
            git_issue.user,
            git_issue.labels,
            git_issue.created_at,
            git_issue.updated_at,
            git_issue.closed_at,
            git_issue.assignee,
        ]
        output_csv.writerow(issue)


if __name__ == '__main__':
    run_csv()

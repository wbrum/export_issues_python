# coding=utf-8
import csv
import github3

git_username = 'wbrum'
git_api_token = '1d031b21a0a9cd15803ef7f7b32e3627d0f666e1'
git_repo = 'https://github.com/gems-uff/noworkflow'

# csv name
csv_name = "git_hub_commits.csv"


def run_csv():
    # Exporta commits de um repositório em formato CSV

    output_csv = csv.writer(open(csv_name, 'wb'), delimiter=',')
    github = github3.login(username=git_username, token=git_api_token)

    # csv headers
    headers = [
        'sha',
        'author',
        'message',

    ]

    # escreve header rows
    output_csv.writerow(headers)

    # baixa issues e transcreve para csv
    git_commits = github.repository("gems-uff", "noworkflow").iter_commits()
    for git_commit in git_commits:
        print git_commit.commit.message
        commit = [
            git_commit.sha,
            git_commit.author,
            git_commit.commit.message.encode('utf8'),

        ]
        output_csv.writerow(commit)


if __name__ == '__main__':
    run_csv()

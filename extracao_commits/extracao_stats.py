# coding=utf-8
import csv
import github3

git_username = 'wbrum'
git_api_token = '0ca9fb9a09e516190d0e6375b814bf20873c4378'
git_repo = 'https://github.com/gems-uff/noworkflow'

# csv name
csv_name = "git_hub_stats.csv"


def run_csv():
    # Exporta estatísticas de um repositório em formato CSV

    output_csv = csv.writer(open(csv_name, 'wb'), delimiter=',')
    github = github3.login(username=git_username, token=git_api_token)

    # csv headers
    headers = [
        'author',
        'total',
        'Start of the Week',
        'Deletions',
        'Additions',
        'Commits',

    ]

    # escreve header rows
    output_csv.writerow(headers)

    # baixa estatísticas do repositório e transcreve para csv
    git_stats = github.repository("gems-uff", "noworkflow").iter_contributor_statistics()
    for git_stat in git_stats:
        for git_week in git_stat.alt_weeks:
            commit = [
                git_stat.author,
                git_stat.total,
                git_week['start of week'],
                git_week['deletions'],
                git_week['additions'],
                git_week['commits'],
            ]
            output_csv.writerow(commit)


if __name__ == '__main__':
    run_csv()

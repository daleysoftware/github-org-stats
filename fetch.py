import os
import sys
import datetime
import github


def main(github_organization, github_token):
    api_client = github.Github(github_token)
    repos = api_client.get_organization(github_organization).get_repos()

    for repo in repos:
        # Only inspect private repos and repos that have been updated in the last 60 days.
        print(repo)
        print(repo.updated_at)
        if repo.private and repo.updated_at > datetime.datetime.now() + datetime.timedelta(-60):
            """
            print(repo)
            print(repo.get_stats_contributors()[0].weeks)
            """
            # TODO aggregate this so it is useful and actionable


def usage():
    print("Usage: python3 %s <organization_name>" % sys.argv[0])
    sys.exit(1)


if __name__ == '__main__':
    if 'GITHUB_TOKEN' not in os.environ:
        usage()
    if len(sys.argv) != 2:
        usage()
    main(sys.argv[1], os.environ['GITHUB_TOKEN'])

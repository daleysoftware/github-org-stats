import os
import sys
import datetime
import github
import collections

DEBUG = False

past_days_30 = datetime.datetime.now() + datetime.timedelta(-30)
past_days_60 = datetime.datetime.now() + datetime.timedelta(-60)


def debug(message):
    if DEBUG:
        print("%s %s" % (datetime.datetime.now(), message))


org_members_cache = set()


def is_in_org(api_org, author):

    if len(org_members_cache) == 0:
        for member in api_org.get_members():
            org_members_cache.add(member.login)

    return author.login in org_members_cache


class Contributor(object):
    def __init__(self):
        self.stats = []
        self.user = None

    def extend(self, stats):
        self.stats.extend(stats)

    def _stats_this_month(self):
        return filter(lambda week: week.w >= past_days_30, self.stats)

    def _stats_last_month(self):
        return filter(lambda week: past_days_30 >= week.w >= past_days_60, self.stats)

    @staticmethod
    def _score(stats):
        result = 0
        for stat in stats:
            commits, additions, deletions = stat.c, stat.a, stat.d
            # Somewhat arbitrarily, value commits at 10 "points" a piece. Code is worth 1 point for 10 lines, capped at
            # 100 points for deletions, 100 for additions each week.
            result += 10 * commits + min(100, additions/10) + min(100, deletions/10)
        return int(result)

    def score_this_month(self):
        debug("Computing this-month score for %s" % self.user)
        stats = self._stats_this_month()
        return Contributor._score(stats)

    def score_last_month(self):
        debug("Computing last-month score for %s" % self.user)
        stats = self._stats_last_month()
        return Contributor._score(stats)


class ScoreSummary(object):
    def __init__(self, contributors, scores):
        self.contributors = contributors
        self.scores = scores

    def __str__(self):
        result = []

        for contributor_id in self.scores.keys():
            score_this_month, score_last_month = self.scores[contributor_id]
            result.append((self.contributors[contributor_id].user.name,
                           self.contributors[contributor_id].user.login,
                           self.contributors[contributor_id].user.avatar_url,
                           score_this_month, score_last_month))

        return '\n'.join([','.join(str(y) for y in x) for x in sorted(result, reverse=True, key=lambda t: t[3])])


def main(github_organization, github_token):
    print("Generating your report.")
    print("This might take a while depending on the number of repos in your organization.")
    print("Please wait...")

    api_client = github.Github(github_token)
    api_org = api_client.get_organization(github_organization)
    repos = api_org.get_repos()

    contributors = collections.defaultdict(Contributor)

    for repo in repos:
        debug("Inspecting repository %s" % repo)

        # Only inspect private repos and repos that have been pushed to in the last 60 days.
        if repo.private and repo.pushed_at > past_days_60:
            stats_contributors = repo.get_stats_contributors()

            if stats_contributors is not None:
                for stats_contributor in stats_contributors:
                    debug("Logging stats for contributor %s" % stats_contributor.author)

                    if not is_in_org(api_org, stats_contributor.author):
                        continue

                    contributors[stats_contributor.author.id].user = stats_contributor.author
                    contributors[stats_contributor.author.id].stats.extend(stats_contributor.weeks)

    scores = {}
    for contributor in sorted(contributors.keys()):
        this_month = contributors[contributor].score_this_month()
        last_month = contributors[contributor].score_last_month()

        if this_month != 0 or last_month != 0:
            scores[contributor] = (this_month, last_month)

    score_summary = str(ScoreSummary(contributors, scores))
    print()
    print("User Name,User ID,User Avatar URL,Score This Month,Score Last Month")
    print(score_summary)


def usage():
    print("Usage: python3 %s <organization_name>" % sys.argv[0])
    sys.exit(1)


if __name__ == '__main__':
    if 'GITHUB_TOKEN' not in os.environ:
        usage()
    if len(sys.argv) != 2:
        usage()
    main(sys.argv[1], os.environ['GITHUB_TOKEN'])

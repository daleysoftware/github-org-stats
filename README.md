# Github Org Stats

Generate interesting leaderboard statistics from your Github Organization.

## Overview

This tool will generate a leaderboard report for your Github organization.
The leaderboard report contains the following fields:

- User name (first & last)
- User ID
- User Avatar URL
- Score This Month (last 30 days)
- Score Last Month (the 30 days prior)

The _Score_ is computed as follows. Each commit is given a value of 10 points.
10 lines of code is worth 1 point, with a cap of 100 points per week in a given
repository.

The philosophy on the score takes its spirit from Agile; we want to encourage
many small commits, during each sprint.

LOC contribution to Score is capped so as to minimize the impact of large
boilerplate changes on your result.

The output of this tool is data in CSV format.

## Disclaimer

While these statistics can be interesting, IMO, they should be interpreted with
a grain of salt. Number of commits and LOC are _not_ (again, IMO) an accurate
overall measure of engineering productivity. These statistics should be used in
conjunction with other management best practices, and not in isolation.

It may not be wise to share such statistics in a public context with a team, as
such sharing might result in gamification of the system and encourage the
wrong behavior amongst the developers.

## Development

To install dependencies (virtualenv and python3 are required first):

    make setup

To execute the fetching script:

    make all ORG=<github_organization> GITHUB_TOKEN=<github_token>

## Utilities

In development you may wish to monitor your rate limiting status with Github.
This tool should not exhaust your rate limit quota unless run excessively.

See also `./scripts/check-rate-limits.sh` which expects `GITHUB_TOKEN` to be
set in your environment.

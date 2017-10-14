# Github Org Stats

Generate useful and actionable statistics for your Github organization.

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

## Development

To install dependencies:

    make setup

To execute the fetching script:

    make all ORG=<github_organization> GITHUB_TOKEN=<github_token>

## Utilities

In development you may wish to monitor your rate limiting status with Github.
This tool should not exhaust your rate limit quota unless run excessively.

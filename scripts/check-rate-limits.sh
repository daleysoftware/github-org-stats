#!/bin/bash

remaining=$(curl --silent -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit \
    | jq  '.resources.core.remaining')

limit=$(curl --silent -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit \
    | jq  '.resources.core.limit')

reset=$(curl --silent -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit \
    | jq  '.resources.core.reset')

echo $remaining/$limit
if [ "$(uname -s)" = "Darwin" ]
then
    echo Reset @ $(date -r ${reset} +"%r")
else
    echo Reset @ $(date -d @${reset} +"%r")
fi

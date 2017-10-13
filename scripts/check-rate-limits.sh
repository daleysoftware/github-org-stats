remaining=$(curl --silent -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit \
    | jq  '.resources.core.remaining')

limit=$(curl --silent -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit \
    | jq  '.resources.core.limit')

reset=$(curl --silent -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit \
    | jq  '.resources.core.reset')

echo $remaining/$limit
echo Reset @ $(date -d @${reset} +"%r")

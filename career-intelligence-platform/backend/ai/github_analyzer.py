import requests


def analyze_github(username):

    url = f'https://api.github.com/users/{username}/repos'

    response = requests.get(url)

    repos = response.json()

    total_stars = 0

    languages = []

    for repo in repos:
        total_stars += repo['stargazers_count']

        if repo['language']:
            languages.append(repo['language'])

    return {
        'total_repositories': len(repos),
        'total_stars': total_stars,
        'languages': list(set(languages))
    }
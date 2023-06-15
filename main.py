import requests
from plotly import offline

def language_to_url(language):
    lang = language.lower()
    url = f"https://api.github.com/search/repositories?q=language:{lang}&sort=stars"
    return url

def check_status(request):
    status = int(request.status_code)
    return status



if __name__ == '__main__':

    language = input("Enter programming language: ")
    url = language_to_url(language)
    headers = {'Accept': 'application/vnd.github.full+json'}
    r = requests.get(url, headers=headers)
    print(f"Status code: {r.status_code}")
    if check_status(r) != 200:
        print("Invalid status")
        exit()

    response_dict = r.json()
    repo_dicts = response_dict['items']

    repo_links, stars, labels = [], [], []
    for repo_dict in repo_dicts:
        repo_name = repo_dict['name']
        repo_url = repo_dict['html_url']
        repo_links.append(f"<a href='{repo_url}'>{repo_name}</a>")
        stars.append(repo_dict['stargazers_count'])

        owner = repo_dict['owner']['login']
        description = repo_dict['description']
        label = f"{owner}<br />{description}"
        labels.append(label)

    data = [{
        'type': 'bar',
        'x': repo_links,
        'y': stars,
        'hovertext': labels,
        'marker':{
            'color':'rgb(50,75,140)',
            'line': {'width': 1.5, 'color': 'rgb(20,20,20)'}
        },
        'opacity': 0.5,
    }]
    my_layout = {
        'title': f"Most-Starred {language} Projects on GitHub",
        'titlefont': {'size': 30},
        'xaxis': {
            'title': 'Repository',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14}
        },
        'yaxis': {
            'title': 'Stars',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        },

    }
    fig = {'data': data, 'layout': my_layout}
    offline.plot(fig, filename='repository.html')



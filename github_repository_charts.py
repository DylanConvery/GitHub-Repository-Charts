import math
import requests
import plotly.express as px
import argparse
import os

GITHUB_API = 'https://api.github.com/search/repositories'


def fetch_repositories(language, minimum_stars, total, order, page_size, token=None):
    if total <= 0:
        return []
    page_size = max(1, min(100, page_size, total))
    pages = max(1, math.ceil(total/page_size))
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'python-repository_charts/1.0'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'

    collected = []
    with requests.Session() as session:
        for page in range(1, pages+1):
            params = {
                'q': f'language:{language} stars:>={minimum_stars}',
                'sort': 'stars',
                'order': 'order',
                'per_page': page_size,
                'page': page
            }
            try:
                request = session.get(
                    GITHUB_API,
                    params=params,
                    headers=headers,
                    timeout=15
                )
                if request.status_code == 403 and request.headers.get('X-RateLimit-Remaining') == '0':
                    raise SystemExit(
                        'GitHub rate limit reached. Set GITHUB_TOKEN and try again.')
                request.raise_for_status()
                items = request.json().get('items', [])
                if not items:
                    print('Request incorrectly formatted.')
                    break
                for item in items:
                    owner = (item.get('owner') or {}).get('login') or 'unknown'
                    collected.append({
                        'name': item.get('name') or 'unknown',
                        'html_url': item.get('html_url') or '',
                        'stars': int(item.get('stargazers_count') or 0),
                        'owner': owner,
                        'description': item.get('description') or 'No description'
                    })
                if len(collected) >= total:
                    break
            except requests.RequestException as e:
                raise SystemExit(f'Request failed: {e}')
    return collected[:total]


def make_chart(repositories, title):
    repository_links = [
        f"<a href='{repository['html_url']}'>{repository['name']}</a>"
        for repository in repositories
    ]
    stars = [
        repository['stars']
        for repository in repositories
    ]
    hover_texts = [
        f"<b>{repository['name']}</b>"
        f"<br />{repository['owner']}<br />"
        f"{repository['description']}"
        for repository in repositories
    ]

    fig = px.bar(
        x=repository_links,
        y=stars,
        title=title,
        labels={
            'x': 'Repositories',
            'y': 'Stars'
        }
    )

    fig.update_layout(
        title_font_size=28,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20
    )

    fig.update_traces(
        hovertext=hover_texts,
        hovertemplate="%{hovertext}<br />%{y} Stars<extra></extra>",
        marker_color='SteelBlue',
        marker_opacity=0.6
    )
    fig.show()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Visualize most-starred GitHub repos for a language."
    )
    parser.add_argument(
        '--language',
        default='python',
        help='Language to search for.'
    )
    parser.add_argument(
        '--order',
        default='desc',
        # add description
        help='Sort order.'
    )
    parser.add_argument(
        '--minimum-stars',
        type=int,
        default=10000,
        help='Minimum amount of stars to sort by.'
    )
    parser.add_argument(
        '--total-repos',
        type=int,
        default=10,
        help='Amount of repositories to fetch.'
    )
    parser.add_argument(
        '--page-size',
        type=int,
        default=100,
        choices=range(1, 101),
        metavar='[1-100]',
        help='Results per API page.'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    token = os.getenv('GITHUB_TOKEN')
    repositories = fetch_repositories(
        language=args.language,
        minimum_stars=args.minimum_stars,
        total=args.total_repos,
        order=args.order,
        page_size=args.page_size,
        token=token
    )
    print(f'Fetched {len(repositories)} repositories.')
    make_chart(
        repositories,
        title=f'Most-Starred {args.language.capitalize()} Projects on GitHub'
    )


if __name__ == "__main__":
    main()

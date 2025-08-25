import pytest
from github_repository_charts import fetch_repositories, parse_arguments

TOTAL = 30
STARS = 30


@pytest.fixture
def repositories():
    repositories = fetch_repositories(
        language='python',
        minimum_stars=STARS,
        total=TOTAL,
        order='desc',
        page_size=30,
    )
    return repositories


def test_fetch_repositories_size(repositories):
    assert len(repositories) == TOTAL


def test_fetch_repositories_stars(repositories):
    for repo in repositories:
        assert repo['stars'] > STARS


def test_no_repositories_returned():
    repo = fetch_repositories('python', 1000000000, TOTAL, 'desc', 30)
    assert len(repo) == 0


def test_fetch_repositories_fields(repositories):
    for repo in repositories:
        assert "stars" in repo
        assert "name" in repo
        assert "html_url" in repo
        assert "owner" in repo
        assert "description" in repo

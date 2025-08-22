# GitHub Repository Charts

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=ffdd54)

This project fetches and visualizes the most-starred GitHub repositories for a specified programming language using GitHub’s Search API and Plotly to display an bar chart sorted by your preferences. To get started, you first need to install the requirements:

```bash
pip install -r requirements.txt
```

After installation, run the script with desired options, for example:

```bash
# With flags
python github_repository_visualizer.py --language python --order desc --minimum-stars 10000 --total-repos 20 --page-size 50
# Without flags
python github_repository_visualizer.py 
```

Note that GitHub API has rate limits; you can optionally provide a GitHub token to increase these limits.

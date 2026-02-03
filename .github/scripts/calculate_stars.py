import os
import json
from github import Github

# Initialize GitHub API
g = Github(os.getenv('GH_TOKEN'))
user = g.get_user()

# 1. Count stars from your owned repositories
total_stars = sum(repo.stargazers_count for repo in user.get_repos(type='owner'))

# 2. Count stars from the external list
try:
    with open('external_repos.json', 'r') as f:
        external_repos = json.load(f)
    
    for repo_name in external_repos:
        repo = g.get_repo(repo_name)
        total_stars += repo.stargazers_count
except Exception as e:
    print(f"Error reading external repos: {e}")

# 3. Format the number (e.g., 1500 -> 1.5k)
display_count = f"{total_stars/1000:.1f}k" if total_stars >= 1000 else str(total_stars)

# 4. Create the JSON for Shields.io
data = {
    "schemaVersion": 1,
    "label": "Impact Stars",
    "message": display_count,
    "color": "orange",
    "style": "for-the-badge"
}

with open('stars_data.json', 'w') as f:
    json.dump(data, f)

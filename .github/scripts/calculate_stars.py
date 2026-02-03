import os
import json
from github import Github, Auth

# 1. Initialize GitHub API with the new Auth syntax
auth = Auth.Token(os.getenv('GH_TOKEN'))
g = Github(auth=auth)

# 2. Fetch YOUR user specifically (this uses public data)
# Replace YOUR_GITHUB_USERNAME with PallottaEnrico
username = "PallottaEnrico"
user = g.get_user(username)

# 3. Count stars from your owned repositories
# We fetch by username to avoid the 'authenticated user' permission error
total_stars = sum(repo.stargazers_count for repo in user.get_repos())

# 4. Count stars from the external list
try:
    if os.path.exists('external_repos.json'):
        with open('external_repos.json', 'r') as f:
            external_repos = json.load(f)
        
        for repo_name in external_repos:
            repo = g.get_repo(repo_name)
            total_stars += repo.stargazers_count
except Exception as e:
    print(f"Error reading external repos: {e}")

# 5. Format and save
display_count = f"{total_stars/1000:.1f}k" if total_stars >= 1000 else str(total_stars)

data = {
    "schemaVersion": 1,
    "label": "⭐ Stars",
    "message": display_count,
    "color": "FFD700",
    "style": "for-the-badge"
}

with open('stars_data.json', 'w') as f:
    json.dump(data, f)

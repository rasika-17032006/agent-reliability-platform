import os
import requests
from config import GITEA_URL, GITEA_TOKEN

class GiteaClient:
    def __init__(self):
        self.headers = {"Authorization": f"token {GITEA_TOKEN}"}
        self.base_url = GITEA_URL

    def create_local_repo(self, repo_name):
        """Creates a repository on the local Gitea instance."""
        url = f"{self.base_url}/api/v1/user/repos"
        data = {"name": repo_name, "private": False, "auto_init": True}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def get_repo_files(self, repo_name):
        """Fetches file structure from the Gitea instance repository."""
        url = f"{self.base_url}/api/v1/repos/agent-bot/{repo_name}/contents"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [f["name"] for f in response.json()]
        return []
import requests
from app.core.config import settings
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
import os

class GitHubService:
    def __init__(self):
        # self.g = Github(auth=Auth.Token(settings.GITHUB_TOKEN))
        self.headers={
            # "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Authorization": "Bearer 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",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.base_url = "https://api.github.com/"

        self.user = self._request("user")['login']

    def _request(self, url: str, params: dict = None):
        response = requests.get(self.base_url + url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error: {response.json()}")
        return response.json()
    
    def get_repo(self, repo_name: str):
        return self._request(f"repos/{self.user}/{repo_name}")

    def get_commits(self, repo_name: str):
        return self._request(f"repos/{self.user}/{repo_name}/commits")

    def get_prs(self, repo_name: str):
        return self._request(f"repos/{self.user}/{repo_name}/pulls")
    
    def get_issues(self, repo_name: str):
        params = {
            "filter": "assigned",
            "state": "all"
        }
        return self._request(f"repos/{self.user}/{repo_name}/issues", params=params)
    
    def get_tools(self, repo_name: str):
        private_key = os.open(settings.GITHUB_APP_PRIVATE_KEY_LOC, os.O_RDONLY)
        # make private key a string
        private_key_str = os.read(private_key, 1000000)
        private_key_str = private_key_str.decode("utf-8")
        os.close(private_key)
        github = GitHubAPIWrapper(github_app_id=settings.GITHUB_APP_ID, github_app_private_key=private_key_str)
        toolkit = GitHubToolkit(github, repo_name)
        
        tools = toolkit.get_tools()
        for i in range(len(tools)):
            tools[i].name = tools[i].mode

        return tools
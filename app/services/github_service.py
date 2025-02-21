import requests
from app.core.config import settings

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


    def _request(self, url: str):
        response = requests.get(self.base_url + url, headers=self.headers)
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
        return self._request(f"repos/{self.user}/{repo_name}/issues")
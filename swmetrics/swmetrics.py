from git import Repo
from src.general.general import General


class SwMetrics:
    def __init__(self, repo_path: str):
        self._repo = Repo(repo_path)
        self._general = General(self._repo)
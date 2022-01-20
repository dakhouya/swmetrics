from git import Repo
from os import path


class General:
    def __init__(self, repo: Repo):
        self.authors = []
        self.commits = []
        self.files = []
        self.__analyse(repo)

    def line_count(self) -> int:
        line_count = 0

        for file in self.files:
            try:
                with open(file, 'r') as f:
                    line_count += sum(1 for _ in f)
            except UnicodeDecodeError:
                # File is binary we can't count line
                pass

        return line_count

    def __analyse(self, repo: Repo):
        # Get commits
        self.commits = list(repo.iter_commits())

        # Get authors
        for commit in list(repo.iter_commits()):
            if commit.author not in self.authors:
                self.authors.append(commit.author)

        # Get files
        trees = [repo.head.commit.tree]
        while len(trees) > 0:
            tree = trees.pop()
            for file in tree.blobs:
                self.files.append(path.join(repo.working_tree_dir, file.path))
            for subtree in tree.trees:
                trees.append(subtree)

from git import Repo
from general.general import General
import click

class SwMetrics:
    def __init__(self, repo_path: str):
        self._repo = Repo(repo_path)
        self.general = General(self._repo)


@click.command()
@click.argument('repo')
def main(repo):
    sw_metric = SwMetrics(repo)
    print(sw_metric.general.__str__())


if __name__ == '__main__':
    main()

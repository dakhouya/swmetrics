import pytest
from swmetrics.general.general import General
from git import Repo
import os
import shutil

TEST_BASE_PATH = './tmp/'
TEST_REPO_PATH = TEST_BASE_PATH + '/test-repo/'
TEST_FILE_PATH = TEST_REPO_PATH + 'readme.txt'


def recursive_chmod(path, permissions):
    for dir_path, _, filenames in os.walk(path):
        os.chmod(dir_path, permissions)
        for filename in filenames:
            os.chmod(os.path.join(dir_path, filename), permissions)


@pytest.fixture
def setup():
    # Create a repo with commit to use as test repository
    repo = Repo.init(TEST_REPO_PATH)
    with open(TEST_FILE_PATH, 'w') as f:
        f.write('First line')
        f.close()
    repo.config_writer().set_value("user", "name", "test name").release()
    repo.config_writer().set_value("user", "email", "test.name@email.com").release()
    repo.git.add(all=True)
    repo.git.commit('-m', 'first commit')
    # Close all descriptors
    repo.close()
    yield
    # Change file permissions in order to delete
    recursive_chmod(TEST_BASE_PATH, 0o777)
    shutil.rmtree(TEST_BASE_PATH)


def test_init(setup):
    repo = Repo(TEST_REPO_PATH)
    general = General(repo)
    repo.close()
    assert len(general.authors) == 1

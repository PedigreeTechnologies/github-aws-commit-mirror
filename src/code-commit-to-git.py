"""
Python script to automate restoring
github repositories from codecommit
"""
import os
import boto3
from github import Github

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
GITHUB_API_TOKEN = os.getenv("GH_API_TOKEN")
AWS_SSH_KEY_ID = os.getenv("AWS_SSH_KEY_ID")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
RUN_ID = os.getenv("GITHUB_RUN_ID")

github_client = Github(GITHUB_API_TOKEN)

codecommit_client = boto3.client(
    "codecommit",
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

response = codecommit_client.describe_repositories(nextToken="string", maxResults=123)

repos = response["repositories"]


class BColors:
    """Define print colors"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def clone_code_commit(repo_name):
    """Clone Repo from codecommit"""
    print(
        f"{BColors.OKGREEN}--> Cloning repository {repo_name} from CodeCommit {BColors.ENDC}",
        flush=True,
    )
    os.system(
        "git clone --mirror ssh://{1}@git-codecommit.us-east-1.amazonaws.com/v1/repos/{0} {0}".format(
            repo_name,
            AWS_SSH_KEY_ID,
        )
    )


def sync_git_repo(repo_name):
    """Sync repository"""
    print(
        f"{BColors.OKGREEN}--> Pushing changes from repository \
            {repo_name} to Github {BColors.ENDC}",
        flush=True,
    )
    os.system(
        "cd {0} && git remote add sync \
        https://github.com/PedigreeTechnologies/{0}.git".format(
            repo_name
        )
    )
    os.system("cd {} && git push sync --mirror".format(repo_name))


def is_repo_exists_on_github(repo_name):
    """Check if repo exists on aws"""
    try:
        github_client.get_user().get_repo("{0}".format(repo_name))
        return True
    except Exception:
        return False


def create_git_repo(repo_name):
    """Create Github Repo"""
    print(
        f"{BColors.OKGREEN}--> Creating Repository {repo_name} on Github {BColors.ENDC}",
        flush=True,
    )
    os.system(
        "git remote add origin git@github.com:PedigreeTechnologies/{0}.git".format(
            repo_name
        )
    )


def delete_repo_local(repo_name):
    """Clone local repository"""
    print(
        f"{BColors.OKGREEN}--> Deleting repository {repo_name} from local storage {BColors.ENDC}",
        flush=True,
    )
    os.system("rm -Rf {}".format(repo_name))


for repo in repos:
    repo_name = repo["repositoryName"]
    print(
        f"{BColors.HEADER}> Processing repository: {repo_name} {BColors.ENDC}",
        flush=True,
    )
    clone_code_commit(repo_name)
    if is_repo_exists_on_github(repo_name):
        sync_git_repo(repo_name)
    else:
        create_git_repo(repo_name)
        sync_git_repo(repo_name)
    delete_repo_local(repo_name)

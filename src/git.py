from git import Repo


def git_clone_into_directory(git_url: str, clone_directory_path: str):
	Repo.clone_from(git_url, clone_directory_path)

from git import Repo
from git.exc import BadName
from pathlib import Path
import tempfile


class GitLocalRepositoryInstance():

	def __init__(self, *, directory_path: str):

		self.__directory_path = directory_path

	def get_directory_path(self) -> str:
		return self.__directory_path


class GitManager():

	def __init__(self, *, git_directory_path: str):

		self.__git_directory_path = git_directory_path

	@staticmethod
	def __get_project_directory_name_from_git_url(*, git_url: str) -> str:
		project_directory_name = git_url.split("/")[-1].split(".git")[0]
		if project_directory_name == "":
			raise Exception(f"Failed to find project name in git url: \"{git_url}\".")
		return project_directory_name

	@staticmethod
	def __get_sha_from_repo(*, repo: Repo) -> str:
		try:
			sha = repo.rev_parse("origin/master")
		except BadName as ex:
			sha = repo.rev_parse("origin/main")
		return sha

	def is_remote_commit_different(self, *, git_url: str):

		is_different = True
		git_project_name = GitManager.__get_project_directory_name_from_git_url(
			git_url=git_url
		)
		git_project_directory_path = Path(self.__git_directory_path, git_project_name)
		if git_project_directory_path.exists():
			temp_directory = tempfile.TemporaryDirectory()
			remote_repo = Repo.clone_from(git_url, temp_directory.name, depth=1)
			remote_sha = GitManager.__get_sha_from_repo(
				repo=remote_repo
			)
			temp_directory.cleanup()

			local_repo = Repo(git_project_directory_path)
			local_sha = GitManager.__get_sha_from_repo(
				repo=local_repo
			)

			if remote_sha == local_sha:
				is_different = False

		return is_different

	def clone(self, *, git_url: str):

		# get project name via git_url
		# if not self.__git_directory_path + project name can be parsed as a git directory
		#	delete everything in self.__git_directory_path + project name
		# else
		# 	determine the current version in self.__git_directory_path + project name
		# 	if the version is different from the git_url
		#		clone from git_url

		git_project_name = GitManager.__get_project_directory_name_from_git_url(
			git_url=git_url
		)
		git_project_directory_path = Path(self.__git_directory_path, git_project_name)
		if git_project_directory_path.exists():
			git_project_directory_path.unlink()
		Repo.clone_from(git_url, git_project_directory_path)

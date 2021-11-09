from git import Repo


class GitManager():

	def __init__(self, *, git_directory_path: str):

		self.__git_directory_path = git_directory_path

	def clone(self, *, git_url: str):

		Repo.clone_from(git_url, self.__git_directory_path)

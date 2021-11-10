import unittest
from src.austin_heller_repo.git_manager import GitManager, GitLocalRepositoryInstance
import tempfile
from pathlib import Path


class GitManagerTest(unittest.TestCase):

	def setUp(self):
		pass

	def test_initialize(self):

		temp_directory = tempfile.TemporaryDirectory()

		git_manager = GitManager(
			git_directory_path=temp_directory.name
		)

		temp_directory.cleanup()

	def test_clone(self):

		temp_directory = tempfile.TemporaryDirectory()

		git_manager = GitManager(
			git_directory_path=temp_directory.name
		)

		git_manager.clone(
			git_url="https://github.com/AustinHellerRepo/TestDeviceModule.git"
		)

		expected_file_objects = [
			"TestDeviceModule",
			"TestDeviceModule/.git"
		]

		for expected_file_object in expected_file_objects:
			expected_file_object_path = Path(temp_directory.name, expected_file_object)
			self.assertTrue(expected_file_object_path.exists())

		temp_directory.cleanup()

	def test_clone_then_is_different_from_remote_not_different(self):

		temp_directory = tempfile.TemporaryDirectory()

		git_manager = GitManager(
			git_directory_path=temp_directory.name
		)

		git_url = "https://github.com/AustinHellerRepo/TestDeviceModule.git"

		git_manager.clone(
			git_url=git_url
		)

		is_different = git_manager.is_remote_commit_different(
			git_url=git_url
		)

		temp_directory.cleanup()

		self.assertFalse(is_different)

	def test_clone_then_is_different_from_remote_different(self):

		temp_directory = tempfile.TemporaryDirectory()

		git_manager = GitManager(
			git_directory_path=temp_directory.name
		)

		git_url_first = "https://github.com/AustinHellerRepo/TestDeviceModule.git"
		git_url_second = "https://github.com/AustinHellerRepo/GitManager.git"

		self.assertNotEqual(git_url_first, git_url_second)

		git_manager.clone(
			git_url=git_url_first
		)

		is_different = git_manager.is_remote_commit_different(
			git_url=git_url_second
		)

		temp_directory.cleanup()

		self.assertTrue(is_different)

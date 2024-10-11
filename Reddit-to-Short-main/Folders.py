import os
import shutil


class FolderManager:
    """A class to manage the creation of necessary folders for video processing."""

    def __init__(self, base_folder='output', reddit_folder='reddit_download', render_folder='render_download', final_folder='final_output'):
        """
        Initializes the FolderManager with paths for base, reddit, render, and final folders.

        Args:
            base_folder (str): The base folder path where all other folders will be created.
            reddit_folder (str): The name of the folder for Reddit downloads.
            render_folder (str): The name of the folder for rendered videos.
            final_folder (str): The name of the folder for final outputs.
        """
        self.base_folder = base_folder
        self.reddit_folder_path = os.path.join(self.base_folder, reddit_folder)
        self.render_folder_path = os.path.join(self.base_folder, render_folder)
        self.final_folder_path = os.path.join(self.base_folder, final_folder)

    def create_folders(self):
        """
        Creates the base, reddit, render, and final folders by calling the _create_folder method.
        """
        self._create_folder(self.base_folder)
        self._create_folder(self.reddit_folder_path)
        self._create_folder(self.render_folder_path)
        self._create_folder(self.final_folder_path)

    @staticmethod
    def _create_folder(path):
        """
        Creates a folder at the specified path. If the folder exists, it is deleted and recreated.

        Args:
            path (str): The path where the folder should be created.
        """
        if os.path.exists(path):
            shutil.rmtree(path)  # Delete the folder and its contents if it exists
        os.makedirs(path)  # Create the folder


if __name__ == "__main__":
    # Example usage: Initialize the FolderManager and create the folders
    folder_manager = FolderManager()
    folder_manager.create_folders()

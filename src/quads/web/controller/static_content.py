import os
import shutil


class StaticContent:
    FOLDER_NAME = 'quads_web'

    def __init__(self):
        self.repo_path = None

    def clone_repo(self, repo_link: str):
        """
        This method clone repository from GitHub/ GitLab repository.
        # Must be public
        """
        repo_name = repo_link.split('/')[-1].split('.')[0]
        self.repo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), repo_name)
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path)
        cmd = f'git clone {repo_link}'
        os.system(cmd)

    def move_static_content(self):
        """
        This method find static content in download repo and move them to current dir.
        """
        quads_web_path = os.path.join(self.repo_path, self.FOLDER_NAME)
        for quads_web_dirs in os.listdir(quads_web_path):
            if os.path.isdir(os.path.join(quads_web_path, quads_web_dirs)):
                private_static_path = os.path.join(quads_web_path, quads_web_dirs)
                local_static_path = os.path.join(os.path.dirname(self.repo_path), quads_web_dirs)
                for dir_name in os.listdir(private_static_path):
                    if not os.path.exists(os.path.join(local_static_path, dir_name)):
                        os.mkdir(os.path.join(local_static_path, dir_name))
                    if os.path.isdir(os.path.join(private_static_path, dir_name)):
                        for file_name in os.listdir(os.path.join(private_static_path, dir_name)):
                            if os.path.isfile(os.path.join(private_static_path, dir_name, file_name)):
                                src_path = os.path.join(private_static_path, dir_name, file_name)
                                dst_path = os.path.join(local_static_path, dir_name, file_name)
                                shutil.move(src_path, dst_path)

    def download_static_content(self, repo_link: str):
        """
        This method download static content and stores in local path
        """
        self.clone_repo(repo_link=repo_link)
        self.move_static_content()


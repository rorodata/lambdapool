import shutil
import subprocess

def copy(src, dest):
    if src.is_file():
        shutil.copy(src, dest)
    else:
        shutil.copytree(src, dest)

def run_command(command):
    subprocess.run(command.split(), check=True)

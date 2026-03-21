# shared/utils.py
import os

def find_project_root(start_path):
    """
    Finds the project root by searching upwards for a '.git' directory.
    """
    path = os.path.abspath(start_path)
    while True:
        if os.path.isdir(os.path.join(path, '.git')):
            return path
        parent_path = os.path.dirname(path)
        if parent_path == path:
            raise FileNotFoundError("Project root with .git directory not found.")
        path = parent_path

def get_dist_dir(skill_name):
    """
    Finds a suitable distribution directory for a skill's runtime files.
    All generated artifacts are placed in a .dist directory at the root of the skills repository.
    """
    try:
        # Assuming the script is called from within the project structure
        project_root = find_project_root(os.path.dirname(__file__))
        dist_dir = os.path.join(project_root, ".dist", skill_name)
        os.makedirs(dist_dir, exist_ok=True)
        return dist_dir
    except FileNotFoundError:
        # Fallback for when script is run in a context where .git isn't found
        # This is a less ideal, non-portable fallback
        fallback_dir = os.path.join(os.path.dirname(__file__), '..', '.dist', skill_name)
        os.makedirs(fallback_dir, exist_ok=True)
        return os.path.abspath(fallback_dir)

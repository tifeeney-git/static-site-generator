import os
import shutil
import sys

from gencontent import generate_pages_recursively

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def copy_contents(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_contents(from_path, dest_path)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_contents(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursively(
        os.path.join(dir_path_content),
        template_path,
        os.path.join(dir_path_public),
        basepath
    )


main()
import os
import shutil
from src.md_parser import markdown_to_html_node, extract_title


def init_directory(source, destination):

    # Check paths exist
    if not (os.path.exists(source)):
        raise FileNotFoundError("Invalid source path")

    # Check if src is a directory
    if os.path.isfile(source):
        raise NotADirectoryError("Source path wasn't a directory")

    # Clear/ Initialize destination directory

    # Create directory if it doesn't exist
    if not os.path.exists(destination):
        os.mkdir(destination)
        print("Creating destination directory")

    # Iterate through flat directories and remove them
    for item in os.listdir(destination):
        full_path = os.path.join(destination, item)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)

    print("Destination directory initialized")

    copy_directory(source, destination)


# For each file and subdirectory copy the contents to the new directory and print to console
def copy_directory(source, destination):
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copying {src_path} to destination")
        else:
            os.mkdir(dst_path)
            print(f"Copying directory {src_path}")
            copy_directory(src_path, dst_path)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(
        f"Generating page from {from_path} to {dest_path} using template at {template_path}"
    )
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as t:
        template = t.read()

    title = extract_title(md)

    html = markdown_to_html_node(md).to_html()

    new_page = template.replace("{{ Title }}", title.capitalize()).replace(
        "{{ Content }}", html
    )

    os.makedirs(
        os.path.dirname(
            dest_path,
        ),
        exist_ok=True,
    )

    with open(dest_path, "w") as d:
        d.write(new_page)

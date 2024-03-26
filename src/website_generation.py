import os
import os.path
import shutil
from datetime import datetime
from block_md_parsing import markdown_to_blocks, markdown_to_html_node


def logger(message: str):
    now = datetime.now().strftime("%s")
    print(f"[{now}]: {message}")


def copy_all_to_target(source_dir: str, target_dir: str):
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    logger(f"current dir: {source_dir}")
    for file_name in os.listdir(source_dir):
        file = os.path.join(source_dir, file_name)
        if os.path.isfile(file):
            logger(f"{file_name} -> {os.path.join(target_dir, file_name)}")
            shutil.copy(file, target_dir)
        else:
            recursive_target = os.path.join(target_dir, file_name)
            copy_all_to_target(file, recursive_target)
    logger(f"finished copying all {source_dir} files recursively")
    return None


def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise Exception("No valid title (h1 heading) found on document")


def generate_page(from_path, template_path, dest_path):
    logger(f"Generating from {from_path} to {dest_path} using {template_path}")
    md, html_template = "", ""
    with open(from_path, "r") as f, open(template_path, "r") as t:
        md = f.read()
        html_template = t.read()

    md_blocks = markdown_to_html_node(md)
    md_title = extract_title(md)
    filled_template = html_template.replace("{{ Title }}", md_title).replace(
        "{{ Content }}", md_blocks.to_html()
    )
    dest_path_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_path_dir):
        os.makedirs(dest_path_dir)
    with open(os.path.join(dest_path), "w+") as f:
        f.write(filled_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file)
        if os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_file_path)
        if file_path.endswith(".md"):
            generate_page(
                file_path, template_path, dest_file_path.replace(".md", ".html")
            )

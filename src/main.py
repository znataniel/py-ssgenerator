import os
import shutil
from website_generation import (
    logger,
    copy_all_to_target,
    generate_pages_recursive,
)


def main():
    static_path = "./static"
    public_path = "./public"

    logger(f"Cleaning public directory at {public_path}")
    if len(os.listdir(public_path)):
        shutil.rmtree(public_path)

    copy_all_to_target(static_path, public_path)
    generate_pages_recursive("./content", "./template.html", "./public")


main()

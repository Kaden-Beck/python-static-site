import sys
from src.build import init_build_directory, generate_pages_recursive


def main():
    init_build_directory("./static", "./docs")

    generate_pages_recursive(
        "./content", "src/template.html", "./docs", sys.argv[1] or "/"
    )


if __name__ == "__main__":
    main()

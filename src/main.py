from src.build import init_build_directory, generate_pages_recursive


def main():
    init_build_directory("./static", "./public")
    generate_pages_recursive("./content", "src/template.html", "./public")


if __name__ == "__main__":
    main()

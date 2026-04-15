from src.build import init_directory, generate_page


def main():
    init_directory("./static", "./public")
    generate_page("src/content/index.md", "src/template.html", "./public/index.html")


if __name__ == "__main__":
    main()

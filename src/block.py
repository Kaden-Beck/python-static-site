def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(lambda a: a, map(lambda a: a.strip(), markdown.split("\n\n"))))

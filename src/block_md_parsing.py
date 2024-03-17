def markdown_to_blocks(markdown: str):
    splits = markdown.split("\n\n")
    splits_stripped = list(map(lambda block: block.strip("\n "), splits))
    return list(filter(lambda block: block != "" and block != "\n", splits_stripped))

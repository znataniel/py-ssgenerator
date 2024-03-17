import re


def markdown_to_blocks(markdown: str):
    splits = markdown.split("\n\n")
    splits_stripped = list(map(lambda block: block.strip("\n "), splits))
    return list(filter(lambda block: block != "" and block != "\n", splits_stripped))


block_type_para = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


def block_to_block_type(block: str):
    heading_pattern = r"\#{1,6} \w+"
    if re.match(heading_pattern, block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    lines_split = block.split("\n")
    if block.startswith(">"):
        if all([line.startswith(">") for line in lines_split]):
            return block_type_quote
        return block_type_para
    if block.startswith("* "):
        if all([line.startswith("* ") for line in lines_split]):
            return block_type_ul
        return block_type_para
    if block.startswith("- "):
        if all([line.startswith("- ") for line in lines_split]):
            return block_type_ul
        return block_type_para
    if block.startswith("1. "):
        if all(
            [
                lines_split[i - 1].startswith(f"{i}. ")
                for i in range(2, len(lines_split) + 1)
            ]
        ):
            return block_type_ol
    return block_type_para

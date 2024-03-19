import re
from htmlnode import ParentNode, LeafNode
from inline_md_parsing import text_to_textnodes
from textnode import text_node_to_html_node

block_type_para = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


def markdown_to_blocks(markdown: str):
    splits = markdown.split("\n\n")
    splits_stripped = list(map(lambda block: block.strip("\n "), splits))
    return list(filter(lambda block: block != "" and block != "\n", splits_stripped))


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


def markdown_to_html_node(markdown):
    html_nodes = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_para:
            html_nodes.append(para_block_md2html(block))
        if block_type == block_type_heading:
            html_nodes.append(heading_block_md2html(block))
        if block_type == block_type_code:
            html_nodes.append(code_block_md2html(block))
        if block_type == block_type_quote:
            html_nodes.append(quote_block_md2html(block))
        if block_type == block_type_ul:
            html_nodes.append(ul_block_md2html(block))
        if block_type == block_type_ol:
            html_nodes.append(ol_block_md2html(block))
    return ParentNode("div", html_nodes)


def para_block_md2html(block: str):
    text_nodes = text_to_textnodes(block)
    leaf_nodes = [text_node_to_html_node(textnode) for textnode in text_nodes]
    return ParentNode("p", leaf_nodes)


def heading_block_md2html(block: str):
    split = block.split(maxsplit=1)
    heading_level = len(split[0])
    if heading_level in range(0, 7):
        text_nodes = text_to_textnodes(split[1])
        leaf_nodes = [text_node_to_html_node(textnode) for textnode in text_nodes]
        return ParentNode(f"h{heading_level}", leaf_nodes)


def code_block_md2html(block: str):
    return LeafNode("code", block.strip("`"))


def quote_block_md2html(block: str):
    lines_split = block.split("\n")
    clean_lines = [line.lstrip("> ") for line in lines_split]
    clean_text = "\n".join(clean_lines)
    text_nodes = text_to_textnodes(clean_text)
    leaf_nodes = [text_node_to_html_node(textnode) for textnode in text_nodes]
    return ParentNode("blockquote", leaf_nodes)


def ul_block_md2html(block: str):
    lines_split = block.split("\n")
    clean_lines = [line.lstrip("*- ") for line in lines_split]
    ul_li_elements = []
    for line in clean_lines:
        line_to_txtnodes = text_to_textnodes(line)
        line_leaf_nodes = [
            text_node_to_html_node(__line) for __line in line_to_txtnodes
        ]
        ul_li_elements.append(ParentNode("li", line_leaf_nodes))
    return ParentNode("ul", ul_li_elements)


def ol_block_md2html(block: str):
    lines_split = block.split("\n")
    clean_lines = [line.lstrip("1234567890. ") for line in lines_split]
    ol_li_elements = []
    for line in clean_lines:
        line_to_txtnodes = text_to_textnodes(line)
        line_leaf_nodes = [
            text_node_to_html_node(__line) for __line in line_to_txtnodes
        ]
        ol_li_elements.append(ParentNode("li", line_leaf_nodes))
    return ParentNode("ol", ol_li_elements)

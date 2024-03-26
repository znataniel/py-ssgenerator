from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code,
)
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    nodes_split = []
    for on in old_nodes:
        if on.text_type != text_type_text:
            nodes_split.append(on)
            continue
        splits = on.text.split(delimiter)
        if not len(splits) % 2:
            raise Exception(
                f"""
                Invalid markdown syntax: closing {delimiter} not found in
                vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
                {on.text}
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                """
            )
        for i in range(len(splits)):
            if not splits[i]:
                continue
            nodes_split.append(
                TextNode(splits[i], text_type if i % 2 else text_type_text)
            )
    return nodes_split


def extract_markdown_images(line: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", line)


def extract_markdown_links(line: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", line)


def split_nodes_image(old_nodes: list[TextNode]):
    nodes_split = []

    for on in old_nodes:
        matches = extract_markdown_images(on.text)
        if not len(matches) and on.text:
            nodes_split.append(on)
            continue
        for i in range(len(matches)):
            aux_split = on.text.split(f"![{matches[i][0]}]({matches[i][1]})", 1)
            if aux_split[0]:
                nodes_split.append(TextNode(aux_split[0], text_type_text))
            nodes_split.append(TextNode(matches[i][0], text_type_image, matches[i][1]))
            on.text = aux_split[1]
        if on.text:
            nodes_split.append(on)
    return nodes_split


def split_nodes_link(old_nodes: list[TextNode]):
    nodes_split = []

    for on in old_nodes:
        matches = extract_markdown_links(on.text)
        if (not len(matches) and on.text) or on.text_type != text_type_text:
            nodes_split.append(on)
            continue
        for i in range(len(matches)):
            aux_split = on.text.split(f"[{matches[i][0]}]({matches[i][1]})", 1)
            if aux_split[0]:
                nodes_split.append(TextNode(aux_split[0], text_type_text))
            nodes_split.append(TextNode(matches[i][0], text_type_link, matches[i][1]))
            on.text = aux_split[1]
        if on.text:
            nodes_split.append(on)
    return nodes_split


def text_to_textnodes(text: str):
    split_imgs = split_nodes_image([TextNode(text, text_type_text)])
    split_links = split_nodes_link(split_imgs)
    split_bold = split_nodes_delimiter(split_links, "**", text_type_bold)
    split_italic = split_nodes_delimiter(split_bold, "*", text_type_italic)
    split_code = split_nodes_delimiter(split_italic, "`", text_type_code)
    return split_code

from textnode import TextNode, text_type_text, text_type_image, text_type_link
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    nodes_split = []
    for on in old_nodes:
        if delimiter not in on.text or not isinstance(on, TextNode):
            nodes_split.append(on)
            continue

        aux_split = on.text.split(delimiter, maxsplit=1)
        nodes_split.append(TextNode(aux_split[0], on.text_type))
        if delimiter not in aux_split[1]:
            raise Exception(f"Invalid markdown syntax: closing {delimiter} not found")

        delimiter_has_closed = 1
        while delimiter in aux_split[1]:
            aux_split = aux_split[1].split(delimiter, maxsplit=1)
            nodes_split.append(
                TextNode(
                    aux_split[0],
                    text_type if delimiter_has_closed % 2 else on.text_type,
                )
            )
            delimiter_has_closed += 1

        if delimiter_has_closed % 2:
            raise Exception(f"Invalid markdown syntax: closing {delimiter} not found")

        if len(aux_split[1]):
            nodes_split.append(TextNode(aux_split[1], on.text_type))
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

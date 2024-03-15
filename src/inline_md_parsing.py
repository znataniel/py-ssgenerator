from textnode import TextNode
import re


def split_nodes_delimiter(old_nodes: list, delimiter, text_type):
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

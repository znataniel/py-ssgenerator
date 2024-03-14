from textnode import TextNode


def main():
    my_textnode = TextNode("This is a text node.", "bold", "https://www.boot.dev")
    my_other_textnode = TextNode(
        "This is another text node.", "bold", "https://www.gnu.org"
    )
    print(my_textnode)
    print(my_other_textnode)
    print(f"{my_textnode} == {my_other_textnode}? {my_textnode == my_other_textnode}")


main()

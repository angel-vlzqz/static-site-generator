import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertEqual(node.url, "https://www.google.com")
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, "This is a text node")

    def test_url_default(self):
        node = TextNode("This is a text node")
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()

import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="This is a html node", props={"class": "test"})
        node2 = HTMLNode(tag="p", value="This is a html node", props={"class": "test"})
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("This is a html node")
        node2 = HTMLNode("This is a html node 2")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("This is a html node")
        self.assertEqual(repr(node), "HTMLNode: tag=This is a html node, value=None, children=None, props=None")

    def test_props_to_html (self):
        node = HTMLNode("This is a html node", props={"class": "test"})
        self.assertEqual(node.props_to_html(), ' class="test"')
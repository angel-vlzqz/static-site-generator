import unittest

from htmlnode import HTMLNode
from text_to_html import text_node_to_html_node
from textnode import TextNode, TextType


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

    def test_text(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "This is a text node")
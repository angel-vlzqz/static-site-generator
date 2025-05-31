import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("This is a leaf node")
        node2 = LeafNode("This is a leaf node")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = LeafNode("This is a leaf node")
        node2 = LeafNode("This is a leaf node 2")
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_repr(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")
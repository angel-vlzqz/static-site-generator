import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(tag="p", children=[LeafNode("Hello, world!")])
        node2 = ParentNode(tag="p", children=[LeafNode("Hello, world!")])
        self.assertEqual(node, node2)
    
    def test_to_html_with_children(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_missing_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(children=[LeafNode("Hello, world!")]).to_html()

    def test_missing_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="p").to_html()
import os
from expression_tree import ExpressionTree

def evaluate_expression(expr):
    tree = ExpressionTree(expr)
    return tree.evaluate()

def build_tree_image(expr):
    tree = ExpressionTree(expr)
    image_path = f'static/tree_images/{expr.replace("/", "_")}.png'
    tree.visualize(filename=image_path)
    return '/' + image_path

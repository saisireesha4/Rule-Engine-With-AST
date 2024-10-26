import re


class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # 'operator' or 'operand'
        self.left = left  # Left child node (for operators)
        self.right = right  # Right child node (for operators)
        self.value = value  # For operands, e.g., ('age', '>', 30)

    def evaluate(self, data):
        """Evaluate the AST against the provided data."""
        if self.type == 'operand':
            attribute, operator, target_value = self.value
            return self.evaluate_condition(data[attribute], operator, target_value)
        elif self.type == 'operator':
            if self.value == 'AND':
                return self.left.evaluate(data) and self.right.evaluate(data)
            elif self.value == 'OR':
                return self.left.evaluate(data) or self.right.evaluate(data)

    def evaluate_condition(self, actual_value, operator, target_value):
        """Evaluate a single condition."""
        if operator == '>':
            return actual_value > target_value
        elif operator == '<':
            return actual_value < target_value
        elif operator == '==':
            return actual_value == target_value
        elif operator == '>=':
            return actual_value >= target_value
        elif operator == '<=':
            return actual_value <= target_value
        return False


def create_rule(rule_string):
    """Parse the rule string and return the root Node of the AST."""
    tokens = re.findall(r'\w+|[<>=!]+|\(|\)|AND|OR', rule_string)

    def parse_expression(tokens):
        """Recursively parse the expression into an AST."""
        if len(tokens) == 3:  # operand
            attribute, operator, value = tokens[0], tokens[1], int(tokens[2])
            return Node('operand', value=(attribute, operator, value))
        elif len(tokens) > 3:  # operator with left and right nodes
            left = parse_expression(tokens[:3])
            operator = tokens[3]
            right = parse_expression(tokens[4:])
            return Node('operator', left=left, right=right, value=operator)

    return parse_expression(tokens)


def combine_rules(rule_nodes):
    """Combine multiple rules into one AST."""
    combined = rule_nodes[0]
    for rule in rule_nodes[1:]:
        combined = Node('operator', left=combined, right=rule, value='AND')
    return combined

from src.model import Node


def test_less_than():
    assert Node(value=1) < Node(value=2)
    assert not Node(value=1) < Node(value=0)
    assert Node(value=1) <= Node(value=1)

from components import *

# Positive testing initializers
def test_filter_selector_initializer():
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    filter_selector = FilterSelector(type=test_type, pattern=test_pattern)
    assert filter_selector.type == test_type
    assert filter_selector.pattern == test_pattern


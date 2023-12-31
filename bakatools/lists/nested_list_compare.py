def nested_list_compare(a: int | list, b: int | list) -> int:
    """
    0 for equal, -1 for a < b, 1 for a > b

    If both values are integers, compare them as integers.

    If both values are lists, compare items one by one until they are not equal.
    The list that runs out of items faster is considered smaller.

    If exactly one value is an integer, convert the integer to a list which contains that integer as its only value,
    then retry the comparison.
    """
    match a, b:
        case int(), int():
            return (a > b) - (a < b)
        case list(), list():
            for subcomparison_result in map(nested_list_compare, a, b):
                if subcomparison_result != 0:
                    return subcomparison_result
            return nested_list_compare(len(a), len(b))
        case int(), list():
            return nested_list_compare([a], b)
        case list(), int():
            return nested_list_compare(a, [b])

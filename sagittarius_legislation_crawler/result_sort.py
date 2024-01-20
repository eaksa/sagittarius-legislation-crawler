import json
from re import split

def get_number(s: str) -> int:
    """Gets the number in a string.
    Args:
        s: The string to get the number from.
    Returns:
        The number in the string.
    """
    n = split("-", s)[2]
    try:
        return int(n)
    except:
        return int(n[:-1])

def sort_by_number(l: list[str]) -> list[str]:
    """Sorts a list of strings by the number in the string.
    Args:
        l: The list to sort.
    Returns:
        The sorted list.
    """
    return sorted(l, key=lambda x: get_number(x))

with open("result.json", "r") as f:
    result = json.load(f)

sorted_result = {
    k: {y: sort_by_number(l) for y, l in v.items()} 
    for k, v in result.items()
}

with open("sorted_result.json", "w") as f:
    json.dump(sorted_result, f, indent=4)


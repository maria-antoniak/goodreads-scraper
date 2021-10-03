from typing import Dict, List


def sort_by_value(_dict: Dict[str, int]) -> List[str]:
    return sorted(_dict.items(), key=lambda x: x[1], reverse=True)

import json
from typing import Any

def format_json(data: Any) -> str:
    """
    Formats data as a JSON string.
    """
    return json.dumps(data, indent=4)

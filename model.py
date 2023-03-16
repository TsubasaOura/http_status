from dataclasses import dataclass
from typing import Any, List


@dataclass
class HttpTarget:
    url: str = "google.com"
    status: Any = 0


@dataclass
class HttpData:
    count: int = 0
    datetime: str = ""
    targets: List[HttpTarget] = None


@dataclass
class HttpLog:
    datetime: str = ""
    data: List[HttpData] = None

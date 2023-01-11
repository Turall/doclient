from dataclasses import dataclass
from typing import Optional


@dataclass
class Vpc:
    name: str
    description: Optional[str]
    region: str
    ip_range: Optional[str]

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TaintEffect(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    NoSchedule = auto()
    PreferNoSchedule = auto()
    NoExecute = auto()

    @classmethod
    def get_val(cls, taint: str):
        return TaintEffect(taint).value


@dataclass
class Taints:
    key: str
    value: str
    effect: TaintEffect


@dataclass
class MaintenancePolicy:
    start_time: str
    day: str


@dataclass
class NodePool:
    size: str
    name: str
    count: int
    tags: Optional[list[str]] = None
    labels: Optional[dict] = None
    taints: Optional[list[Taints]] = None
    auto_scale: bool = False
    min_nodes: int = 0
    max_nodes: int = 0


@dataclass
class KubernetesPayload:
    name: str
    region: str
    vpc_uuid: str
    node_pools: list[NodePool]
    version: str = ""
    tags: Optional[list[str]] = None
    maintenance_policy: Optional[MaintenancePolicy] = None
    auto_upgrade: bool = False
    surge_upgrade: bool = False
    ha: bool = False

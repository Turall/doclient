from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel


class TaintEffect(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    NoSchedule = auto()
    PreferNoSchedule = auto()
    NoExecute = auto()

    @classmethod
    def get_val(cls, taint: str):
        return TaintEffect(taint).value


class Options(BaseModel):
    name: str
    slug: str


class K8SVersionsOptions(BaseModel):
    slug: str
    kubernetes_version: str
    supported_features: list[str]


class _K8SClusterOptions(BaseModel):
    regions: list[Options]
    versions: list[K8SVersionsOptions]
    sizes: list[Options]


class K8SClusterOptions(BaseModel):
    options: _K8SClusterOptions


class Taints(BaseModel):
    key: str
    value: str
    effect: TaintEffect

    class Config:
        use_enum_values = True


class MaintenancePolicy(BaseModel):
    start_time: str
    day: str


class ClusterStatus(BaseModel):
    state: str
    message: str


class NodePool(BaseModel):
    size: str
    name: str
    count: int
    tags: Optional[list[str]]
    labels: Optional[dict]
    taints: Optional[list[Taints]]
    auto_scale: bool = False
    min_nodes: int = 0
    max_nodes: int = 0


class NodePoolResponse(NodePool):
    droplet_id: Optional[str]


class KubernetesPayload(BaseModel):
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


class KubernetesUpdatePayload(BaseModel):
    name: str
    tags: Optional[list[str]]
    maintenance_policy: Optional[MaintenancePolicy]
    auto_upgrade: Optional[bool]
    surge_upgrade: Optional[bool]
    ha: Optional[bool]


class KubernetesResponse(KubernetesPayload):
    id: str
    cluster_subnet: str
    service_subnet: str
    registry_enabled: bool
    status: ClusterStatus
    created_at: str
    updated_at: str
    supported_features: list[str]
    endpoint: Optional[str]
    ipv4: Optional[str]


class Kubernetes1clickApps(BaseModel):
    addon_slugs: list[str]
    cluster_uuid: str

from pydantic import BaseModel
from typing import Optional


class _VPCSchema(BaseModel):
    name: str
    description: str
    region: str
    ip_range: str


class VPCSchema(_VPCSchema):
    urn: str
    created_at: str
    id: str
    default: bool


class VPCResponse(BaseModel):
    vpc: VPCSchema


class VPCsSchema(BaseModel):
    vpcs: list[VPCSchema]
    links: dict
    meta: dict


class VPCPayload(_VPCSchema):
    pass

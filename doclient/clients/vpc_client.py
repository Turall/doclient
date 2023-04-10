import os

import aiohttp
from doclient.resources.vpc.schemas import VPCsSchema, VPCPayload, VPCResponse


class VPCclient:
    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key or os.getenv("DO_TOKEN")

        self.api_url = "https://api.digitalocean.com"
        self.base_url = f"{self.api_url}/v2/vpcs"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def get_vpcs(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers=self.headers) as response:
                print(await response.text())
                if response.ok:
                    data = await response.json()
                    return VPCsSchema(**data)

    async def create_vpc(self, vpc_payload: VPCPayload):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url, headers=self.headers, json=vpc_payload.dict()
            ) as response:
                print(await response.text())
                if response.ok:
                    data = await response.json()
                    return VPCResponse(**data)

    async def delete_vpcs(self, vpc_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.base_url}/{vpc_id}", headers=self.headers
            ) as response:
                if response.ok:
                    return True

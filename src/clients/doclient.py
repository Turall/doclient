import os
from dataclasses import asdict

import aiohttp

from src.exceptions.apiexceptions import K8SCreateError
from src.resources.k8s.schemas import KubernetesPayload


class DoClient:
    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key or os.getenv("DO_TOKEN")
        print(self.api_key)
        self.url = "https://api.digitalocean.com/v2/kubernetes/clusters"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def create_k8s_cluster(self, payload: KubernetesPayload):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, json=asdict(payload), headers=self.headers
            ) as response:
                if response.ok:
                    return await response.json()
                raise K8SCreateError(await response.text())

    async def delete_cluster_with_all_depends(self, cluster_id: str):
        url = f"https://api.digitalocean.com/v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources/dangerous"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self.headers) as response:
                print(response.status)


        

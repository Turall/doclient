import os

import aiohttp

from src.exceptions.apiexceptions import K8SCreateError
from src.resources.k8s.schemas import (KubernetesPayload, KubernetesResponse,
                                       KubernetesUpdatePayload)


class DoK8Sclient:
    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key or os.getenv("DO_TOKEN")
        self.base_url = "https://api.digitalocean.com/v2/kubernetes/clusters"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def create_k8s_cluster(self, payload: KubernetesPayload) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url, json=payload.dict(), headers=self.headers
            ) as response:
                if response.ok:
                    data = await response.json()
                    print(data)
                    if data.get("kubernetes_cluster"):
                        return KubernetesResponse(**data.get("kubernetes_cluster"))
                raise K8SCreateError(await response.text())

    async def delete_cluster_with_all_depends(self, cluster_id: str) -> bool:
        url = (
            f"{self.base_url}/{cluster_id}/destroy_with_associated_resources/dangerous"
        )
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self.headers) as response:
                if response.ok:
                    return True
        return False

    async def delete_cluster_selective(
        self,
        cluster_id: str,
        load_balancers: list[str] = None,
        volumes: list[str] = None,
        volume_snapshots: list[str] = None,
    ) -> bool:
        url = (
            f"{self.base_url}/{cluster_id}/destroy_with_associated_resources/selective"
        )
        payload = {
            "load_balancers": load_balancers,
            "volumes": volumes,
            "volume_snapshots": volume_snapshots,
        }
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url, json=payload, headers=self.headers
            ) as response:
                if response.ok:
                    return True
        return False

    async def get_k8s_clusters(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()
        return []

    async def get_k8s_cluster(self, cluster_id: str) -> dict:
        url = f"{self.base_url}/{cluster_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()

    async def update_k8s_cluster(
        self, payload: KubernetesUpdatePayload, cluster_id: str
    ):
        url = f"{self.base_url}/{cluster_id}"
        async with aiohttp.ClientSession() as session:
            async with session.put(
                url, json=payload.dict(exclude_none=True), headers=self.headers
            ) as response:
                if response.ok:
                    return await response.json()

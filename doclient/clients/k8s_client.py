import os

import aiohttp

from doclient.exceptions.apiexceptions import K8SCreateError
from doclient.resources.k8s.schemas import (
    K8SClusterOptions,
    KubernetesPayload,
    KubernetesResponse,
    KubernetesUpdatePayload,
    NodePool,
    Kubernetes1clickApps,
)


class DoK8Sclient:
    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key or os.getenv("DO_TOKEN")
        
        self.api_url = "https://api.digitalocean.com"
        self.base_url = f"{self.api_url}/v2/kubernetes"
        self.addon_apps_url = f"{self.api_url}/v2/1-clicks/kubernetes"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def create_k8s_cluster(self, payload: KubernetesPayload) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/clusters", json=payload.dict(), headers=self.headers
            ) as response:
                if response.ok:
                    data = await response.json()
                    if data.get("kubernetes_cluster"):
                        return KubernetesResponse(**data.get("kubernetes_cluster"))
                raise K8SCreateError(await response.text())

    async def delete_cluster_with_all_depends(self, cluster_id: str) -> bool:
        url = f"{self.base_url}/clusters/{cluster_id}/destroy_with_associated_resources/dangerous"
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
        url = f"{self.base_url}/clusters/{cluster_id}/destroy_with_associated_resources/selective"
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

    async def get_k8s_options(self) -> K8SClusterOptions:
        """
        To list the versions of Kubernetes available for use,
        the regions that support Kubernetes, and the available node sizes
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/options", headers=self.headers
            ) as response:
                if response.ok:
                    data = await response.json()
                    return K8SClusterOptions(**data)

    async def get_k8s_clusters(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/clusters", headers=self.headers
            ) as response:
                if response.ok:
                    return await response.json()
        return []

    async def get_k8s_cluster(self, cluster_id: str) -> dict:
        url = f"{self.base_url}/clusters/{cluster_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()

    async def update_k8s_cluster(
        self, payload: KubernetesUpdatePayload, cluster_id: str
    ):
        url = f"{self.base_url}/clusters/{cluster_id}"
        async with aiohttp.ClientSession() as session:
            async with session.put(
                url, json=payload.dict(exclude_none=True), headers=self.headers
            ) as response:
                if response.ok:
                    return await response.json()

    async def get_and_save_kubeconfig(
        self,
        cluster_id: str,
        path: str = ".",
        filename: str = "config.yaml",
        expiry_seconds: int = 0,
    ):
        url = f"{self.base_url}/clusters/{cluster_id}/kubeconfig?expiry_seconds={expiry_seconds}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    path = f"{path}/{filename}"
                    with open(path, "wb") as w:
                        w.write(await response.content.read())
                    return path

    async def get_k8s_credentials(
        self,
        cluster_id: str,
    ):
        url = f"{self.base_url}/clusters/{cluster_id}/credentials"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()

    async def get_k8s_upgrades(
        self,
        cluster_id: str,
    ):
        url = f"{self.base_url}/clusters/{cluster_id}/upgrades"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()

    async def upgrade_k8s_cluster_version(self, cluster_id: str, version: str):
        url = f"{self.base_url}/clusters/{cluster_id}/upgrade"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json={"version": version}, headers=self.headers
            ) as response:
                if response.ok:
                    return True

    async def get_k8s_node_pools(
        self,
        cluster_id: str,
    ):
        url = f"{self.base_url}/clusters/{cluster_id}/node_pools"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()

    async def add_node_pool_to_k8s_cluster(self, cluster_id: str, node_info: NodePool):
        url = f"{self.base_url}/clusters/{cluster_id}/node_pools"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=node_info.dict(exclude_none=True), headers=self.headers
            ) as response:
                if response.ok:
                    return await response.json()

    async def get_k8s_node_pool(self, cluster_id: str, node_pool_id: str):
        url = f"{self.base_url}/clusters/{cluster_id}/node_pools/{node_pool_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()

    async def update_k8s_node_pool(
        self, payload: NodePool, cluster_id: str, node_pool_id: str
    ):
        url = f"{self.base_url}/clusters/{cluster_id}/node_pools/{node_pool_id}"
        async with aiohttp.ClientSession() as session:
            async with session.put(
                url, json=payload.dict(exclude_none=True), headers=self.headers
            ) as response:
                if response.ok:
                    return await response.json()

    async def delete_k8s_node_pool(self, cluster_id: str, node_pool_id: str):
        url = f"{self.base_url}/clusters/{cluster_id}/node_pools/{node_pool_id}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self.headers) as response:
                return response.ok

    async def delete_k8s_node(
        self,
        cluster_id: str,
        node_pool_id: str,
        node_id: str,
        skip_drain: int = 1,
        replace: int = 0,
    ):
        """
        Appending the skip_drain=1 query parameter to the request causes node draining to be skipped.
        Omitting the query parameter or setting its value to 0 carries out draining prior to deletion.

        Appending the replace=1 query parameter to the request causes the node to be replaced by a new one after deletion.
        Omitting the query parameter or setting its value to 0 deletes without replacement.
        """
        url = f"{self.base_url}/clusters/{cluster_id}/node_pools/{node_pool_id}/nodes/{node_id}?skip_drain={skip_drain}&replace={replace}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self.headers) as response:
                return response.ok

    async def get_k8s_associated_user(self, cluster_id: str):
        url = f"{self.base_url}/clusters/{cluster_id}/user"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.ok:
                    return await response.json()

    # async def run_k8s_clusterlint(self, cluster_id: str, node_info: NodePool):
    #     url = f"{self.base_url}/clusters/{cluster_id}/node_pools"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(
    #             url, json=node_info.dict(exclude_none=True), headers=self.headers
    #         ) as response:
    #             if response.ok:
    #                 return await response.json()

    async def install_1click_to_k8s(self, addon_info: Kubernetes1clickApps):
        url = f"{self.addon_apps_url}"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=addon_info.dict(exclude_none=True), headers=self.headers
            ) as response:
                if response.ok:
                    return await response.json()

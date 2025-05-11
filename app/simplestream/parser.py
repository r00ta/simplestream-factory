import aiohttp
from copy import deepcopy

from app.models.entities import SimplestreamProductArch
from app.simplestream.models import SimplestreamsSourceManifest, SimplestreamsProductManifest


class SimplestreamParser:
    async def download(self, index_url: str) -> SimplestreamsSourceManifest:
        async with aiohttp.ClientSession() as session:
            async with session.get(index_url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch manifest: {response.status}")

                manifest_data = await response.json()
                products = {}
                for product_name in manifest_data["products"].keys():
                    name = product_name
                    arch = SimplestreamProductArch(manifest_data["products"][product_name]["arch"].upper())
                    properties = deepcopy(manifest_data["products"][product_name])
                    del properties["versions"]
                    versions = manifest_data["products"][product_name]["versions"]
                    products.update(
                        {
                            name: SimplestreamsProductManifest(
                                arch=arch,
                                properties=properties,
                                versions=versions
                            )
                        }
                    )
            return SimplestreamsSourceManifest(
                products=products
            )


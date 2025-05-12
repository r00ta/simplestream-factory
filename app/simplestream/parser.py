from copy import deepcopy

import aiohttp

from app.models.entities import SimplestreamProductArch, SimplestreamChannel
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
                    label = manifest_data['products'][product_name]['label']
                    channel = SimplestreamChannel(label.upper())
                    name = product_name.replace(f"com.ubuntu.maas.{label}", "com.r00ta.spaghettihub.stable")
                    arch = SimplestreamProductArch(manifest_data["products"][product_name]["arch"].upper())
                    os = manifest_data["products"][product_name]["os"]
                    properties = deepcopy(manifest_data["products"][product_name])
                    del properties["versions"]
                    versions = manifest_data["products"][product_name]["versions"]
                    products.update(
                        {
                            name: SimplestreamsProductManifest(
                                arch=arch,
                                channel=channel,
                                os=os,
                                properties=properties,
                                versions=versions
                            )
                        }
                    )
            return SimplestreamsSourceManifest(
                products=products
            )


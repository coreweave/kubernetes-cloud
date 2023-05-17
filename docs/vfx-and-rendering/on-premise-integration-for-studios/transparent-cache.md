---
description: Learn more about CloudLink for VFX Cloud Studios
---

# Transparent Cache

## Transparent cache

![Diagram exemplifying the transparent cache connection](../../.gitbook/assets/111335067-772be780-864a-11eb-949c-56ece0902a9d.png)

A pull-through transparent cache can be deployed in CoreWeave Cloud.

Storage for the cache is backed by CoreWeave NVMe or HDD storage, and can be anywhere from `1GB` to `500TB`. The cache allows all on-premise storage to be efficiently accessed without the need to first synchronize files.

When an artist submits a render job, the first render Worker to access an asset will cause that asset to be loaded from on-premise storage and stored in the cache. Subsequent access by other render nodes, or by subsequent render jobs will load the data directly from cache.

When an artist makes a change to an asset, the cache is invalidated and the asset is pulled again on next render. As most assets don't change between iterations, high cache efficiency can be maintained, saving upstream bandwidth from the on-premise location.

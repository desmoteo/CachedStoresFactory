# CachedStoresFactory
Extensible factory for the configuration of custom cached storage interfaces 

## Scope

Imagine you have several remote data sources you want to cache (locally or to another remote but faster resource) using several different caching schemes (TTL - Time To Live, FIFO - First In First Out, etc). This factory allows to quickly implement Store interfaces and combine them to build a caching mechanism as desired. 

## Examples

### Example 1

Suppose you want to cache S3 requests on local temporary Files, using a TTL cahce with retention of 60 secons.
You can build the desired configuration and read data from the store as follows:

```python
from cached_stores_factory.stores.S3_store import S3Store
from cached_stores_factory.stores.tempfile_store import TempfileStore
from cached_stores_factory.caches.TTL_cache import TTLCache
from cached_stores_factory.factories.cached_store_factory import CachedStoreFactory

#Initialize the Factory
CSF = CachedStoreFactory(TempfileStore, S3Store, TTLCache)

#Initialize the Store with the required local target, remote target and cache configuration  
CS = CSF.build(local_target='my_local_store', remote_bucketname='my_bucket', remote_s3_profile='my_profile', remote_s3_region='eu-central-1', cache_interval=60.0)

#"Open" a resource to make it available as file like object
CSFD = CS.open('path/my.file')

#Read Cached Store as regular file
res = CSFD.read()

#Write to Cached Store as regular file 
CSFD.write(my_data)


```

### Example 2

Suppose you want to cache S3 requests from a glacier bucket on a different, frequent access one, using a FIFO cahce with depth of 3 elements.
You can build the desired configuration and read data from the store as follows:

```python
from cached_stores_factory.stores.S3_store import S3Store
from cached_stores_factory.caches.TTL_cache import FIFOCache
from cached_stores_factory.factories.cached_store_factory import CachedStoreFactory

#Initialize the Factory
CSF = CachedStoreFactory(S3Store, S3Store, FIFOCache)

#Initialize the Store with the required local target, remote target and cache configuration  
CS = CSF.build(local_bucketname='my_frequent_bucket', local_s3_profile='my_profile', local_s3_region='eu-central-1', remote_bucketname='my_glacier_bucket', remote_s3_profile='my_profile', remote_s3_region='eu-central-1', cache_size=3)

#"Open" a resource to make it available as file like object
CSFD = CS.open('path/my.file')

#Read Cached Store as regular file
res = CSFD.read()

#Write to Cached Store as regular file 
CSFD.write(my_data)
```

## Documentation

TODO

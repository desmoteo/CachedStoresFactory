# CachedStoresFactory
Extensible factory for the configuration of custom cached storage interfaces 

## Scope

Imagine you have several remote data sources you want to cache (locally -on temporary files or e.g. with redis- or to another remote but faster resource) using several different caching schemes (TTL - Time To Live, FIFO - First In First Out, etc). This factory allows to quickly implement Store interfaces and combine them to build a caching mechanism as desired. 

## Examples

### Example 1 (TTL Cache using Temporary Files)

You want to cache S3 requests on local temporary Files, using a TTL cahce with retention of 60 secons.
You can build the desired configuration and read data from the store as follows:

```python
from cached_stores_factory.stores.S3_store import S3Store
from cached_stores_factory.stores.tempfile_store import TempfileStore
from cached_stores_factory.caches.TTL_cache import TTLCache
from cached_stores_factory.factories.cached_store_factory import CachedStoreFactory

#Initialize the Factory
temp_store = TempfileStore('my_local_store')
s3_store =  S3Store(bucketname='my_bucket', s3_profile='my_profile', s3_region='eu-central-1')
ttl_cache = TTLCache(interval=60.0)

CSF = CachedStoreFactory(temp_store, s3_store, ttl_cache)

#Initialize the Store with the required local target, remote target and cache configuration  
CS = CSF.build()

#"Open" a resource to make it available as file like object
CSFD = CS.open('path/my.file')

#Read Cached Store as regular file
res = CSFD.read()

#Write to Cached Store as regular file 
CSFD.write(my_data)


```

### Example 2 (Cache using Redis)

You want to cache S3 requests on a redis server, with a default retention of 5 minutes.  
You can build the desired configuration and read data from the store as follows:

```python
import redis
from cached_stores_factory.stores.S3_store import S3Store
from cached_stores_factory.stores.redis_store import RedisStore
from cached_stores_factory.factories.cached_store_factory import CachedStoreFactory

#Initialize the Factory
redis_store = RedisStore(host='localhost',port=6379, ex=5*60)
s3_store =  S3Store(bucketname='my_bucket', s3_profile='my_profile', s3_region='eu-central-1')

CSF = CachedStoreFactory(redis_store, s3_store)

#Initialize the Store with the required local target, remote target and cache configuration  
CS = CSF.build()

#"Open" a resource to make it available as file like object
CSFD = CS.open('path/my.file')

#Read Cached Store as regular file
res = CSFD.read()

#Write to Cached Store as regular file 
CSFD.write(my_data)


```
### Example 3 (Fifo Cache using S3 bucket)

You want to cache S3 requests from a glacier bucket on a different, frequent access one, using a FIFO cahce with depth of 3 elements.
You can build the desired configuration and read data from the store as follows:

```python
from cached_stores_factory.stores.S3_store import S3Store
from cached_stores_factory.caches.TTL_cache import FIFOCache
from cached_stores_factory.factories.cached_store_factory import CachedStoreFactory

#Initialize the Factory
s3_frequent_store =  S3Store(bucketname='my_frequent_bucket', s3_profile='my_profile', s3_region='eu-central-1')
s3_infrequent_store =  S3Store(bucketname='my_infrequent_bucket', s3_profile='my_profile', s3_region='eu-central-1')
fifo_cache = TTLCache(interval=60.0)

CSF = CachedStoreFactory(s3_frequent_store, s3_infrequent_store, fifo_cache)

#Initialize the Store with the required local target, remote target and cache configuration  
CS = CSF.build()

#"Open" a resource to make it available as file like object
CSFD = CS.open('path/my.file')

#Read Cached Store as regular file
res = CSFD.read()

#Write to Cached Store as regular file 
CSFD.write(my_data)
```


## Documentation

TODO

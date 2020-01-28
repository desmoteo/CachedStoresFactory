import io
import os
import redis
from cached_stores_factory.stores.base_store import BaseStore
from cached_stores_factory.store_results.store_result import StoreResult


class RedisStore(BaseStore):
    """Store Class based on Temporary dict objects

    """

    def __init__(self, host='localhost', port=6379, ex=60):
        """DictStore constructor

        Args:
            **kwargs: arguments required to properly label a temporary dict store:
                target, a label
        """
        self._pool = redis.connection.ConnectionPool()
        self._conn = redis.Redis(host=host, port=port,
                                 connection_pool=self._pool)
        self._ex = ex

    def _read_proxy(self, key, update=False, **kwargs):
        data = self._conn.get(key)
        res = StoreResult(success=(data is not None), data=data)
        return res

    def _write_proxy(self, key, data, **kwargs):
        ex = kwargs.get('ex', self._ex)
        self._conn.set(key, data, ex=ex)
        res = StoreResult(success=True)
        return res

    def _delete_proxy(self, key):
        self._conn.delete(key)
        res = StoreResult(success=True)
        return res

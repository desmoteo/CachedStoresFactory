import io
import os
from cached_stores_factory.stores.base_store import BaseStore
from cached_stores_factory.store_results.store_result import StoreResult


class DictStore(BaseStore):
    """Store Class based on Temporary dict objects

    """

    def __init__(self, **kwargs):
        """DictStore constructor

        Args:
            **kwargs: arguments required to properly label a temporary dict store:
                target, a label
        """
        self.target_label = kwargs.get('target')
        self.store_dict = {}

    def _read_proxy(self, key, update=False, **kwargs):
        data = self.store_dict.get(key, None)
        res = StoreResult(success=(data is not None), data=data)
        return res

    def _write_proxy(self, key, data, **kwargs):
        self.store_dict[key] = data
        res = StoreResult(success=True)
        return res

    def _delete_proxy(self, key):
        data = self.store_dict.pop(key, None)
        res = StoreResult(success=(data is not None))
        return res

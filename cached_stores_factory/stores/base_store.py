from cached_stores_factory.store_results.store_result import StoreResult

import traceback
class BaseStore():
    """Virtual class representing the interface of a Store

    """

    def __init__(self):
        pass

    def _read_proxy(self, key, update=False, **kwargs):
        raise NotImplementedError()

    def read(self, key, update=False, **kwargs):
        """Read data from Store

        Args:
            key (String): the key to read in the store

        Returns:
            StoreResult: Operation Result containing the data read from store
        """
        try:
            res = self._read_proxy(key, update, **kwargs)
        except Exception as e:
            traceback.print_exc()
            res = StoreResult(success=False, error=e)
        return res

    def _write_proxy(self, key, data, **kwargs):
        raise NotImplementedError()

    def write(self, key, data, **kwargs):
        """Write data to Store

        Args:
            key (String): the key to write in the store
            data (bytes): the data to write at key

        Returns:
            StoreResult: Operation Result
        """
        wdata = data
        if isinstance(wdata, str):
            wdata = wdata.encode()
        try:
            res = self._write_proxy(key, wdata, **kwargs)
        except Exception as e:
            traceback.print_exc()
            res = StoreResult(success=False, error=e)
        return res

    def _delete_proxy(self, key):
        raise NotImplementedError()

    def delete(self, key):
        """Remove key from store

        Args:
            key (String): the key to delete from store

        Returns:
            StoreResult: Operation Result
        """
        try:
            res = self._delete_proxy(key)
        except Exception as e:
            traceback.print_exc()
            res = StoreResult(success=False, error=e)
        return res

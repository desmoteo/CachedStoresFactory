import io
import os
import tempfile
from cached_stores_factory.stores.base_store import BaseStore
from cached_stores_factory.store_results.store_result import StoreResult

class TempfileStore(BaseStore):
    """Store Class based on Temporary Files 

    """

    def __init__(self, **kwargs):
        """TempfileStore constructor

        Args:
            **kwargs: arguments required to properly setup a temporary file store: 
                target, a directory inside the system's /tmp where the temporary files are saved
        """
        self.bucketdir = tempfile.TemporaryDirectory(
            prefix='{0}_'.format(kwargs.get('target')))

    def _read_proxy(self, key):
        fd = open('{0}/{1}'.format(self.bucketdir.name, key), 'rb')
        data = fd.read()
        fd.close()
        res = StoreResult(success=True, data=data)
        return res

    def _write_proxy(self, key, data):
        filepath = '{0}/{1}'.format(self.bucketdir.name, key)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        fd = open(filepath, 'w+b')
        fd.write(data)
        fd.close()
        res = StoreResult(success=True)
        return res

    def _delete_proxy(self, key):
        filepath = '{0}/{1}'.format(self.bucketdir.name, key)
        os.remove(filepath)
        res = StoreResult(success=True)
        return res

import io
import boto3
import tempfile
from cached_stores_factory.stores.base_store import BaseStore
from cached_stores_factory.store_results.store_result import StoreResult


class S3Store(BaseStore):
    """Store class based on AWS S3

    """

    def __init__(self, **kwargs):
        """S3 Store constructor

        Args:
            **kwargs: arguments required to properly setup an S3 store: bucketname,
                s3_profile, s3_region
        """
        self.bucketname = kwargs.get('bucketname')
        self._session = boto3.Session(profile_name=kwargs.get(
            's3_profile'), region_name=kwargs.get('s3_region'))
        self._s3 = self._session.resource('s3')
        self.bucket = self._s3.Bucket(self.bucketname)

    def _read_proxy(self, key):
        s3_obj = self.bucket.Object(key)
        with tempfile.NamedTemporaryFile() as fd:
            s3_obj.download_fileobj(fd)
            fd.flush()
            fd.seek(0)
            data = fd.read()
        res = StoreResult(success=True, data=data)
        return res

    def _write_proxy(self, key, data):
        s3_obj = self.bucket.Object(key)
        bytesdata = io.BytesIO(data)
        s3_obj.upload_fileobj(bytesdata)
        bytesdata.close()
        res = StoreResult(success=True)
        return res

    def _delete_proxy(self, key):
        self.bucket.Object(key).delete()
        res = StoreResult(success=True)
        return res

from cached_stores_factory.store_results.cached_store_result import CachedStoreResult
from cached_stores_factory.stores.base_store import BaseStore


def _remove_prefix(text, prefix):
    """Removes a prefix from a String

    Args:
        text (String): The String to process
        prefix (String): The prefix to lookup

    Returns:
        String: The String with the prefix removed
    """
    return text[text.startswith(prefix) and len(prefix):]


class CachedStoreFD():
    """A class to access Cached Store elements as regular file descriptors

    """

    def __init__(self, key, target_factory):
        self._target_factory = target_factory
        self._key = key

    def read(self, info=None, **kwargs):
        """Reads from CachedStoreFD

        Args:
            info (dict, optional): a dict to share CachedStoreResult. Defaults to None.

        Returns:
            bytes: the store element data
        """

        res = self._target_factory.read(self._key, **kwargs)
        if isinstance(info, dict):
            info.update(res.__dict__)
        return res.data

    def write(self, data, **kwargs):
        """Writes to CachedStoreFD

        Args:
            data (bytes): data to be written to store
        """
        self._target_factory.write(self._key, data, **kwargs)

    def delete(self):
        self._target_factory.delete(self._key)


class CachedStore():
    """Helper class to open store elements as regular files, invoking the requested factory

    Returns:
        CachedStoreFD: a file like object,
            allowing to operate on store elemnts as regular files
    """

    def __init__(self, target_factory):
        self._target_factory = target_factory

    def open(self, key):
        """Builds a CachedStoreFD to acces store elements as regular files

        Args:
            key (String): the store element to access

        Returns:
            CachedStoreFD: a file like object to acces store elements as regular files
        """
        return CachedStoreFD(key, self._target_factory)


class CachedStoreFactory(BaseStore):
    """A Factory to compose custom cached Stores

    """

    def __init__(self, local_store, remote_store, cache=None):
        """Factory construnctor

        Args:
            local_store: The Store object to use as local store
            remote_store: The Store objecy to use as remote store
            cache: The cache object to use, if desired

        Returns:
            CachedStoreFactory: A CachedStoreFactory isntance implementing the desired Cached Store
        """
        self.local_store = local_store
        self.remote_store = remote_store
        self.cache = cache

    def add_to_cache(self, key):
        """Adds a key to the explicit cache, if defined

        Args:
            key (String): The key to add to the explicit cache

        Returns:
            n/a: implementation dependent
        """
        if self.cache is not None:
            return self.cache.add_to_cache(key)
        return None

    def check(self, key):
        """Checks the key in the explicit cache, if defined

        Args:
            key (String): the key to lookup in the explicit cache

        Returns:
            bool: The result of the lookup
        """
        if self.cache is not None:
            return self.cache.check(key)
        return True

    def delete_from_cache(self, key):
        """Deletes the key from the explicit cache, if defined

        Args:
            key (String): the key to delete from the explicit cache

        Returns:
            n/a: implementation dependent
        """
        if self.cache is not None:
            return self.cache.delete_from_cache(key)
        return None

    def _push_to_cache(self, key, data, **kwargs):
        """Add key entry to cache

        Args:
            key (String): the key to persist in cache
            data (bytes): the data corresponding to key

        Returns:
            [type]: [description]
        """
        local_res = self.local_store.write(key, data, **kwargs)
        if local_res.success:
            self.add_to_cache(key)
            local_res = self.local_store.read(key)
            if not local_res.success:
                print('Local Store save failed: {0}'.format(
                    local_res.error))
        else:
            print('Local Store save failed: {0}'.format(
                local_res.error))
        return local_res

    def _read_proxy(self, key, update=False, **kwargs):
        """Reads record from cached store 

        Args:
            key (String): the key to lookup in cached store
            update (bool, optional): . Defaults to False.

        Returns:
            CachedStoreResult: Operation result
        """
        in_cache = False if update else self.check(key)
        if in_cache:
            res = self.local_store.read(key)
            if not res.success:
                in_cache = False
                print(
                    'Local file not found ({0}), falling back to remote!'.format(res.error))
                res = self.remote_store.read(key)
                self.delete_from_cache(key)
                if res.success:
                    res = self._push_to_cache(key, res.data, **kwargs)
        else:
            res = self.remote_store.read(key,)
            if res.success:
                res = self._push_to_cache(key, res.data, **kwargs)

        return CachedStoreResult(res, in_cache)

    def _write_proxy(self, key, data, **kwargs):
        """Writes record to cached store

        Args:
            key (String): the key to write in cached store
            data (bytes): the data to write in cache store for key

        Returns:
            CachedStoreResult: Operation result
        """
        res = self.remote_store.write(key, data, **kwargs)
        print(res.success)
        if res.success:
            res = self._push_to_cache(key, data, **kwargs)
        return CachedStoreResult(res, False)

    def _delete_proxy(self, key):
        """Deletes record from cahced store

        Args:
            key (String): the key to delete from cached store

        Returns:
            CachedStoreResult: Operation result
        """
        self.delete_from_cache(key)
        remote_res = self.remote_store.delete(key)
        local_res = self.local_store.delete(key)
        if not remote_res.success:
            return CachedStoreResult(remote_res, False)
        if not local_res.success:
            return CachedStoreResult(local_res, False)
        return CachedStoreResult(remote_res, False)

    def build(self):
        """Build the desired CachedStore

        Returns:
            CachedStore: A Cached Store configured as desired by means of the Factory
        """
        return CachedStore(self)

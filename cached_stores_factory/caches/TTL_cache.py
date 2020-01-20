import datetime
from cached_stores_factory.caches.base_cache import BaseCache


class TTLCache(BaseCache):
    """Implements a Time To Live Cache, by means of a simple Python Dictionary

    """

    def __init__(self, **kwargs):
        """**kwargs must include arg "limit", 
        a Float specifying the duration of cache records in seconds
        """
        self.limit = kwargs.get('limit', 60.0)
        self.kv = {}

    def _add_to_cache_proxy(self, key):
        """Adds the key to Cache dictionary

        Args:
            key (String): The key to be cached 
        """
        self.kv[key] = datetime.datetime.now().timestamp()

    def _check_proxy(self, key):
        """Checks if a key is cached

        Args:
            key (String): The key to be looked up

        Returns:
            Bool: Whether the key was found or not in the cache
        """
        el = self.kv.get(key)
        res = False
        if el is not None:
            res = True
        return res

    def _check_expired_proxy(self):
        """Checks expired keys and cleans up cache

        Returns:
            List: a list of deletable keys
        """
        deletable = []
        for key in self.kv:
            el = self.kv.get(key)
            now = datetime.datetime.now().timestamp()
            if (now - el) >= self.limit:
                deletable.append(key)
            else:
                break
        for key in deletable:
            self.kv.pop(key)
        return deletable

    def _delete_from_cache_proxy(self, key):
        """Deletes a key from cache

        Args:
            key (String): The key to remove from cache
        """
        if key in self.kv:
            self.kv.pop(key)

    def get_cache_status(self):
        """Returns info about the status of the cache

        Returns:
            List: The TTL Dictionary list
        """
        return dict(self.kv)

    def delete_local(self, key):
        """Deletes local coopy of entry key

        Args:
            key (String): The store entry key

        Raises:
            NotImplementedError: Implemented at execution time by the Factory!
        """
        raise NotImplementedError()

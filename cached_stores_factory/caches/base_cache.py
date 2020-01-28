class BaseCache():
    """Virtual base class for Caches, implementing common logic to various possible cache implementations

    """

    def __init__(self, **kwargs):
        pass

    def _add_to_cache_proxy(self, key):
        """Adds a key to the cache, Implementation Specific

        Args:
            key {String} -- The key to be cached

        Raises:
            NotImplementedError: Virtual Methond, to be implemented in derived class
        """
        raise NotImplementedError()

    def add_to_cache(self, key):
        """Adds a key to the cache

        Args:
            key {String} -- The key to be cached

        Returns:
            Unknown -- Implementation specific of derived classes
        """
        self.delete_from_cache(key)
        ret = self._add_to_cache_proxy(key)
        self.check_expired()
        return ret

    def _check_proxy(self, key):
        """Checks if a key is cached, Implementation Specific

        Args:
            key {String} -- The key to look up in the cache

        Raises:
            NotImplementedError: Implementation specific of derived classes
        """
        raise NotImplementedError()

    def check(self, key):
        """Checks if a key is cached

        Args:
            key {String} -- The key to look up in the cache

        Returns:
            Bool -- Whether the key was found or not in the cache
        """
        self.check_expired()
        return self._check_proxy(key)

    def _check_expired_proxy(self):
        """Checks expired keys and cleans up cache, Implementation Specific

        Raises:
            NotImplementedError: Implementation specific of derived classes
        """
        raise NotImplementedError()

    def check_expired(self):
        """Checks expired keys and cleans up cache
        """
        deletable = self._check_expired_proxy()
        return deletable

    def _delete_from_cache_proxy(self, key):
        """Deletes a key from cache, implelentations specific

        Args:
            key {String} -- The key to remove from cache

        Raises:
            NotImplementedError: Implementation specific of derived classes
        """
        raise NotImplementedError()

    def delete_from_cache(self, key):
        """Deletes a key from cache

        Args:
            key {String} -- The key to remove from cache

        Returns:
            Unknown -- Implementation specific of derived classes
        """
        self.check_expired()
        return self._delete_from_cache_proxy(key)

    def get_cache_status(self):
        """Returns info about the status of the cache

        Raises:
            NotImplementedError: Implementation specific of derived classes
        """
        raise NotImplementedError()

from cached_stores_factory.caches.base_cache import BaseCache


class FIFOCache(BaseCache):
    """Implements a First In First Out Cache, by means of a simple Python list

    """

    def __init__(self, **kwargs):
        """**kwargs must include arg "size", an Int specifying the lenght of the FIFO
        """
        super(FIFOCache, self).__init__()
        self.fifo = []
        self.size = kwargs.get('size', 4)
        print('Fifo Cache with size: {0}'.format(self.size))

    def _add_to_cache_proxy(self, key):
        """Appends key to FIFO

        Args:
            key (String): The key to be cached 
        """
        self.fifo.append(key)

    def _check_proxy(self, key):
        """Checks if a key is cached

        Args:
            key (String): The key to be looked up

        Returns:
            Bool: Whether the key was found or not in the cache
        """

        return key in self.fifo

    def _check_expired_proxy(self):
        """Checks expired keys and cleans up cache

        Returns:
            List: a list of deletable keys
        """
        deletable = []
        while len(self.fifo) > self.size:
            deletable.append(self.fifo.pop(0))
        return deletable

    def _delete_from_cache_proxy(self, key):
        """Deletes a key from cache

        Args:
            key (String): The key to remove from cache
        """
        if key in self.fifo:
            idx = self.fifo.index(key)
            self.fifo.pop(idx)

    def get_cache_status(self):
        """Returns info about the status of the cache

        Returns:
            List: The FIFO list
        """
        return self.fifo

    def delete_local(self, key):
        """Deletes local coopy of entry key

        Args:
            key (String): The store entry key

        Raises:
            NotImplementedError: Implemented at execution time by the Factory!
        """
        raise NotImplementedError()

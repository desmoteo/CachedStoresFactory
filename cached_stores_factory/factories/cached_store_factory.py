from cached_stores_factory.store_results.cached_store_result import CachedStoreResult

def _remove_prefix(text, prefix):
    """Removes a prefix from a String

    Args:
        text (String): The String to process
        prefix (String): The prefix to lookup

    Returns:
        String: The String with the prefix removed
    """
    return text[text.startswith(prefix) and len(prefix):]


class CachedStoreFactory():
    """A Factory to compose custom cached Stores

    """

    def __init__(self, LocalSuper, RemoteSuper, CacheSuper):
        """Factory construnctor

        Args:
            LocalSuper (Class): The Store class to use as local store
            RemoteSuper (Class): The Store class to use as remote store
            CacheSuper (Class): The cache class to use

        Returns:
            CachedStoreFactory: A CachedStoreFactory isntance implementing the desired Cached Store
        """
        class LocalClass(LocalSuper):
            """Local Store class implementing the local methods

            """

            def read_local(self, key):
                """Local store read method

                Args:
                    key (String): the key to loopup in store

                Returns:
                    StoreResult: The result of the Store Operation
                """
                return super()._read_proxy(key)

            def write_local(self, key, data):
                """Local store write method

                Args:
                    key (String): the key to write in store
                    data (bytes): the bytearray to write to store

                Returns:
                    StoreResult: The result of the Store Operation
                """
                return super()._write_proxy(key, data)

            def delete_local(self, key):
                """Local store delete method

                Args:
                    key (String): the key to write in store

                Returns:
                    StoreResult: The result of the Store Operation
                """
                return super()._delete_proxy(key)

        class RemoteClass(RemoteSuper):
            """Remote Store class implementing the remote methods

            """

            def read_remote(self, key):
                """Remote store read method

                Args:
                    key (String): the key to loopup in store

                Returns:
                    StoreResult: The result of the Store Operation
                """
                return super()._read_proxy(key)

            def write_remote(self, key, data):
                """Remote store write method

                Args:
                    key (String): the key to loopup in store
                    data (bytes): the bytearray to write to store

                Returns:
                    StoreResult: The result of the Store Operation
                """
                return super()._write_proxy(key, data)

            def delete_remote(self, key):
                """Remote store delete method

                Args:
                    key (String): the key to loopup in store

                Returns:
                    StoreResult: The result of the Store Operation
                """
                return super()._delete_proxy(key)

        class TargetClass(LocalClass, RemoteClass, CacheSuper):
            """Target Store Class

            Args:
                LocalClass (Class): The Store class to use as local store
                RemoteClass (Class): The Store class to use as remote store
                CacheSuper (Class): The cache class to use

            """

            def __init__(self, local_options, remote_options, cache_options):
                """Target Store constructor

                Args:
                    local_options (Dict): Local Store kwargs
                    remote_options (Dict): Remote Store kwargs
                    cache_options (Dict): Cache kwarg
                """
                LocalClass.__init__(self, **local_options)
                RemoteClass.__init__(self, **remote_options)
                CacheSuper.__init__(self, **cache_options)

            def _push_to_cache(self, key, data):
                """Add key entry to cache

                Args:
                    key (String): the key to persist in cache
                    data (bytes): the data corresponding to key

                Returns:
                    [type]: [description]
                """
                local_res = self.write_local(key, data)
                if local_res.success:
                    self.add_to_cache(key)
                    local_res = self.read_local(key)
                    if not local_res.success:
                        print('Local Store save failed: {0}'.format(
                            local_res.error))
                else:
                    print('Local Store save failed: {0}'.format(
                        local_res.error))
                return local_res

            def _read_proxy(self, key, update=False):
                """Reads record from cached store 

                Args:
                    key (String): the key to lookup in cached store
                    update (bool, optional): . Defaults to False.

                Returns:
                    CachedStoreResult: Operation result
                """
                in_cache = False if update else self.check(key) 
                if in_cache:
                    res = self.read_local(key)
                    if not res.success:
                        print(
                            'Local file not found ({0}), falling back to remote!'.format(res.error))
                        res = self.read_remote(key)
                        self._delete_from_cache(key)
                        if res.success:
                            res = self._push_to_cache(key, res.data)
                else:
                    res = self.read_remote(key,)
                    if res.success:
                        res = self._push_to_cache(key, res.data)

                return CachedStoreResult(res, in_cache)

            def _write_proxy(self, key, data):
                """Writes record to cached store

                Args:
                    key (String): the key to write in cached store
                    data (bytes): the data to write in cache store for key

                Returns:
                    CachedStoreResult: Operation result
                """
                res = self.write_remote(key, data)
                print(res.success)
                if res.success:
                    res = self._push_to_cache(key, data)
                return CachedStoreResult(res, False)

            def _delete_proxy(self, key):
                """Deletes record from cahced store

                Args:
                    key (String): the key to delete from cached store

                Returns:
                    CachedStoreResult: Operation result
                """
                self._delete_from_cache(key)
                remote_res = self.delete_remote(key)
                local_res = self.delete_local(key)
                if not remote_res.success:
                    return CachedStoreResult(remote_res, False)
                if not local_res.success:
                    return CachedStoreResult(local_res, False)
                return CachedStoreResult(remote_res, False)

        self._target_class = TargetClass

    def build(self, **kwargs):
        """Build the cahced store instance corresponding to the required configuration

        Args:
            **kwargs: a list of arguments required to configure the desired subclasses.
                Prefix is used to redirect kwargs to required bas class:
                local_ for Local Store configuration
                remote_ for Remote Store configuration
                cache_ for cache configuration.
                See examples  and documentation for details
        Returns:
            TargetClass: A target class instance compiled as requested
        """
        local_params = {}
        remote_params = {}
        cache_params = {}
        for k in kwargs:
            if k.startswith('local_'):
                local_params[_remove_prefix(k, 'local_')] = kwargs[k]
            elif k.startswith('remote_'):
                remote_params[_remove_prefix(k, 'remote_')] = kwargs[k]
            elif k.startswith('cache_'):
                cache_params[_remove_prefix(k, 'cache_')] = kwargs[k]

        print(local_params, remote_params, cache_params)
        return self._target_class(local_params, remote_params, cache_params)

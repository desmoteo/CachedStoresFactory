from .store_result import StoreResult


class CachedStoreResult(StoreResult):
    """Helper class to store a cached store operation result

    """

    def __init__(self, store_result, cached=False):
        """CachedStoreResult constructor

        Args:
            store_result (StoreResult): the reference store operation result
            cached (bool, optional): if the operation target was in the cache. Defaults to False.
        """
        super().__init__(success=store_result.success, error=store_result.error,
                         data=store_result.data)
        self.cached = cached

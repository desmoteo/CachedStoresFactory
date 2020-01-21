class StoreResult():
    """Helper class to store a store operation result

    """

    def __init__(self, success=False, error=None, data=None):
        """StoreResult constructor

        Args:
            success (bool, optional): the operation completed without error. Defaults to False.
            error ([type], optional): the error message, in case of error. Defaults to None.
            data ([type], optional): the data returned by the operation, in case of read.
                Defaults to None.
        """
        self.success = success
        self.error = error
        self.data = data

    def read(self):
        """Reads Data, to be Used as FD

        Returns:
            bytes: Returns data
        """
        return self.data

from threading import Lock


class SharedList:
    """
    This class manages a shared list of objects with thread safety.
    """

    def __init__(self):
        self._lock = Lock()
        self._list = []

    def add(self, item):
        """
        Adds an item to the shared list.
        """
        with self._lock:
            self._list.append(item)

    def remove(self, item):
        """
        Removes an item from the shared list.
        """
        with self._lock:
            self._list.remove(item)

    def get(self, index):
        """
        Gets an item from the shared list by index.
        """
        with self._lock:
            return self._list[index]
        
    def size(self):
        """
        Returns the size of the shared list.
        """
        with self._lock:
            return len(self._list)

    def iter(self):
        """
        Provides an iterator for the shared list.
        """
        with self._lock:
            return iter(self._list)

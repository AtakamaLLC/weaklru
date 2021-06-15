import threading
from collections import OrderedDict
from contextlib import suppress
from typing import Generic, TypeVar, Optional, Dict, cast, Tuple, Iterable
from weakref import WeakValueDictionary

K = TypeVar("K")
V = TypeVar("V")

class WeakLRU(Generic[K, V]):
    """Combines an LRU cache with a WeakValueDictionary.

    Acts as an LRU cache, while also acting as a weak-ref cache.

    To change the locking strategy, replace Lock() class or lock instance
    """
    Lock = threading.Lock

    def __init__(self, capacity: int):
        if not capacity:
            raise ValueError("WeakLRU must have max_size")
        self._capacity = capacity
        self._weak_dict: WeakValueDictionary[K, V] = WeakValueDictionary()
        self._lru_dict: OrderedDict[K, V] = OrderedDict()
        self.lock = self.Lock()

    def set(self, k: K, v: V):
        with self.lock:
            self._weak_dict[k] = v
            self._lru_dict[k] = v
            if len(self._lru_dict) > self._capacity:
                self._lru_dict.popitem(last=False)

    def get(self, k: K, default: Optional[V] = None) -> Optional[V]:
        with self.lock:
            with suppress(KeyError):
                self._lru_dict.move_to_end(k)
            return self.peek(k, default)

    def peek(self, k: K, default: Optional[V] = None) -> Optional[V]:
        return self._lru_dict.get(k, self._weak_dict.get(k, default))

    def items(self) -> Iterable[Tuple[K, V]]:
        with self.lock:
            for k, v in self._weak_dict:
                if k not in self._lru_dict:
                    yield k, v
            for k, v in self._lru_dict:
                yield k, v

    def __len__(self) -> int:
        with self.lock:
            return sum(1 for el in self.items())

    def __delitem__(self, key):
        with self.lock:
            if key in self._lru_dict:
                del self._lru_dict[key]
                if key in self._weak_dict:
                    del self._weak_dict[key]
            else:
                del self._weak_dict[key]

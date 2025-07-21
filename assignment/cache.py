import time
import threading
from collections import OrderedDict, defaultdict

class SmartCache:
    def __init__(self, capacity=10, eviction_policy='LRU'):
        self.capacity = capacity
        self.eviction_policy = eviction_policy.upper()
        self.cache = OrderedDict()           # For FIFO and LRU
        self.expiry = {}                     # TTL expiration tracker
        self.frequency = defaultdict(int)    # For LFU
        self.lru_order = []                  # For LRU tracking
        self.lock = threading.RLock()        # Thread-safe access

    def write(self, key, value=None, ttl=None):
        with self.lock:
            self._remove_expired_keys()

        
            if isinstance(key, list) and value is None:
                for k, v in key:
                    self.write(k, v, ttl)
                return

            if key in self.cache:
                self.delete(key)

            if len(self.cache) >= self.capacity:
                self._evict()

            self.cache[key] = value
            self.expiry[key] = time.time() + ttl if ttl else None
            self.frequency[key] = 1
            self._update_lru(key)


    def read(self, key):
        with self.lock:
            self._remove_expired_keys()
            if key in self.cache:
                self.frequency[key] += 1
                self._update_lru(key)
                return self.cache[key]
            return None

    def delete(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
            if key in self.expiry:
                del self.expiry[key]
            if key in self.frequency:
                del self.frequency[key]
            if key in self.lru_order:
                self.lru_order.remove(key)

    def search(self, predicate):
        with self.lock:
            self._remove_expired_keys()
            return {k: v for k, v in self.cache.items() if predicate(k, v)}

    def _update_lru(self, key):
        if self.eviction_policy == 'LRU':
            if key in self.lru_order:
                self.lru_order.remove(key)
            self.lru_order.append(key)

    def _evict(self):
        with self.lock:
            self._remove_expired_keys()
            if not self.cache:
                return

            if self.eviction_policy == 'FIFO':
                oldest_key = next(iter(self.cache))
                print(f"Evicting (FIFO): {oldest_key}")
                self.delete(oldest_key)

            elif self.eviction_policy == 'LRU':
                if self.lru_order:
                    lru_key = self.lru_order.pop(0)
                    print(f"Evicting (LRU): {lru_key}")
                    self.delete(lru_key)

            elif self.eviction_policy == 'LFU':
                min_freq = min(self.frequency.values())
                candidates = [k for k, f in self.frequency.items() if f == min_freq]
                for key in self.cache:
                    if key in candidates:
                        print(f"Evicting (LFU): {key}")
                        self.delete(key)
                        break

    def _remove_expired_keys(self):
        now = time.time()
        expired = [k for k, exp in self.expiry.items() if exp is not None and now > exp]
        for k in expired:
            print(f"Removing expired key: {k}")
            self.delete(k)

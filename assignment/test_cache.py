from cache import SmartCache
import time

# test_cache for LRU eviction strategy with TTL implementation showing expiration keys.


cache = SmartCache(capacity=2, eviction_policy='LRU')

cache.write("a", 5, ttl=2)
cache.write("b",6, ttl=2)
print("After 2 writes:", list(cache.cache.keys()))

cache.write("c", "cherry", ttl=2) 
print("After 3rd write (eviction expected):", list(cache.cache.keys()))

print("Read b:", cache.read("b"))
time.sleep(5)
print("Read a:", cache.read("a"))  


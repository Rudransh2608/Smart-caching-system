from cache import SmartCache
import time

# test_cache for FIFO eviction strategy showing a list data type used and results after the cache is full.

cache = SmartCache(capacity=2, eviction_policy='FIFO')

cache.write("a", ["hello","hye"], ttl=5)
cache.write("b", "banana", ttl=5)
print("After 2 writes:", list(cache.cache.keys()))

cache.write("c", "cherry", ttl=5)  
print("After 3rd write (eviction expected):", list(cache.cache.keys()))

cache.write("d",["hello","hii"],ttl=5)

print("Read b:", cache.read("b"))
print("Read a:", cache.read("a")) 
print(cache.read("d"))

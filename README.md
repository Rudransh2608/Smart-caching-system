<h1>🧠 SmartCache – Python In-Memory Caching System</h1>
SmartCache is a flexible and intelligent in-memory cache system implemented in Python. It supports:

Multiple eviction policies (LRU, LFU, FIFO)

Time-to-Live (TTL) based expiration

Thread-safe operations for concurrent reads/writes

Multi-type value support (strings, lists, numbers, etc.)

Scalable batch writes, efficient eviction of old/stale data

✅ Key Features
🔁 Eviction Policies: FIFO, LRU, LFU

🕒 TTL Expiry: Auto-removal of expired items using time checks

🔒 Thread-safe using RLock for concurrency

🧠 Custom Search Support via predicate function

⚡ Batch Write for multiple key-value pairs

🔎 Efficient Reads & Deletes

🛠️ How It Works
✅ Example: cache.write("a", "apple")
This line calls the write() method, which:

Checks for existing/expired keys.

Evicts a key if capacity is full (based on eviction policy).

Stores the key-value pair in an internal OrderedDict:

python
Copy
Edit
self.cache["a"] = "apple"
Tracks TTL using a dictionary:

python
Copy
Edit
self.expiry["a"] = current_time + ttl (if given)
Internally, your cache now contains: {"a": "apple"}

🔑 Core Methods
write(key, value, ttl=None)
Stores a key-value pair in cache.

Supports batch insert using a list of tuples.

Automatically evicts a key if the cache is full.

Sets TTL if provided.

read(key)
Returns the value for a key if it exists and is not expired.

Updates LRU/LFU frequency.

delete(key)
Removes a key from cache, TTL tracker, frequency, and LRU list.

search(predicate)
Custom search using lambda functions or any function that takes (key, value) and returns a Boolean.

🔁 Eviction Policies
📦 FIFO (First-In, First-Out)
Evicts the oldest inserted key when full.

📌 LRU (Least Recently Used)
Evicts the least recently accessed key.

📉 LFU (Least Frequently Used)
Evicts the least frequently accessed key.

Frequency updated on every read.

⏳ TTL Expiry Handling
TTL (Time-To-Live) allows you to set expiry duration in seconds.

Expired keys are automatically removed when:

A read/write is attempted.

Internal _remove_expired_keys() checks each TTL.

Example:

python
Copy
Edit
cache.write("a", "apple", ttl=2)
time.sleep(3)
print(cache.read("a"))  # Outputs: None (expired)
🧵 Thread-Safety & Concurrent Access
Uses threading.RLock() for safe access in multi-threaded environments.

Every method (read, write, delete, etc.) uses a with self.lock: block to prevent race conditions.

⚙️ Handling Large Datasets & Memory Limits
capacity defines the maximum number of items allowed.

When full, the cache evicts old entries based on the eviction policy.

Supports scalable batch writes like:

python
Copy
Edit
cache.write([("a", "apple"), ("b", "banana")], ttl=5)
💡 Supports Multiple Data Types
You can store:

Strings: "apple"

Numbers: 123

Lists: ["a", "b", "c"]

Even complex objects (like dictionaries)

This is possible because Python dictionaries allow any hashable key and any value.

🔍 Custom Search Example
python
Copy
Edit
# Find all keys whose value is a fruit name
results = cache.search(lambda k, v: isinstance(v, str) and v in ["apple", "banana"])
📦 Test Case Highlights
✅ Test Case 1: LRU with TTL
python
Copy
Edit
cache = SmartCache(capacity=2, eviction_policy='LRU')
cache.write("a", 5, ttl=2)
cache.write("b", 6, ttl=2)
cache.write("c", "cherry", ttl=2)  # Evicts "a"
time.sleep(5)
print(cache.read("a"))  # Expired, returns None
✅ Test Case 2: LFU + Batch Writes
python
Copy
Edit
cache = SmartCache(capacity=10, eviction_policy='LFU')
cache.write([("a", "apple"), ("b", "tomato")], ttl=2)
for _ in range(3): cache.read("b")  # b has high frequency
cache.write("e", "mango", ttl=2)    # Evicts least used key
✅ Test Case 3: FIFO with List Values
python
Copy
Edit
cache = SmartCache(capacity=2, eviction_policy='FIFO')
cache.write("a", ["hello", "hye"], ttl=5)
cache.write("b", "banana", ttl=5)
cache.write("c", "cherry", ttl=5)  # Evicts "a"

from flask_caching import Cache
from flask import request
my_cache = Cache(config={'CACHE_TYPE':  "SimpleCache"})

def clear_cache_on_request_body_change(timeout=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            # Generate a cache key that includes the request body
            cache_key = f"api_data:{request.data}"

            # Check if the data is already cached
            cached_data = my_cache.get(cache_key)
            if cached_data is not None:
                return cached_data

            # If the data is not cached, process it
            processed_data = f(*args, **kwargs)

            # Store the processed data in the cache with the specified timeout
            my_cache.set(cache_key, processed_data, timeout=timeout)

            return processed_data

        return wrapper

    return decorator


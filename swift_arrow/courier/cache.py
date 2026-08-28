answer_cache = {}
cache_order = []    

CACHE_LIMIT = 10


def get_from_cache(key):
    if key not in answer_cache:
        return None

    # Move the key to the end because it was just used
    if key in cache_order:
        cache_order.remove(key)

    cache_order.append(key)
    return answer_cache[key]




def save_to_cache(key, answer):
    if key in answer_cache:
        answer_cache[key] = answer

        if key in cache_order:
            cache_order.remove(key)

        cache_order.append(key)
        return

    answer_cache[key] = answer
    cache_order.append(key)

    if len(cache_order) > CACHE_LIMIT:
        oldest_key = cache_order.pop(0)

        del answer_cache[oldest_key]




def remove_from_cache(key):
    if key in answer_cache:
        del answer_cache[key]

    if key in cache_order:
        cache_order.remove(key)
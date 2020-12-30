from functools import reduce


def zip_with_itself(iterable):
    return list(zip(iterable, iterable))

def non_zero_keys(dictionary):
    # Return keys which have non zero value
    return reduce(lambda acc, key: {**acc, key: dictionary[key]} if dictionary[key] else acc, dictionary, {})

def join_true_values(iterable, string=", "):
    return string.join(filter(lambda s: s, map(lambda x: "" if x is None else x, iterable)))

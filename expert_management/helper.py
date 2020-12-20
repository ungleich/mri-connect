def join_true_values(iterable, string=", "):
    return string.join(filter(lambda s: s, map(lambda x: "" if x is None else x, iterable)))

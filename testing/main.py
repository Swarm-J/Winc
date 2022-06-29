def get_none():
    return None


def flatten_dict(d):
    for v in d.values():
        values_list = []
    
        if isinstance(v, dict):
            values_list.extend(flatten_dict(v))
        else:
            values_list.append(v)
    return values_list
    
d2 = {'a': {'inner_a': 42, 'inner_b': 350}, 'b': 3.14}
# print(d2.values())
print(flatten_dict(d2))

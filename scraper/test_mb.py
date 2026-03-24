import json

def search_keys(d, path=""):
    if isinstance(d, dict):
        for k, v in d.items():
            if any(term in str(k).lower() for term in ['protein', 'serv', 'nutri', 'stock', 'price']):
                if isinstance(v, (str, int, float, bool)):
                    print(f"{path}.{k} = {v}")
            search_keys(v, path+"."+str(k))
    elif isinstance(d, list):
        for i, item in enumerate(d):
            search_keys(item, path+f"[{i}]")

with open('mb_debug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

search_keys(data)

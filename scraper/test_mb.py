import json

with open('mb_debug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = data['props']['pageProps']['data']['results']

# Full attr dump
print("=== ATTR (full dump) ===")
print(json.dumps(results.get('attr', []), indent=2)[:3000])

# Also check availVar for the specific variant we requested (VRNT-165145)
print("\n=== CURRENT VARIANT KEYS ===")
avail = results.get('availVar', {})
# Find the first variant and show its full structure
for key, val in list(avail.items())[:1]:
    print(f"\nVariant key: {key}")
    print(json.dumps(val, indent=2)[:3000])

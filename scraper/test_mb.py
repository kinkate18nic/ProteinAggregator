import json

with open('mb_debug.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = data['props']['pageProps']['data']['results']
avail_var = results.get('availVar', {})

print("=== ALL VARIANT KEYS WITH THEIR sv_id ===")
for var_key, var_data in avail_var.items():
    sv_id = var_data.get('sv_id', '?')
    full_name = var_data.get('fullName', '?')
    oos = var_data.get('oos', '?')
    price = var_data.get('hkUserLoyaltyPricingDto', {}).get('hkNormalOfferPrice', '?')
    print(f"  VRNT-{sv_id} | ₹{price} | OOS={oos} | {full_name}")

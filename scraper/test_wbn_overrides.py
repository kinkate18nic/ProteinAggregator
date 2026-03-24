import json

with open('scraper/data/nutrition_overrides.json', 'r') as f:
    overrides = json.load(f)

# Hardcoded rules based on Wellbeing Nutrition standard sizing:
# Whey = 33g scoop
# Vegan/Plant = 36g scoop
# Creatine Combos = Add 3g to scoop? WBN combos usually just bundle Creatine separately or mix it. We'll use 33g.

with open('public/master_catalog.json', 'r') as f:
    catalog = json.load(f)

for p in catalog:
    if p['brand'] == 'Wellbeing Nutrition':
        pid = p['id']
        if pid not in overrides:
            serv_g = 36 if 'vegan' in pid.lower() or 'plant' in pid.lower() else 33
            
            # Estimate protein if missing
            prot = p['protein_per_serving_g']
            if not prot:
                if 'whey' in pid.lower(): prot = 24
                elif 'vegan' in pid.lower() or 'plant' in pid.lower(): prot = 22
                else: prot = 24
                
            overrides[pid] = {
                "serving_size_g": serv_g,
                "protein_per_serving_g": prot,
                "source": "Estimated based on product type (Vegan=36g/22g, Whey=33g/24-26g) from WBN standards"
            }

with open('scraper/data/nutrition_overrides.json', 'w') as f:
    json.dump(overrides, f, indent=2)
print(f"Updated overrides for {len(overrides)} total items.")

import json

overrides_file = 'scraper/data/nutrition_overrides.json'
with open(overrides_file, 'r') as f:
    overrides = json.load(f)

# Update weight for the 6 missing ones
updates = {
    "wbn-superfood-plant-protein-powder-in-banoffee-pie": {
        "total_weight_g": 500.0,
        "num_servings": 15
    },
    "wbn-superfood-plant-protein-powder-for-women": {
        "total_weight_g": 500.0,
        "num_servings": 16
    },
    "wbn-vegan-protein-flavor-combo": {
        "total_weight_g": 480.0,
        "num_servings": 15
    },
    "wbn-whey-protein-isolate-dark-chocolate-creatine-monohydrate-combo": {
        "total_weight_g": 1000.0,
        "num_servings": 28
    },
    "wbn-unflavored-whey-protein-isolate-creatine-monohydrate-combo": {
        "total_weight_g": 1000.0,
        "num_servings": 28
    },
    "wbn-unflavored-whey-protein-concentrate-creatine-monohydrate-combo": {
        "total_weight_g": 1000.0,
        "num_servings": 30
    }
}

for pid, data in updates.items():
    if pid in overrides:
        overrides[pid].update(data)
    else:
        overrides[pid] = data

with open(overrides_file, 'w') as f:
    json.dump(overrides, f, indent=2)

print("Mapped missing weights for WBN.")

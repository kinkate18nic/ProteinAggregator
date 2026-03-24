import json

overrides_file = 'scraper/data/nutrition_overrides.json'
with open(overrides_file, 'r') as f:
    overrides = json.load(f)

# Update the 5 specific missing ones from screenshots
updates = {
    "wbn-unflavored-whey-protein-isolate-creatine-monohydrate-combo": {
        "serving_size_g": 35.5,
        "protein_per_serving_g": 30.9,
        "source": "Manual override from product label image"
    },
    "wbn-vegan-protein-flavor-combo": {
        "serving_size_g": 32.0,
        "protein_per_serving_g": 22.0,
        "source": "Manual override from product label image"
    },
    "wbn-superfood-plant-protein-powder-in-banoffee-pie": {
        "serving_size_g": 32.0,
        "protein_per_serving_g": 22.12,
        "source": "Manual override from product label image"
    },
    "wbn-superfood-plant-protein-powder-for-women": {
        "serving_size_g": 30.0,
        "protein_per_serving_g": 18.0,
        "source": "Manual override from product label image"
    },
    "wbn-whey-protein-isolate-dark-chocolate-creatine-monohydrate-combo": {
        "serving_size_g": 35.5,
        "protein_per_serving_g": 26.6,
        "source": "Manual override from product label image"
    }
}

for pid, data in updates.items():
    if pid in overrides:
        overrides[pid].update(data)
    else:
        overrides[pid] = data

with open(overrides_file, 'w') as f:
    json.dump(overrides, f, indent=2)

print("Succesfully updated the overrides.")

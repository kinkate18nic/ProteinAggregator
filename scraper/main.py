import json
import datetime
import os

def get_live_price(brand_id, product_url):
    """
    Simulated scraper for initial build. 
    In production, this runs requests/BeautifulSoup to fetch prices from the product_url.
    Mocking this locally prevents us from accidentally spamming D2C websites while testing.
    """
    prices = {
        "nutrabox": 1799.0,
        "muscleblaze": 2299.0,
        "the_whole_truth": 2999.0
    }
    return prices.get(brand_id, 2000.0)

def calculate_quality_metrics(product_data, lab_data):
    metrics = {
        "cost_per_gram": None,
        "is_tested": False,
        "protein_verified_percent": None,
        "quality_score_note": "No Lab Data"
    }
    
    # Base weight (Assuming 1KG for MVP, can be moved to schema later)
    total_weight = 1000 
    live_price = product_data['live_price_inr']

    if lab_data and lab_data.get('is_tested'):
        metrics['is_tested'] = True
        verified_pct = lab_data['protein_verified_percent']
        metrics['protein_verified_percent'] = verified_pct
        
        # Calculate cost per VERIFIED gram of protein
        total_verified_protein = total_weight * (verified_pct / 100)
        metrics['cost_per_gram'] = round(live_price / total_verified_protein, 2)
        metrics['quality_score_note'] = "Verified via Lab"
    else:
        # Fallback to Claimed Percent if untested
        claimed_pct = lab_data.get('protein_claimed_percent') if lab_data else 75.0
        
        # Calculate cost per CLAIMED gram of protein
        total_claimed_protein = total_weight * (claimed_pct / 100)
        metrics['cost_per_gram'] = round(live_price / total_claimed_protein, 2)
        metrics['quality_score_note'] = "Unverified (Claimed)"
        
    return metrics

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    brands_path = os.path.join(script_dir, "data", "brands.json")
    lab_results_path = os.path.join(script_dir, "data", "lab_results.json")
    
    # Output path for the Next.js frontend to consume
    output_dir = os.path.join(os.path.dirname(script_dir), "public")
    os.makedirs(output_dir, exist_ok=True)
    master_catalog_path = os.path.join(output_dir, "master_catalog.json")
    
    try:
        with open(brands_path, "r", encoding="utf-8") as f:
            brands = json.load(f)
            
        with open(lab_results_path, "r", encoding="utf-8") as f:
            lab_results_list = json.load(f)
            
        # O(1) lookups by product_id
        lab_results = {item['product_id']: item for item in lab_results_list}
            
    except FileNotFoundError as e:
        print(f"Error: Required data file missing: {e}")
        return

    master_catalog = []
    print("Starting data scrape...")
    
    for brand in brands:
        brand_id = brand.get("brand_id")
        brand_name = brand.get("brand_name")
        
        for product in brand.get("products", []):
            product_id = product.get("product_id")
            print(f"Scraping: {brand_name} - {product.get('name')}")
            
            # Fetch live price
            live_price = get_live_price(brand_id, product.get("url"))
            product_lab_data = lab_results.get(product_id)
            
            # Core catalog entry
            catalog_entry = {
                "id": product_id,
                "brand": brand_name,
                "product_name": product.get("name"),
                "product_url": product.get("url"),
                "live_price_inr": live_price,
                "last_updated": datetime.datetime.now().isoformat()
            }
            
            # Merge metrics (Tested Vs Untested Cost/Gram)
            metrics = calculate_quality_metrics(catalog_entry, product_lab_data)
            catalog_entry.update(metrics)
            
            if product_lab_data:
                catalog_entry["lab_details"] = product_lab_data
            
            master_catalog.append(catalog_entry)
            
    with open(master_catalog_path, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, indent=2)
        
    print(f"Successfully generated master_catalog.json with {len(master_catalog)} products.")
    print(f"Output saved to: {master_catalog_path}")

if __name__ == "__main__":
    main()

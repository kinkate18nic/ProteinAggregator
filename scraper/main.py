import json
import datetime
import os
import requests
import re
from bs4 import BeautifulSoup

def get_live_price(brand_id, product_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'}
        r = requests.get(product_url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # 1. Advanced Next.js specific extraction
            next_data = soup.find('script', id='__NEXT_DATA__')
            if next_data and next_data.string:
                try:
                    data = json.loads(next_data.string)
                    results = data.get('props', {}).get('pageProps', {}).get('data', {}).get('results', {})
                    hk_pricing = results.get('hkUserLoyaltyPricingDto', {})
                    if 'hkNormalOfferPrice' in hk_pricing:
                        return float(hk_pricing['hkNormalOfferPrice'])
                except:
                    pass
            
            # 2. Generic unescaped HTML DOM extraction
            text = soup.get_text(separator=' ')
            matches = re.findall(r'₹\s*([\d,]+)', text)
            if matches:
                prices = [int(m.replace(',', '')) for m in matches if int(m.replace(',', '')) > 800]
                if prices:
                    return float(prices[0])
    except Exception as e:
        pass
        
    # STRICLY NO FALLBACK!
    return None

def extract_weight_in_grams(name):
    name_lower = name.lower()
    kg_match = re.search(r'([\d.]+)\s*kg', name_lower)
    if kg_match: return int(float(kg_match.group(1)) * 1000)
    g_match = re.search(r'([\d.]+)\s*g\b', name_lower)
    if g_match: return int(float(g_match.group(1)))
    lb_match = re.search(r'([\d.]+)\s*lb', name_lower)
    if lb_match: return int(float(lb_match.group(1)) * 453.592)
    return 1000

def calculate_quality_metrics(product_data, lab_data):
    metrics = {
        "cost_per_gram": None,
        "is_tested": False,
        "total_weight_grams": extract_weight_in_grams(product_data['product_name']),
        "protein_verified_percent": None,
        "protein_claimed_percent": None,
        "quality_score_note": "Data Unavailable"
    }
    
    total_weight = metrics["total_weight_grams"]
    live_price = product_data['live_price_inr']

    # Rule 1: We absolutely cannot build a metric without knowing the exact live price first
    if live_price is None:
        metrics['quality_score_note'] = "Price Unavailable"
        return metrics

    if lab_data and lab_data.get('is_tested'):
        metrics['is_tested'] = True
        verified_pct = lab_data['protein_verified_percent']
        metrics['protein_verified_percent'] = verified_pct
        metrics['protein_claimed_percent'] = lab_data.get('protein_claimed_percent')
        
        if verified_pct:
            total_verified_protein = total_weight * (verified_pct / 100)
            if total_verified_protein > 0:
                metrics['cost_per_gram'] = round(live_price / total_verified_protein, 2)
            metrics['quality_score_note'] = "Verified via Lab"
            
    elif lab_data and lab_data.get('protein_claimed_percent'):
        # We explicitly rely on the labeled claim explicitly mapped in the JSON
        claimed_pct = lab_data['protein_claimed_percent']
        metrics['protein_claimed_percent'] = claimed_pct
        
        total_claimed_protein = total_weight * (claimed_pct / 100)
        if total_claimed_protein > 0:
            metrics['cost_per_gram'] = round(live_price / total_claimed_protein, 2)
        metrics['quality_score_note'] = "Unverified (Claimed)"
    else:
        # Rule 2: If we don't have a verified source OR an exact labeled claim for this product, we abort metric processing completely!
        # NO 75% FALLBACKS.
        metrics['quality_score_note'] = "Missing Protein %"
        
    return metrics

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    brands_path = os.path.join(script_dir, "data", "brands.json")
    lab_results_path = os.path.join(script_dir, "data", "lab_results.json")
    
    output_dir = os.path.join(os.path.dirname(script_dir), "public")
    os.makedirs(output_dir, exist_ok=True)
    master_catalog_path = os.path.join(output_dir, "master_catalog.json")
    
    with open(brands_path, "r", encoding="utf-8") as f:
        brands = json.load(f)
        
    with open(lab_results_path, "r", encoding="utf-8") as f:
        lab_results_list = json.load(f)
        
    lab_results = {item['product_id']: item for item in lab_results_list}

    master_catalog = []
    print("Executing Strict Zero-Fallback Scraper Protocol...")
    
    for brand in brands:
        brand_id = brand.get("brand_id")
        brand_name = brand.get("brand_name")
        
        for product in brand.get("products", []):
            product_id = product.get("product_id")
            
            live_price = get_live_price(brand_id, product.get("url"))
            print(f"Scraped {product_id}: Price={live_price}")
            
            product_lab_data = lab_results.get(product_id)
            
            catalog_entry = {
                "id": product_id,
                "brand": brand_name,
                "product_name": product.get("name"),
                "product_url": product.get("url"),
                "live_price_inr": live_price,
                "last_updated": datetime.datetime.now().isoformat()
            }
            
            metrics = calculate_quality_metrics(catalog_entry, product_lab_data)
            catalog_entry.update(metrics)
            
            if product_lab_data:
                catalog_entry["lab_details"] = product_lab_data
            
            master_catalog.append(catalog_entry)
            
    with open(master_catalog_path, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, indent=2)
        
    print(f"Successfully generated 100% transparent master_catalog.json with {len(master_catalog)} products.")

if __name__ == "__main__":
    main()

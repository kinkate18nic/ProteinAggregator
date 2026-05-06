#!/usr/bin/env python3
"""
Catalog Verification Script
Re-scrapes a sample of products from each brand and compares
stored catalog data against live website data.
"""

import json
import sys
import os

# Add scraper directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scraper'))

from main import scrape_product, BRAND_SCRAPERS

def load_catalog():
    catalog_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'master_catalog.json')
    with open(catalog_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def verify_products():
    catalog = load_catalog()
    
    # Group by brand
    by_brand = {}
    for product in catalog:
        brand = product['brand']
        if brand not in by_brand:
            by_brand[brand] = []
        by_brand[brand].append(product)
    
    # Pick 2 samples per brand (first and last for variety)
    samples = []
    for brand, products in by_brand.items():
        samples.append(products[0])  # First product
        if len(products) > 1:
            samples.append(products[-1])  # Last product
    
    print(f"Verification Report")
    print(f"=" * 80)
    print(f"Catalog last updated: {max(p['last_updated'] for p in catalog)}")
    print(f"Total products in catalog: {len(catalog)}")
    print(f"Products to verify: {len(samples)} (sample from each brand)")
    print(f"=" * 80)
    print()
    
    discrepancies = []
    errors = []
    
    for product in samples:
        brand_id = product['brand'].lower().replace(' ', '').replace("'", "")
        product_id = product['id']
        url = product['product_url']
        stored_price = product.get('live_price_inr')
        stored_stock = product.get('in_stock')
        stored_name = product.get('product_name')
        
        print(f"\n{'-' * 80}")
        print(f"Brand: {product['brand']}")
        print(f"Product: {stored_name}")
        print(f"URL: {url}")
        print(f"Stored:  Price=Rs.{stored_price}, InStock={stored_stock}")
        
        try:
            # Determine correct scraper
            scraper_name = None
            for bid, func in BRAND_SCRAPERS.items():
                if bid in brand_id or brand_id in bid:
                    scraper_name = bid
                    break
            
            if not scraper_name:
                print(f"  [!] No scraper found for brand '{product['brand']}', trying generic...")
                scraper_name = 'generic'
            
            live = scrape_product(scraper_name, url)
            
            live_price = live.get('price')
            live_stock = live.get('in_stock')
            live_name = live.get('scraped_name')
            
            print(f"Live:    Price=Rs.{live_price}, InStock={live_stock}")
            
            # Compare
            issues = []
            
            if stored_price != live_price:
                if live_price is not None:
                    diff = live_price - (stored_price or 0)
                    pct = (diff / stored_price * 100) if stored_price else 0
                    issues.append(f"PRICE CHANGED: Rs.{stored_price} -> Rs.{live_price} (diff: Rs.{diff:+.0f}, {pct:+.1f}%)")
                else:
                    issues.append(f"PRICE LOST: was Rs.{stored_price}, now None")
            
            if stored_stock != live_stock:
                issues.append(f"STOCK CHANGED: {stored_stock} -> {live_stock}")
            
            if issues:
                print(f"  [X] DISCREPANCIES FOUND:")
                for issue in issues:
                    print(f"      - {issue}")
                discrepancies.append({
                    'product': product,
                    'live': live,
                    'issues': issues
                })
            else:
                print(f"  [OK] MATCHES - data is current")
                
        except Exception as e:
            print(f"  [ERR] ERROR during verification: {e}")
            errors.append({'product': product, 'error': str(e)})
    
    # Summary
    print(f"\n{'=' * 80}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'=' * 80}")
    print(f"Products checked: {len(samples)}")
    print(f"Discrepancies: {len(discrepancies)}")
    print(f"Errors: {len(errors)}")
    
    if discrepancies:
        print(f"\n[!] DISCREPANCIES DETAIL:")
        for d in discrepancies:
            print(f"\n  [{d['product']['brand']}] {d['product']['product_name']}")
            for issue in d['issues']:
                print(f"    - {issue}")
    
    if errors:
        print(f"\n[X] ERRORS:")
        for e in errors:
            print(f"  - {e['product']['product_name']}: {e['error']}")
    
    if not discrepancies and not errors:
        print(f"\n[OK] ALL SAMPLED PRODUCTS ARE UP TO DATE!")
    
    print(f"\nNote: This checks a sample only. Run the full scraper (python scraper/main.py) to update all products.")
    
    return discrepancies, errors

if __name__ == "__main__":
    verify_products()

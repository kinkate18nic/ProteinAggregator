import json
import datetime
import os
import requests
import re
from bs4 import BeautifulSoup

# =============================================================================
# BRAND-SPECIFIC SCRAPERS
# =============================================================================

def scrape_healthkart(product_url):
    """
    HealthKart platform scraper (works for MuscleBlaze, TrueBasics, etc.).
    Extracts ALL data from the __NEXT_DATA__ JSON payload embedded in each product page.
    
    Returns dict with:
      - price: float or None
      - protein_per_serving_g: float or None (e.g., 25.0)
      - serving_size_g: float or None (e.g., 36.0)
      - protein_percent: float or None (e.g., 69.0)
      - num_servings: int or None
      - in_stock: bool
      - total_weight_g: float or None (computed from serving_size * num_servings)
    """
    result = {
        "price": None,
        "protein_per_serving_g": None,
        "serving_size_g": None,
        "protein_percent": None,
        "num_servings": None,
        "in_stock": None,
        "total_weight_g": None,
        "scraped_name": None,
    }
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'}
        r = requests.get(product_url, headers=headers, timeout=15)
        if r.status_code != 200:
            return result
            
        soup = BeautifulSoup(r.text, 'html.parser')
        next_data_tag = soup.find('script', id='__NEXT_DATA__')
        if not next_data_tag or not next_data_tag.string:
            return result
            
        data = json.loads(next_data_tag.string)
        results = data.get('props', {}).get('pageProps', {}).get('data', {}).get('results', {})
        if not results:
            return result
        
        # --- CHECK IF THIS IS A COMBO PACK (/pk/ URL) ---
        is_combo = '/pk/' in product_url
        if is_combo:
            packs = results.get('packs', {})
            if isinstance(packs, dict):
                result['price'] = float(packs['offer_pr']) if packs.get('offer_pr') else None
                result['in_stock'] = not packs.get('oos', True)
                result['scraped_name'] = packs.get('nm', '').strip() if packs.get('nm') else None
            return result
        
        # --- PRICE ---
        hk_pricing = results.get('hkUserLoyaltyPricingDto') or {}
        result['price'] = float(hk_pricing.get('hkNormalOfferPrice', 0)) or None
        if result['price'] is None:
            offer_pr = results.get('offer_pr')
            if offer_pr:
                result['price'] = float(offer_pr)
        
        # --- STOCK STATUS ---
        result['in_stock'] = not results.get('oos', True)
        
        # --- NUTRITIONAL DATA from nut_info_grp ---
        nut_info = results.get('nut_info_grp', [])
        for item in nut_info:
            nm = (item.get('nm') or item.get('dis_nm') or '').lower()
            val_str = item.get('val', '')
            if 'protein' in nm and val_str:
                num = re.search(r'([\d.]+)', val_str)
                if num:
                    result['protein_per_serving_g'] = float(num.group(1))
        
        # --- VARIANT ATTRIBUTES (Protein %, Serving Size, Number of Servings) ---
        # These are inside each variant's 'hghAttr' within 'availVar', NOT the top-level 'attr'.
        avail_var = results.get('availVar', {})
        selected_variant = None
        
        # Strategy 1: Match by navKey from URL (e.g., ?navKey=VRNT-165145 → sv_id=165145)
        nav_match = re.search(r'navKey=VRNT-(\d+)', product_url)
        if nav_match:
            target_sv_id = int(nav_match.group(1))
            for var_key, var_data in avail_var.items():
                if isinstance(var_data, dict) and var_data.get('sv_id') == target_sv_id:
                    selected_variant = var_data
                    break
        
        # Strategy 2: Find the variant marked as 'selected' by MuscleBlaze
        if not selected_variant:
            for var_key, var_data in avail_var.items():
                if isinstance(var_data, dict) and var_data.get('selected'):
                    selected_variant = var_data
                    break
        
        # Strategy 3: Fall back to the page-level default variant (navKey in results)
        if not selected_variant:
            page_nav = results.get('navKey', '')
            if page_nav:
                nav_id = re.search(r'VRNT-(\d+)', str(page_nav))
                if nav_id:
                    target_id = int(nav_id.group(1))
                    for var_key, var_data in avail_var.items():
                        if isinstance(var_data, dict) and var_data.get('sv_id') == target_id:
                            selected_variant = var_data
                            break
        
        # Strategy 4: Last resort - first variant in dict
        if not selected_variant and avail_var:
            selected_variant = next(iter(avail_var.values()))
        
        if selected_variant and isinstance(selected_variant, dict):
            # Read hghAttr from the variant
            hgh_attrs = selected_variant.get('hghAttr', [])
            for attr_item in hgh_attrs:
                if not isinstance(attr_item, dict):
                    continue
                dis_nm = (attr_item.get('dis_nm') or '').lower()
                # Values is a list of dicts with 'val' key
                values = attr_item.get('values', [])
                val_str = values[0].get('val', '') if values else ''
                _parse_mb_attr(dis_nm, val_str, result)
            
            # Also read price and stock from this specific variant if available
            var_pricing = selected_variant.get('hkUserLoyaltyPricingDto') or {}
            if var_pricing.get('hkNormalOfferPrice'):
                result['price'] = float(var_pricing['hkNormalOfferPrice'])
            elif selected_variant.get('offer_pr'):
                result['price'] = float(selected_variant['offer_pr'])
            
            result['in_stock'] = not selected_variant.get('oos', True)
            
            # Read the variant's actual full name (includes weight + flavor)
            if selected_variant.get('fullName'):
                result['scraped_name'] = selected_variant['fullName'].strip()
        
        # --- COMPUTE TOTAL WEIGHT ---
        if result['serving_size_g'] and result['num_servings']:
            result['total_weight_g'] = round(result['serving_size_g'] * result['num_servings'], 1)
        
        # Fallback: parse weight from variant's fullName (e.g., "2.2 lb", "1 kg")
        if not result['total_weight_g'] and result.get('scraped_name'):
            name_lower = result['scraped_name'].lower()
            kg_m = re.search(r'([\d.]+)\s*kg', name_lower)
            lb_m = re.search(r'([\d.]+)\s*lb', name_lower)
            g_m = re.search(r'([\d.]+)\s*g\b', name_lower)
            if kg_m:
                result['total_weight_g'] = round(float(kg_m.group(1)) * 1000, 1)
            elif lb_m:
                result['total_weight_g'] = round(float(lb_m.group(1)) * 453.592, 1)
            elif g_m:
                result['total_weight_g'] = float(g_m.group(1))
        
        # --- COMPUTE PROTEIN % from protein_per_serving / serving_size if missing ---
        if not result['protein_percent'] and result['protein_per_serving_g'] and result['serving_size_g']:
            result['protein_percent'] = round((result['protein_per_serving_g'] / result['serving_size_g']) * 100, 1)
        
        # --- CONVERT lb-BASED NAMES TO kg FOR INDIAN DISPLAY ---
        if result.get('scraped_name'):
            name = result['scraped_name']
            def lb_to_kg_replace(m):
                lb_val = float(m.group(1))
                kg_val = round(lb_val * 0.453592, 2)
                # Clean up trailing zeros: 1.0 → 1, 0.5 → 0.5
                kg_str = f"{kg_val:g}"
                return f"{kg_str} kg"
            result['scraped_name'] = re.sub(r'(\d+\.?\d*)\s*lb\b', lb_to_kg_replace, name, flags=re.IGNORECASE)
        
    except Exception as e:
        print(f"  [MB Scraper Error] {product_url}: {e}")
    
    return result


def _parse_mb_attr(dis_nm, val_str, result):
    """Helper to parse MuscleBlaze attribute key-value pairs."""
    if not val_str:
        return
    num = re.search(r'([\d.]+)', str(val_str))
    if not num:
        return
    
    val = float(num.group(1))
    
    if 'protein %' in dis_nm or 'protein percent' in dis_nm:
        result['protein_percent'] = val
    elif 'serving size' in dis_nm:
        result['serving_size_g'] = val
    elif 'number of serving' in dis_nm:
        result['num_servings'] = int(val)


# =============================================================================
# GENERIC FALLBACK SCRAPER (for brands not yet implemented)
# =============================================================================

def scrape_generic(product_url):
    """Generic scraper that only extracts price from DOM text."""
    result = {
        "price": None,
        "protein_per_serving_g": None,
        "serving_size_g": None,
        "protein_percent": None,
        "num_servings": None,
        "in_stock": None,
        "total_weight_g": None,
    }
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'}
        r = requests.get(product_url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text(separator=' ')
            matches = re.findall(r'₹\s*([\d,]+)', text)
            if matches:
                prices = [int(m.replace(',', '')) for m in matches if int(m.replace(',', '')) > 100]
                if prices:
                    result['price'] = float(prices[0])
    except Exception:
        pass
    return result


# =============================================================================
# SHOPIFY SCRAPER (bgreen, etc.)
# =============================================================================

def scrape_shopify(product_url):
    """
    Shopify-based D2C brand scraper.
    Uses the public /products/{handle}.json endpoint.
    
    URL format: https://domain.com/products/{handle}?variant={variant_id}
    """
    result = {k: None for k in [
        'scraped_name', 'price', 'in_stock', 'protein_percent',
        'protein_per_serving_g', 'serving_size_g', 'num_servings', 'total_weight_g'
    ]}
    
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(product_url)
        params = parse_qs(parsed.query)
        variant_id = int(params.get('variant', [0])[0])
        
        # Build JSON API URL: /products/{handle}.json
        path_parts = parsed.path.strip('/').split('/')
        handle = path_parts[-1] if path_parts else ''
        json_url = f"{parsed.scheme}://{parsed.netloc}/products/{handle}.json"
        
        resp = requests.get(json_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if resp.status_code != 200:
            print(f"  [Shopify Error] {json_url}: HTTP {resp.status_code}")
            return result
        
        data = resp.json()
        product = data.get('product', {})
        variants = product.get('variants', [])
        
        # Find the target variant
        selected = None
        for v in variants:
            if v.get('id') == variant_id:
                selected = v
                break
        if not selected and variants:
            selected = variants[0]
        
        if not selected:
            return result
        
        # Extract data
        result['scraped_name'] = f"{product.get('title', '')}, {selected.get('title', '')}"
        result['price'] = float(selected.get('price', 0)) or None
        # Shopify .json API doesn't reliably expose stock; assume in-stock
        # (out-of-stock variants are typically removed from the product page)
        result['in_stock'] = True
        result['total_weight_g'] = float(selected.get('grams', 0)) or None
        
        # Nutritional data not available in Shopify product JSON
        # Will be filled by nutrition_overrides.json
        
    except Exception as e:
        print(f"  [Shopify Error] {product_url}: {e}")
    
    return result


# =============================================================================
# PLIXLIFE SCRAPER
# =============================================================================

def scrape_plix(product_url):
    """
    Scraper for PlixLife, which uses Next.js with a deeply nested variant structure.
    Target variant should be specified via '?sku=' in the URL.
    """
    result = {k: None for k in [
        'scraped_name', 'price', 'in_stock', 'protein_percent',
        'protein_per_serving_g', 'serving_size_g', 'num_servings', 'total_weight_g'
    ]}
    
    try:
        from urllib.parse import urlparse, parse_qs
        import re
        
        parsed_url = urlparse(product_url)
        qs = parse_qs(parsed_url.query)
        target_sku = qs.get('sku', [None])[0]
        
        # Clean URL for request
        clean_url = product_url.split('?')[0]
        resp = requests.get(clean_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if resp.status_code != 200:
            print(f"  [Plix Error] {product_url}: HTTP {resp.status_code}")
            return result
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        nd = soup.find('script', id='__NEXT_DATA__')
        if not nd:
            print(f"  [Plix Error] {product_url}: No __NEXT_DATA__ found")
            return result
            
        data = json.loads(nd.string)
        product = data.get('props', {}).get('pageProps', {}).get('productPageData', {}).get('product', {})
        if not product:
            print(f"  [Plix Error] {product_url}: Product block not found in NEXT_DATA")
            return result
        
        parent_name = (product.get('name') or '').strip()
        variants = product.get('variants', [])
        
        # Find matching variant
        target_variant = None
        if target_sku:
            for v in variants:
                if v.get('sku') == target_sku:
                    target_variant = v
                    break
        
        if not target_variant and variants:
            target_variant = variants[0]
            
        if target_variant:
            # --- Build a clean product name ---
            # Variant name looks like "Milk Chocolate / Pack of 1Kg__1 Month__27 Scoops"
            raw_variant = target_variant.get('name') or ''
            # Extract flavor (before ' / ')
            flavor = raw_variant.split(' / ')[0].strip() if ' / ' in raw_variant else ''
            # Extract weight text (e.g. "Pack of 1Kg", "Pack of 500g")
            wt_part = ''
            wt_match = re.search(r'Pack\s+of\s+(\d+(?:\.\d+)?)\s*(kg|Kg|KG|g|gm|gms)\b', raw_variant)
            if wt_match:
                wt_part = f"{wt_match.group(1)}{wt_match.group(2).lower()}"
            
            # Compose: "Parent Name, Weight / Flavor"
            name_parts = [parent_name]
            if wt_part:
                name_parts.append(wt_part)
            if flavor:
                name_parts.append(flavor)
            result['scraped_name'] = ', '.join(name_parts)
            
            # --- Price ---
            try:
                result['price'] = float(target_variant.get('pricing', {}).get('price', {}).get('gross', {}).get('amount'))
            except (ValueError, TypeError):
                pass
                
            # --- Stock ---
            qty = target_variant.get('quantityAvailable', 0)
            result['in_stock'] = qty > 0
            
            # --- Weight ---
            if wt_match:
                val = float(wt_match.group(1))
                unit = wt_match.group(2).lower()
                if unit == 'kg':
                    result['total_weight_g'] = val * 1000
                else:
                    result['total_weight_g'] = val
            
            # --- Servings from variant name ("27 Scoops") ---
            scoops_match = re.search(r'(\d+)\s*Scoops', raw_variant, re.IGNORECASE)
            if scoops_match:
                result['num_servings'] = int(scoops_match.group(1))
                    
    except Exception as e:
        print(f"  [Plix Error] {product_url}: {e}")
        
    return result


# =============================================================================
# JSON-LD SCRAPER (onlywhatsneeded, etc.)
# =============================================================================

def scrape_jsonld(product_url):
    """
    Generic scraper for sites that expose product data via JSON-LD
    (schema.org Product type with Offer).
    Also checks meta tags as fallback for price.
    """
    result = {k: None for k in [
        'scraped_name', 'price', 'in_stock', 'protein_percent',
        'protein_per_serving_g', 'serving_size_g', 'num_servings', 'total_weight_g'
    ]}
    
    try:
        resp = requests.get(product_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if resp.status_code != 200:
            print(f"  [JSONLD Error] {product_url}: HTTP {resp.status_code}")
            return result
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract from JSON-LD
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                ld = json.loads(script.string)
                if isinstance(ld, dict) and 'offers' in ld:
                    result['scraped_name'] = ld.get('name')
                    offers = ld['offers']
                    if isinstance(offers, dict):
                        result['price'] = float(offers.get('price', 0)) or None
                        avail = offers.get('availability', '')
                        result['in_stock'] = 'InStock' in avail
                    elif isinstance(offers, list) and offers:
                        result['price'] = float(offers[0].get('price', 0)) or None
                        avail = offers[0].get('availability', '')
                        result['in_stock'] = 'InStock' in avail
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Fallback: meta tags for price
        if result['price'] is None:
            meta_price = soup.find('meta', property='product:price:amount')
            if meta_price and meta_price.get('content'):
                try:
                    result['price'] = float(meta_price['content'])
                except ValueError:
                    pass
        
        # Extract weight from URL first (more reliable), then product name
        import re
        # Search URL first, then product name
        for text in [product_url, result['scraped_name'] or '']:
            wt_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|Kg|KG)\b', text)
            if wt_match:
                result['total_weight_g'] = float(wt_match.group(1)) * 1000
                break
            # For grams, only match pack sizes (≥100g) to avoid "24g protein"
            wt_match = re.search(r'(\d{3,})\s*(?:g|gm|gms|G)\b', text)
            if wt_match:
                result['total_weight_g'] = float(wt_match.group(1))
                break
        
    except Exception as e:
        print(f"  [JSONLD Error] {product_url}: {e}")
    
    return result


# =============================================================================
# SCRAPER ROUTER
# =============================================================================

BRAND_SCRAPERS = {
    "muscleblaze": scrape_healthkart,
    "truebasics": scrape_healthkart,
    "bgreen": scrape_shopify,
    "onlywhatsneeded": scrape_jsonld,
    "plixlife": scrape_plix,
}


def scrape_product(brand_id, product_url):
    """Route to the correct brand-specific scraper."""
    scraper = BRAND_SCRAPERS.get(brand_id, scrape_generic)
    return scraper(product_url)


# =============================================================================
# METRIC CALCULATION (ZERO FALLBACK)
# =============================================================================

def calculate_metrics(scraped_data, lab_data):
    """
    Calculate cost-per-gram metrics using ONLY real scraped data.
    
    Shows TWO cost-per-gram values:
      1. cost_per_gram_claimed: based on brand's own label claim (always from scraper)
      2. cost_per_gram_verified: based on independent lab test (only if lab data exists)
    """
    metrics = {
        "live_price_inr": scraped_data['price'],
        "in_stock": scraped_data['in_stock'],
        "protein_per_serving_g": scraped_data['protein_per_serving_g'],
        "serving_size_g": scraped_data['serving_size_g'],
        "protein_claimed_percent": scraped_data['protein_percent'],
        "num_servings": scraped_data['num_servings'],
        "total_weight_g": scraped_data['total_weight_g'],
        "cost_per_gram_claimed": None,
        "cost_per_gram_verified": None,
        "is_lab_tested": False,
        "protein_verified_percent": None,
    }
    
    price = scraped_data['price']
    claimed_pct = scraped_data['protein_percent']
    total_weight = scraped_data['total_weight_g']
    
    # Cost per gram based on CLAIMED protein %
    if price and claimed_pct and total_weight:
        total_claimed_protein = total_weight * (claimed_pct / 100)
        if total_claimed_protein > 0:
            metrics['cost_per_gram_claimed'] = round(price / total_claimed_protein, 2)
    
    # Cost per gram based on LAB VERIFIED protein %
    if lab_data and lab_data.get('is_tested') and lab_data.get('protein_verified_percent'):
        metrics['is_lab_tested'] = True
        verified_pct = lab_data['protein_verified_percent']
        metrics['protein_verified_percent'] = verified_pct
        
        if price and total_weight:
            total_verified_protein = total_weight * (verified_pct / 100)
            if total_verified_protein > 0:
                metrics['cost_per_gram_verified'] = round(price / total_verified_protein, 2)
    
    return metrics


# =============================================================================
# MAIN
# =============================================================================

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

    # Load nutrition overrides (static, one-time extracted data from label images)
    overrides_path = os.path.join(script_dir, "data", "nutrition_overrides.json")
    nutrition_overrides = {}
    if os.path.exists(overrides_path):
        with open(overrides_path, "r", encoding="utf-8") as f:
            raw_overrides = json.load(f)
            # Filter out comment keys
            nutrition_overrides = {k: v for k, v in raw_overrides.items() if not k.startswith('_')}

    master_catalog = []
    
    for brand in brands:
        brand_id = brand['brand_id']
        brand_name = brand['brand_name']
        
        for product in brand.get('products', []):
            product_id = product['product_id']
            product_url = product['url']
            
            print(f"Scraping: {brand_name} > {product['name']}")
            scraped = scrape_product(brand_id, product_url)
            
            # Apply nutrition overrides for missing fields
            if product_id in nutrition_overrides:
                ovr = nutrition_overrides[product_id]
                # protein_percent_override forces correction (e.g., TB Raw Whey 229% → 80%)
                # When override is present, force-apply ALL override fields since scraped data is wrong
                if 'protein_percent_override' in ovr:
                    scraped['protein_percent'] = ovr['protein_percent_override']
                    if 'serving_size_g' in ovr:
                        scraped['serving_size_g'] = ovr['serving_size_g']
                    if 'protein_per_serving_g' in ovr:
                        scraped['protein_per_serving_g'] = ovr['protein_per_serving_g']
                else:
                    # Normal fallback: only fill in missing fields
                    if scraped['serving_size_g'] is None and 'serving_size_g' in ovr:
                        scraped['serving_size_g'] = ovr['serving_size_g']
                    if scraped['protein_per_serving_g'] is None and 'protein_per_serving_g' in ovr:
                        scraped['protein_per_serving_g'] = ovr['protein_per_serving_g']
                # Recompute total_weight if we now have serving data
                if scraped['total_weight_g'] is None and scraped['serving_size_g'] and scraped['num_servings']:
                    scraped['total_weight_g'] = round(scraped['serving_size_g'] * scraped['num_servings'], 1)
                # Recompute num_servings if we have total_weight and serving_size
                if scraped['num_servings'] is None and scraped['total_weight_g'] and scraped['serving_size_g']:
                    scraped['num_servings'] = int(scraped['total_weight_g'] / scraped['serving_size_g'])
                # Recompute protein_percent if we now have protein_per_serving and serving_size
                if scraped['protein_percent'] is None and scraped['protein_per_serving_g'] and scraped['serving_size_g']:
                    scraped['protein_percent'] = round((scraped['protein_per_serving_g'] / scraped['serving_size_g']) * 100, 1)
            
            lab_data = lab_results.get(product_id)
            metrics = calculate_metrics(scraped, lab_data)
            
            # Use scraped name if available, otherwise fall back to our static name
            display_name = scraped.get('scraped_name') or product['name']
            
            catalog_entry = {
                "id": product_id,
                "brand": brand_name,
                "product_name": display_name,
                "product_url": product_url,
                "last_updated": datetime.datetime.now().isoformat(),
                **metrics,
            }
            
            if lab_data:
                catalog_entry["lab_details"] = lab_data
            
            # Log what we got
            p = metrics['live_price_inr']
            c = metrics['protein_claimed_percent']
            s = metrics['in_stock']
            cpg = metrics['cost_per_gram_claimed']
            print(f"  -> Price=₹{p}, Protein%={c}, InStock={s}, ₹/g(claimed)={cpg}")
            
            master_catalog.append(catalog_entry)
    
    with open(master_catalog_path, "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, indent=2)
    
    print(f"\nGenerated master_catalog.json with {len(master_catalog)} products.")

if __name__ == "__main__":
    main()

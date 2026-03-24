import requests, json
from bs4 import BeautifulSoup

urls = [
    ("VRNT-266871", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate-plus-concentrate/SP-135011?navKey=VRNT-266871"),
    ("VRNT-274397", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate/SP-135063?navKey=VRNT-274397"),
    ("VRNT-272429", "https://www.truebasics.com/sv/truebasics-clean-plant-protein/SP-136871?navKey=VRNT-272429"),
    ("VRNT-271469", "https://www.truebasics.com/sv/truebasics-clean-raw-whey-concentrate/SP-136503?navKey=VRNT-271469"),
    ("VRNT-274779", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate-plus-concentrate/SP-135011?navKey=VRNT-274779"),
    ("VRNT-279151", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate/SP-135063?navKey=VRNT-279151"),
    ("VRNT-267055", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate/SP-135063?navKey=VRNT-267055"),
    ("VRNT-277507", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate-plus-concentrate/SP-135011?navKey=VRNT-277507"),
    ("VRNT-277575", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate-plus-concentrate/SP-135011?navKey=VRNT-277575"),
    ("VRNT-281081", "https://www.truebasics.com/sv/truebasics-clean-raw-whey-isolate/SP-139677?navKey=VRNT-281081"),
    ("VRNT-273053", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate/SP-135063?navKey=VRNT-273053"),
    ("VRNT-279771", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate-plus-concentrate/SP-135011?navKey=VRNT-279771"),
    ("VRNT-268555", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate-plus-concentrate/SP-135011?navKey=VRNT-268555"),
    ("VRNT-277577", "https://www.truebasics.com/sv/truebasics-clean-whey-protein-isolate/SP-135063?navKey=VRNT-277577"),
]

# Group by base product page to avoid fetching the same page multiple times
pages = {}
for nav_key, url in urls:
    base_url = url.split('?')[0]
    if base_url not in pages:
        pages[base_url] = []
    sv_id = int(nav_key.replace('VRNT-', ''))
    pages[base_url].append((sv_id, url))

for base_url, variants in pages.items():
    print(f"\nFetching: {base_url}")
    r = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'html.parser')
    nd = soup.find('script', id='__NEXT_DATA__')
    data = json.loads(nd.string)
    res = data['props']['pageProps']['data']['results']
    av = res.get('availVar', {})
    
    for sv_id, full_url in variants:
        found = False
        for k, v in av.items():
            if isinstance(v, dict) and v.get('sv_id') == sv_id:
                name = v.get('fullName', '?')
                oos = v.get('oos', '?')
                price = v.get('hkUserLoyaltyPricingDto', {}).get('hkNormalOfferPrice', v.get('offer_pr', '?'))
                hgh = v.get('hghAttr', [])
                prot = next((a['values'][0]['val'] for a in hgh if 'Protein %' in a.get('dis_nm', '')), 'N/A')
                print(f"  VRNT-{sv_id} | ₹{price} | prot={prot}% | oos={oos} | {name}")
                found = True
                break
        if not found:
            print(f"  VRNT-{sv_id} | NOT FOUND IN availVar!")

import requests, json, re
from bs4 import BeautifulSoup

# Check Mass Gainer for the embedded nutritional label image
url = 'https://www.muscleblaze.com/sv/muscleblaze-mass-gainer-xxl-with-complex-carbs-and-proteins-in-3:1-ratio/SP-33848?navKey=VRNT-72272'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
nd = soup.find('script', id='__NEXT_DATA__')
data = json.loads(nd.string)
res = data['props']['pageProps']['data']['results']
page = res.get('page', {})

sections = page.get('pgSections', [])

print("=== EXTRACTING ALL scContent ITEMS ===")
for i, sec in enumerate(sections):
    sc_content = sec.get('scContent', [])
    for j, item in enumerate(sc_content):
        dis_nm = item.get('dis_nm', '?')
        print(f"\nSection {i}, Item {j}: '{dis_nm}'")
        attrs = item.get('attributeArea', [])
        for attr in attrs:
            name = attr.get('name', '?')
            atype = attr.get('type', '?')
            value = attr.get('value', '')
            print(f"  Attr: name={name}, type={atype}, value_len={len(str(value))}")
            
            # If it's HTML content, extract image URLs
            if isinstance(value, str) and '<img' in value:
                img_soup = BeautifulSoup(value, 'html.parser')
                imgs = img_soup.find_all('img')
                for img in imgs:
                    src = img.get('src', '')
                    alt = img.get('alt', '')
                    print(f"    IMG: alt='{alt[:60]}' src={src[:120]}")
            
            # If it's HTML with tables, extract table data
            if isinstance(value, str) and '<table' in value.lower():
                tbl_soup = BeautifulSoup(value, 'html.parser')
                tables = tbl_soup.find_all('table')
                for t in tables:
                    rows = t.find_all('tr')
                    print(f"    TABLE ({len(rows)} rows):")
                    for row in rows[:10]:
                        cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                        print(f"      {cells}")

import json
d = json.load(open('public/master_catalog.json'))
for p in d:
    pid = p['id']
    if pid.startswith('tb-') or 'biz' in pid:
        prot = p['protein_claimed_percent']
        serv = p['serving_size_g']
        pps = p['protein_per_serving_g']  
        cpg = p['cost_per_gram_claimed']
        print(f"{pid:30s} | prot%={prot:>6} | serv={serv} | ppserv={pps} | cpg={cpg}")

r = [{'ps_oid': '1221', 'oid': '38', 'name': 'Cygate'}, {'ps_oid': '1222', 'oid': '41', 'name': 'default'}, {'ps_oid': 'None', 'oid': '880423', 'name': 'Public Cloud'}, {'ps_oid': 'None', 'oid': '923530', 'name': 'VMware'}, {'ps_oid': 'None', 'oid': '4672177', 'name': 'Centreon'}, {'ps_oid': 'None', 'oid': '4672257', 'name': 'Doro'}]


for i, k in enumerate(r):
    parent_oid = k['ps_oid']
    if parent_oid == 'None':
        break
    else:
        parent = r[i]['oid']


for i, k in enumerate(r):
    parent_oid = k['ps_oid']
    if parent_oid != 'None':
        continue
    else:
        child = r[i]['oid']
        break

print parent, child
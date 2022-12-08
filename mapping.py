import siptracklib
try:
    st = siptracklib.connect('siptrack.test.se', 'itek', '######', '9244', use_ssl=False)
except Exception as e:
    print "connection failed"

password = st.getOID("2905157")
print password.key.attributes.get('name').encode('utf-8', 'ignore')
353818

353818
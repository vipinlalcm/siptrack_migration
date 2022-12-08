import siptracklib
# from siptrack_migration.siptrack_migration import api
# from api import models as api_models
# password_parent = api_models.PasswordParentDetails.objects.filter(st_oid_id=21655)

try:
    st = siptracklib.connect('st.test', 'vipicm', '#####8', '9242', use_ssl=False)
except Exception as e:
    print "connection failed"
view = st.getOID('38')
um = st.getOID('300110')
user_manager = um.parent.user_manager


tree = view.getChildByName('default', include=['password tree'])
for i in tree.parent.listChildren(include=['password key']):
    # Enumerate list of users connected to the key
    # passwordkey = i.attributes.get('name').encode('utf-8')
    print "{},{}".format(i.attributes.get('name').encode('utf-8').strip(),i.oid)
    # for users in user_manager.listChildren():
    #     try:
    #         username = users.username
    #         for subkey in users.listChildren(include=['sub key']):
    #             if subkey.password_key is i:
    #                 print "{},{}".format(passwordkey,username)
    #     except Exception as e:
    #         continue
st.logout()

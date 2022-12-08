import siptracklib
from siptrack_migration.siptrack_migration import api
from api import models as api_models
password_parent = api_models.PasswordParentDetails.objects.filter(st_oid_id=21655)

try:
    st = siptracklib.connect('siptrack.test.se', 'vipicm', '####', '9244', use_ssl=False)
except Exception as e:
    print "connection failed"
for parent in password_parent:
    device_object = st.getOID(parent.st_oid)
    while True:
        oid = str(device_object.oid)

        if oid:
            st_name = device_object.attributes.get('name').encode('utf-8', 'ignore') if \
                device_object.attributes.get('name') else 'Unknown'
            if device_object.attributes.get('disabled'):
                dev_status = 1
            else:
                dev_status = 0
            st_class_id = device_object.class_id
            device_object = device_object.parent
            print st_name, "", device_object.oid
            try:
                idmap_obj, idmap_created = api_models.Idmap.objects.get_or_create(st_oid=oid,
                                                                                  st_parent_oid=device_object.oid)
                detail_obj, detail_created = api_models.ParentDetails.objects.get_or_create(st_oid=idmap_obj,
                                                                                            st_name=st_name,
                                                                                            st_status=dev_status,
                                                                                            st_class_id=st_class_id)

                try:
                    oid = device_object.parent.oid
                except AttributeError:
                    break
            except Exception as e:
                print e
st.logout()

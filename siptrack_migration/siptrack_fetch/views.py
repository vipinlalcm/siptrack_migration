#!/usr/bin/env python
import siptracklib
from siptrack_fetch import models as st_models
from api import models as api_models


def find_tree(device_object):
    tree_list = []
    while True:
        tree_dict = dict()
        oid = str(device_object.oid)
        tree_dict["name"] = str(device_object.attributes.get('name').encode('utf8', 'ignore') \
                                if device_object.attributes.get('name') else 'UNKNOWN')
        tree_dict["oid"] = oid
        if oid:
            device_object = device_object.parent
            try:
                oid = device_object.parent.oid
            except AttributeError:
                break
        tree_list.append(tree_dict)
    return tree_list


def fetch(device_oid):
    try:
        st = siptracklib.connect('st.test', 'vipicm', '#####8', '9244', use_ssl=False)
        # for i in st.quicksearch('*', include=['device']):
        device_object = st.getOID(device_oid)
        if device_object.class_name == 'device':
            if not device_object.attributes.get('disabled'):
                device_l = []
                device_name = str(device_object.attributes.get('name'))
                device = dict()
                device[device_name] = dict()
                device[device_name]["credentials"] = dict()
                device[device_name]["device_path"] = dict()
                cred_l = []
                for p in device_object.listChildren(include=['password']):
                    if p.class_name == 'password':
                        cred = dict()
                        cred["username"] = str(p.attributes.get('username'))
                        cred["password"] = str(p.password)
                        cred["password_key"] = str(p.key.attributes.get('name')) if p.key else None
                        cred_l.append(cred)
                device[device_name]["credentials"] = cred_l
                device[device_name]["device_path"] = find_tree(device_object)
                device_l.append(device)
                return device_l
    except Exception as e:
        print e
    finally:
        st.logout()


def fetchall():
    try:
        st = siptracklib.connect('127.0.0.1', 'admin', 'admin', '9244', use_ssl=False)
        device_l = []
        for i in st.quicksearch('*', include=['device']):
            if i.class_name == 'device':
                if not i.attributes.get('disabled'):
                    device_name = str(i.attributes.get('name'))
                    device = dict()
                    device[device_name] = dict()
                    device[device_name]["credentials"] = dict()
                    device[device_name]["device_path"] = dict()
                    cred_l = []
                    for p in i.listChildren(include=['password']):
                        if p.class_name == 'password':
                            cred = dict()
                            cred["username"] = str(p.attributes.get('username'))
                            cred["password"] = str(p.password)
                            cred["password_key"] = str(p.key.attributes.get('name')) if p.key else None
                            cred_l.append(cred)
                    device[device_name]["credentials"] = cred_l
                    device[device_name]["device_path"] = find_tree(i)
                    device_l.append(device)
        return device_l
    except Exception as e:
        print e
    finally:
        st.logout()


def fetch_paswords():
    try:
        st = siptracklib.connect('st.test', 'vipicm', '#####8', '9244', use_ssl=False)
    except Exception as e:
        print "connection failed"
        return False
    idmap_list = []
    st_idmap = st_models.Idmap.objects.filter(class_id='P')
    local_idmap = api_models.PasswordIdmap.objects.all()
    st_idmap_list = []
    local_idmap_list = []
    for i in st_idmap:
        st_idmap_list.append(i.oid)
    for y in local_idmap:
        local_idmap_list.append(y.st_oid)
    set_st_idmap = set(st_idmap_list)
    set_local_idmap = set(local_idmap_list)
    diff = set_st_idmap.symmetric_difference(set_local_idmap)
    if diff:
        for st_id in diff:
            try:
                st_oid = st.getOID(st_id)
            except Exception as e:
                print e
                continue
            if st_oid:
                password_key = st_oid.key
                if password_key:
                    key_oid = password_key.oid
                else:
                    key_oid = None
            else:
                continue
            try:
                st_obj = st_models.Idmap.objects.get(oid=st_id)
                if st_obj:
                    idmap_obj, created = api_models.PasswordIdmap.objects.get_or_create(st_oid=st_obj.oid,
                                                                                        st_parent_oid=st_obj.parent_oid,
                                                                                        st_key_id=key_oid,
                                                                                        st_class_id=st_obj.class_id)
                    if created:
                        idmap_list.append(idmap_obj.st_oid)
            except Exception as e:
                print e
                continue
    st.logout()
    return idmap_list


def add_data():
    try:
        st = siptracklib.connect('st.test', 'vipicm', '#####8', '9244', use_ssl=False)
    except Exception as e:
        print "connection failed"
        return False
    password_idmaps = api_models.PasswordIdmap.objects.filter(local_status=0)
    if password_idmaps:
        for idmaps in password_idmaps:
            password_parent_oid = idmaps.st_parent_oid
            try:
                password_parent = api_models.PasswordParentDetails.objects.filter(st_oid=password_parent_oid)
                if password_parent:
                    idmaps.local_status = 1
                    idmaps.save()
                else:
                    try:
                        parent_oid = st.getOID(idmaps.st_parent_oid)
                    except Exception as e:
                        print e
                        continue

                    if parent_oid:
                        if parent_oid.attributes.get('name'):
                            dev_name = str(parent_oid.attributes.get('name').encode('utf8', 'ignore'))
                            dev_class_id = parent_oid.class_id
                        else:
                            dev_name = 'unknown'
                            dev_class_id = parent_oid.class_id
                        if parent_oid.attributes.get('disabled'):
                            dev_status = 1
                        else:
                            dev_status = 0

                        try:
                            data_obj, created = api_models.PasswordParentDetails.objects.get_or_create(st_oid=password_parent_oid,
                                                                                                       st_name=dev_name,
                                                                                                       st_status=dev_status,
                                                                                                       st_class_id=dev_class_id)
                        except Exception as e:
                            print e
                            return False
                        idmaps.local_status = 1
                        idmaps.save()
            except Exception as e:
                print e
                return False
    st.logout()
    return True


def add_tree_details():
    try:
        st = siptracklib.connect('st.test', 'vipicm', '#####8', '9244', use_ssl=False)
    except Exception as e:
        print e
        return False

    password_parent = api_models.PasswordParentDetails.objects.filter(local_status=0)
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
                    return False
        parent.local_status = 1
        parent.save()
    st.logout()
    return True

if __name__ == '__main__':
    fetchall()
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import request
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
import urllib3
import certifi
import json
from api import models
import siptracklib
from django.db.models import Q

api_key = '3c2e56983bda47f9384af5672ced3bbc'
key_mapping = {'1290090': '54',
               '1293599': '123',
               '2069166': '29',
               '1288876': '27',
               '2078819': '60',
               '2079744': '109',
               '4877551': '74',
               '1293693': '131',
               '1926073': '52',
               '3594630': '106',
               '2073786': '31',
               '4524689': '113',
               '1293968': '133',
               '2079186': '102',
               '2082259': '128',
               '2079020': '91',
               '2230283': '130',
               '2082178': '43',
               '1359696': '51',
               '6964093': '138',
               '2078124': '56',
               '207662': '20',
               '1792418': '139',
               '4694460': '76',
               '2074941': '21',
               '4517333': '30',
               '2465436': '88',
               '2079037': '93',
               '4690997': '83',
               '1289442': '35',
               '4141791': '32',
               '3257364': '117',
               '1292480': '104',
               '1938615': '15',
               '1292088': '72',
               '4692402': '44',
               '2206586': '105',
               '1068029': '135',
               '22244': '71',
               '3617792': '127',
               '4520089': '73',
               '1292015': '63',
               '4176735': '98',
               '4689106': '40',
               '1294355': '136',
               '2079843': '115',
               '1381991': '17',
               '1292304': '77',
               '1383058': '11',
               '4697380': '42',
               '1302895': '28',
               '4524709': '114',
               '1292411': '99',
               '1793049': '46',
               '2078148': '57',
               '4118607': '84',
               '5720730': '33',
               '1799474': '79',
               '4599118': '24',
               '4645769': '41',
               '1661763': '59',
               '1651781': '23',
               '1292333': '90',
               '1293657': '137',
               '2081344': '126',
               '2078011': '36',
               '4694534': '25',
               '2082382': '134',
               '1293493': '120',
               '2024934': '47',
               '2067320': '100',
               '2079223': '103',
               '2082010': '124',
               '6829958': '49',
               '5541972': '34',
               '2079062': '94',
               '2465441': '58',
               '236317': '48',
               '1382040': '45',
               '1340445': '108',
               '4179159': '122',
               '1284754': '19',
               '5020': '70',
               '1843363': '89',
               '1382020': '37',
               '2206541': '87',
               '2079777': '110',
               '43023': '68',
               '1382051': '55',
               '954156': '38',
               '4710175': '81',
               '2078932': '66',
               '1802485': '78',
               '1292126': '67',
               '2138442': '132',
               '6014901': '61',
               '1295491': '12',
               '1292047': '65',
               '1915972': '39',
               '2170609': '50',
               '2187451': '101',
               '1293437': '107',
               '832505': '16',
               '4694516': '18',
               '1293533': '121',
               '4517306': '96',
               '2082280': '129',
               '2207889': '69',
               '3911027': '92',
               '4755585': '80',
               '7058381': '118',
               '1499736': '82',
               '1290156': '62',
               '2079802': '112',
               '2401525': '64',
               '2006475': '111',
               '2078106': '53',
               '1295563': '14',
               '1292260': '75',
               '1284871': '26',
               '1646548': '97',
               '2079119': '95',
               '1293643': '125',
               '1288530': '22',
               '4164532': '86',
               '4557378': '119',
               '4117778': '85',
               '1795972': '116',
               '1919237': '13',
               '2078998': '90',
               '2963747': '36',
               '3965768': '123',
               '1382196': '115',
               '1293707': '140'}


class PublicEndpoint(BasePermission):

    def has_permission(self, request, view):
        return True


class CreatePStree(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def get(self, request, oid):
        context = dict()
        child_list = []
        try:
            parents = models.ParentDetails.objects.filter(st_oid_id=oid)
        except Exception as e:
            context["Error"] = e
            return Response(context)

        for parent in parents:
            if parent.st_class_id in ['DC', 'DT', 'PC', 'PT', 'V', 'D']:
                st_parent_oid = parent.st_oid_id
                while True:
                    idmap_objs = models.Idmap.objects.filter(st_oid=st_parent_oid)
                    if idmap_objs:
                        idmap_obj = idmap_objs[0]
                        parent_det_obj = models.ParentDetails.objects.filter(st_oid_id=idmap_obj.st_oid)
                        if parent_det_obj:
                            parent_det = parent_det_obj[0]
                            if parent_det.st_class_id == 'D':
                                st_parent_oid = idmap_obj.st_parent_oid
                                continue
                            parent_dict = dict()
                            parent_dict['oid'] = parent_det.st_oid_id
                            parent_dict['name'] = parent_det.st_name
                            parent_dict['ps_oid'] = parent_det.ps_oid
                            parent_dict['st_class'] = parent_det.st_class_id
                            child_list.append(parent_dict)
                        st_parent_oid = idmap_obj.st_parent_oid
                    else:
                        break
            else:
                context["Error"] = "Provided oid is not in required categories."
        child_list.reverse()

        if child_list:
            if child_list[-1]['st_class'] == 'PC':
                child_list.pop()
            nested_folder_id = 0
            for i, k in enumerate(child_list):
                parent_oid = k['ps_oid']
                if parent_oid == 'None':
                    break
                elif child_list[-1]['oid'] == child_list[i]['oid']:
                    nested_folder_id = 0
                else:
                    nested_folder_id = child_list[i]['ps_oid']
            found_child = 'NULL'
            for index, childs in enumerate(child_list):
                parent_oid = childs['ps_oid']
                if parent_oid == 'None':
                    found_child = child_list[i]['oid']
                else:
                    continue
            print nested_folder_id, "<<<<>>>>", found_child
        context["result"] = child_list
        return Response(context)

    def post(self, request):
        parents = models.ParentDetails.objects.filter(ps_oid=None)
        for parent in parents:
            if parent.st_class_id in ['DC', 'DT', 'PC', 'PT', 'V', 'D']:
                print "Migrate"
                self.migrate(parent.st_oid_id)
        return Response(True)

    def migrate(self, oid):
        context = dict()
        child_list = []
        try:
            parents = models.ParentDetails.objects.filter(st_oid_id=oid)
        except Exception as e:
            print e
            context["Error"] = e
            return Response(context)
        for parent in parents:
            if parent.st_class_id in ['DC', 'DT', 'PC', 'PT', 'V', 'D']:
                st_parent_oid = parent.st_oid_id
                while True:
                    idmap_objs = models.Idmap.objects.filter(st_oid=st_parent_oid)
                    if idmap_objs:
                        idmap_obj = idmap_objs[0]
                        parent_det_obj = models.ParentDetails.objects.filter(st_oid_id=idmap_obj.st_oid)
                        if parent_det_obj:
                            parent_det = parent_det_obj[0]
                            if parent_det.st_class_id == 'D':
                                st_parent_oid = idmap_obj.st_parent_oid
                                continue
                            parent_dict = dict()
                            parent_dict['oid'] = parent_det.st_oid_id
                            parent_dict['name'] = parent_det.st_name
                            parent_dict['ps_oid'] = parent_det.ps_oid
                            parent_dict['st_class'] = parent_det.st_class_id
                            child_list.append(parent_dict)
                        st_parent_oid = idmap_obj.st_parent_oid
                    else:
                        break
            else:
                context["Error"] = "Provided oid is not in required categories."
        child_list.reverse()
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/folders"
        if child_list:
            if child_list[-1]['st_class'] == 'PC':
                child_list.pop()
            nested_folder_id = 3178
            for i, k in enumerate(child_list):
                parent_oid = k['ps_oid']
                if parent_oid is None:
                    break
                elif child_list[-1]['oid'] == child_list[i]['oid']:
                    nested_folder_id = 3178
                else:
                    nested_folder_id = child_list[i]['ps_oid']
            context_list = []
            for index, childs in enumerate(child_list):
                parent_oid = childs['ps_oid']
                if parent_oid is None:
                    context = dict()
                    folder_name = childs["name"]
                    context["FolderName"] = folder_name
                    context["Description"] = ""
                    context["NestUnderFolderID"] = nested_folder_id
                    context["APIKey"] = api_key
                    data = json.dumps(context).encode('utf-8')
                    try:
                        r = http.request('POST', url, body=data, headers=headers)
                    except Exception as e:
                        print e
                    data = dict(json.loads(r.data))
                    nested_folder_id = data["FolderID"]
                    try:
                        parent_obj = models.ParentDetails.objects.get(st_oid_id=childs["oid"])
                        if parent_obj and parent_obj.ps_oid is None:
                            parent_obj.ps_oid = nested_folder_id
                            parent_obj.save()
                    except Exception as e:
                        print e
                    context_list.append(json.loads(r.data))
                else:
                    continue
        return Response(context_list)


class GetPasswordList(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def get(self, request, passwordlistid):
        headers = {'APIKey': api_key}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwordlists/" + passwordlistid
        try:
            r = http.request('GET', url, headers=headers)
        except Exception as e:
            print e
        return Response(json.loads(r.data))


class GetAllPasswordLists(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def get(self, request):
        headers = {'APIKey': api_key}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwordlists/"
        try:
            r = http.request('GET', url, headers=headers)
        except Exception as e:
            print e
        return Response(json.loads(r.data))


class CreatePasswordList(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def get(self, request):
        password_ids = models.PasswordIdmap.objects.filter(ps_oid=None)
        for psids in password_ids:
            parent_oid = psids.st_parent_oid
            try:
                d_id = models.ParentDetails.objects.get(Q(st_oid_id=parent_oid), Q(ps_oid=None), Q(st_status='0'),
                                                        (Q(st_class_id='D') | Q(st_class_id='PC')))
                pparent_id = models.Idmap.objects.get(st_oid=parent_oid)

                dc_or_dt = models.ParentDetails.objects.get(st_oid_id=pparent_id.st_parent_oid)
                print "class: {} parent: {}, device: {}, ps_oid: {}".format(dc_or_dt.st_class_id, dc_or_dt.st_name.encode('utf-8', 'ignore'),
                                                                  d_id.st_name.encode('utf-8', 'ignore'),
                                                                 dc_or_dt.ps_oid)
            except Exception as e:
                print "ERR", e
                continue
        return Response("True")

    def post(self, request):
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwordlists/"

        password_ids = models.PasswordIdmap.objects.filter(ps_oid=None)
        for psids in password_ids:
            parent_oid = psids.st_parent_oid
            try:
                d_id = models.ParentDetails.objects.get(Q(st_oid_id=parent_oid), Q(ps_oid=None), Q(st_status='0'),
                                                        (Q(st_class_id='D') | Q(st_class_id='PC')))
                pparent_id = models.Idmap.objects.get(st_oid=parent_oid)
                dc_or_dt = models.ParentDetails.objects.get(st_oid_id=pparent_id.st_parent_oid)
                context = dict()
                context["PasswordList"] = d_id.st_name
                context["LinkToTemplate"] = "false"
                context["CopySettingsFromTemplateID"] = "1"
                context["NestUnderFolderID"] = str(dc_or_dt.ps_oid)
                context["SiteID"] = "0"
                context["APIKey"] = api_key
                data = json.dumps(context).encode('utf-8')
                try:
                    r = http.request('POST', url, body=data, headers=headers)
                except Exception as e:
                    print e
                data = dict(json.loads(r.data))
                password_list_id = data["PasswordListID"]
                d_id.ps_oid = password_list_id
                d_id.save()
            except Exception as e:
                print e
                continue
        return Response("True")


class AddPassword(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        st = siptracklib.connect('st.pws.se', 'vipicm', '####', '9244', use_ssl=False)
        password_idmap = models.PasswordIdmap.objects.filter(ps_oid=None)
        for passwords in password_idmap:
            password_oid = passwords.st_oid
            password_parent_oid = passwords.st_parent_oid
            try:
                st_password_obj = st.getOID(password_oid)
            except Exception as e:
                print "Error_{}: {}".format(e, password_oid)
                continue

            try:
                username = st_password_obj.attributes.get('username').encode('utf-8', 'ignore')
                if username == 'None':
                    username = None
            except Exception as e:
                username = None

            try:
                password = str(st_password_obj.password)
            except Exception as e:
                password = None

            try:
                description = st_password_obj.attributes.get('description')
                if description:
                    description = st_password_obj.attributes.get('description').encode('utf-8', 'ignore')
                else:
                    description = None
            except Exception as e:
                description = None

            try:
                password_parent = models.ParentDetails.objects.get(Q(st_oid_id=password_parent_oid), Q(st_status='0'),
                                                                   Q(st_class_id='DC') | \
                                                                   Q(st_class_id='D') | Q(st_class_id='PC'))
                passwordlistid = password_parent.ps_oid
                context = dict()
                context["ParentDevice"] = password_parent.st_name
                context["PasswordListID"] = passwordlistid
                context["Title"] = "imported from siptrack"
                context["UserName"] = username
                context["password"] = "GeneratePassword"
                context["APIKey"] = api_key
                print context
            except Exception as e:
                continue
            break
        st.logout()
        return Response("True")

    def post(self, request):
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwords"
        st = siptracklib.connect('st.pws.se', 'vipicm', '####', '9244', use_ssl=False)
        password_idmap = models.PasswordIdmap.objects.filter(ps_oid=None)
        for passwords in password_idmap:
            password_oid = passwords.st_oid
            password_parent_oid = passwords.st_parent_oid

            try:
                st_password_obj = st.getOID(password_oid)
            except Exception as e:
                print "{}: {}".format(e, password_oid)
                continue

            try:
                username = st_password_obj.attributes.get('username').encode('utf-8', 'ignore')
                if username == 'None':
                    username = None
            except Exception as e:
                username = None

            try:
                password = str(st_password_obj.password)
                if password:
                    password = password
                    passwords.password_viewed = 'YES'
                    passwords.save()
                else:
                    password = None
            except Exception as e:
                password = None

            try:
                description = st_password_obj.attributes.get('description')
                if description:
                    description = st_password_obj.attributes.get('description').encode('utf-8', 'ignore')
                else:
                    description = None
            except Exception as e:
                description = None
            try:
                title = st_password_obj.key.attributes.get('name').encode('utf-8', 'ignore')
            except Exception as e:
                title = " "

            try:
                password_parent = models.ParentDetails.objects.get(Q(st_oid_id=password_parent_oid), Q(st_status='0'),
                                                                   Q(st_class_id='DC') | Q(st_class_id='D') | Q(st_class_id='PC'))
                passwordlistid = password_parent.ps_oid
                context = dict()
                context["PasswordListID"] = passwordlistid
                context["title"] = title
                context["Description"] = description
                context["UserName"] = username
                context["password"] = password
                context["APIKey"] = api_key
                data = json.dumps(context).encode('utf-8')
                try:
                    r = http.request('POST', url, body=data, headers=headers)
                except Exception as e:
                    print e
                data = dict(json.loads(r.data))
                password_id = data["PasswordID"]
                passwords.ps_oid = password_id
                passwords.password_migrated = 'YES'
                passwords.save()
            except Exception as e:
                print "ParentDetails_{}: {}".format(e, password_oid)
                continue
        return Response("True")


class AddPassPermission(APIView):

    def get(self, request):
        password_idmap = models.PasswordIdmap.objects.filter(ps_oid__isnull=False)
        for passwords in password_idmap:
            if passwords.st_key_id:
                try:
                    security_group_id = key_mapping[str(passwords.st_key_id)]
                    passwords.ps_group_id = security_group_id
                    passwords.save()
                except KeyError:
                    continue
                sec_group = dict()
                sec_group["PasswordID"] = passwords.ps_oid if passwords.ps_oid else None
                sec_group["ApplyPermissionsForSecurityGroupID"] = security_group_id
                sec_group["Permission"] = 'M'
                sec_group["APIKey"] = api_key
                print sec_group
                break
            else:
                continue
        return Response("True")

    def post(self, request):
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwordpermissions"
        password_idmap = models.PasswordIdmap.objects.filter(ps_oid__isnull=False)
        for passwords in password_idmap:
            if passwords.st_key_id:
                try:
                    security_group_id = key_mapping[str(passwords.st_key_id)]
                    passwords.ps_group_id = security_group_id
                    passwords.save()
                except KeyError:
                    continue
                sec_group = dict()
                sec_group["PasswordID"] = passwords.ps_oid if passwords.ps_oid else None
                sec_group["ApplyPermissionsForSecurityGroupID"] = security_group_id
                sec_group["Permission"] = 'M'
                sec_group["APIKey"] = api_key
                sec_group_data = json.dumps(sec_group).encode('utf-8')
                try:
                    request_call = http.request('POST', url, body=sec_group_data, headers=headers)
                    data = dict(json.loads(request_call.data))
                except Exception as e:
                    print e
            else:
                continue
        return Response("True")


class TestCreateFolder(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def post(self, request):
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/folders"
        context = dict()
        context["FolderName"] = "Inwido"
        context["Description"] = ""
        context["NestUnderFolderID"] = "8421"
        context["APIKey"] = api_key
        data = json.dumps(context).encode('utf-8')
        try:
            r = http.request('POST', url, body=data, headers=headers)
        except Exception as e:
            print e
        return Response(json.loads(r.data))


class TestPasswordList(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def post(self, request):
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwordlists"
        context = dict()
        context["PasswordList"] = "kayako-db-backup.i.test.se"
        context["CopySettingsFromTemplateID"] = "1"
        context["LinkToTemplate"] = False
        context["NestUnderFolderID"] = "7890"
        context["SiteID"] = "0"
        context["APIKey"] = api_key
        data = json.dumps(context).encode('utf-8')
        try:
            r = http.request('POST', url, body=data, headers=headers)
            data = dict(json.loads(r.data))
        except Exception as e:
            print e
        return Response(data["PasswordListID"])


class TestPasswordAdd(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def post(self, request):
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwords"
        context = dict()
        context["PasswordListID"] = "12552"
        context["title"] = "Ipeer standard"
        # context["Description"] = "snmp"
        # context["UserName"] = None
        context["Description"] = None
        context["UserName"] = "itek"
        context["password"] = "aaeTozeA1E"
        context["APIKey"] = api_key
        data = json.dumps(context).encode('utf-8')
        try:
            r = http.request('POST', url, body=data, headers=headers)
        except Exception as e:
            print e
        return Response(json.loads(r.data))


class TestPasswordPermissions(APIView):
    parser_classes=(JSONParser,)
    permission_classes=(PublicEndpoint,)

    def post(self, request):
        headers = {'Content-Type': 'application/json'}
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        url = "https://test.pws.se/api/passwordpermissions"
        sec_group = dict()
        sec_group["PasswordID"] = "9093"
        sec_group["ApplyPermissionsForSecurityGroupID"] = "42"
        sec_group["Permission"] = 'M'
        sec_group["APIKey"] = api_key
        sec_group_data = json.dumps(sec_group).encode('utf-8')
        try:
            request_call = http.request('POST', url, body=sec_group_data, headers=headers)
        except Exception as e:
            print e
        return Response(json.loads(request_call.data))
from django.conf.urls import url
from api import api_views
from api import passwordstate as ps_views


urlpatterns = [
    url('siptrack/fetchpasswords', api_views.FetchPasswords.as_view(),
        name='siptrack_fetch_passwords'),
    url('siptrack/dataadd', api_views.DataAdd.as_view(),
        name='siptrack_data_add'),
    url('siptrack/addtree', api_views.AddTreeData.as_view(),
        name='siptrack_data_tree'),


    url('siptrack/device/(?P<device_oid>[0-9]+)/$', api_views.DeviceFetch.as_view(),
        name='siptrack_device_fetch'),
    url('siptrack/device/fetchall', api_views.DeviceFetchAll.as_view(),
        name='siptrack_device_fetchall'),


    # """ passwordstate """
    url('passwordstate/api/createpstree/(?P<oid>[0-9]+)$', ps_views.CreatePStree.as_view(),
        name='passwordstate_createfolder'),
    url('passwordstate/migrate', ps_views.CreatePStree.as_view(),
        name='passwordstate_1createfolder'),
    url('passwordstate/api/passwordlists/create', ps_views.CreatePasswordList.as_view(),
        name='passwordstate_createpasswordlist'),
    url('passwordstate/api/passwordlists/addpassword', ps_views.AddPassword.as_view(),
        name='passwordstate_addpassword'),
    url('passwordstate/api/passwordlists/addpasspermission', ps_views.AddPassPermission.as_view(),
        name='passwordstate_addpasspermission'),

   # """ Testing """"
    url('passwordstate/api/passwordlists/get/(?P<passwordlistid>[0-9]+)/$', ps_views.GetPasswordList.as_view(),
        name='passwordstate_getpasswordlist'),
    url('passwordstate/api/passwordlists/getall', ps_views.GetAllPasswordLists.as_view(),
        name='passwordstate_getallpasswordlists'),
    url('passwordstate/api/passwordlists/test', ps_views.TestPasswordList.as_view(),
        name='passwordstate_testpasswordlist'),
    url('passwordstate/api/folders/test', ps_views.TestCreateFolder.as_view(),
        name='passwordstate_2createfolder'),
    url('passwordstate/api/passwords/test', ps_views.TestPasswordAdd.as_view(),
        name='passwordstate_testpasswordadd'),
    url('passwordstate/api/passwordpermissions/test', ps_views.TestPasswordPermissions.as_view(),
        name='passwordstate_testpasswordpermissions'),
    # url('passwordstate/api/folderpermissions/add/(?P<folder_id>[0-9]+)/$', ps_views.AddFolderPermission.as_view(),
    #     name='passwordstate_addfolderpermission'),
]

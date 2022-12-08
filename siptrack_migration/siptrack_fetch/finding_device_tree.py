import siptracklib


def find_pass(oid):
    llist = []
    for i in oid.listChildren():
        if i.class_id == 'D' and not i.attributes.get('disabled') and i.attributes.get('name'):
            passwords = i.listChildren(include=['password'])
            if passwords:
                print "Device: {}, Passwords: {}".format(i.attributes.get('name').encode('utf8', 'ignore'), passwords)
                # llist.append(str(passwords[0].attributes.get('username')))
    return llist


def parent_reverse_traverse(child):

    while child:
        end_oid = '38'
        parent = child.parent
        if child.oid != end_oid:
            print "ID: {}, Name: {}".format(parent.oid, parent.attributes.get('name').encode('utf8', 'ignore'))
            child = child.parent
            continue
        else:
            break

try:
    s = """294552
337470"""
# 287052
# 29454
# 294618
# 294618
# 27211
# 1857
# 29454
# 29383
# 29454
# 29363
# 29343
# 178759
# 194756
# 2304033
# 29343
# 288252
# 288252
# 295034
# 294166
# 750
# 2769789
# 2770222
# 2950866
# 27498
# 462
# 60844
# 28575
# 25320
# 28495
# 295782
# 288252
# 199603
# 296055
# 296055
# 296055
# 288195
# 2081565
# 2961371
# 2961374
# 4282
# 970931
# 970931
# 4282
# 970931
# 4282
# 1325
# 1325
# 29639
# 29659
# 29659
# 29659
# 29679
# 29679
# 288195
# 29679
# 296900
# 296927
# 296941
# 29699
# 297054
# 29699
# 29699
# 2961775
# 2315722
# 293818
# 293499
# 297353
# 2863265
# 2863265
# 2863265
# 2863265
# 2863265
# 1373885
# 1857
# 297420
# 297420
# 297420
# 297439
# 297439
# 297458
# 297458
# 297477
# 297477
# 297477
# 297496
# 297496
# 297496
# """

    # st = siptracklib.connect('127.0.0.1', 'admin', 'admin', '9242', use_ssl=False)
    # print st.quicksearch('*',
    #                      include=['password'])
    st = siptracklib.connect('st.test', 'vipicm', '#####8', '9242', use_ssl=False)
    for i in s.split("\n"):
        print ">>>>", i
        parent_oid = st.getOID(str(i))
        parent_reverse_traverse(parent_oid)
    # childrens = parent_oid.listChildren(include=['device category'])
    # while childrens:
    #     for ch in childrens:
    #         childrens += ch.listChildren(include=['device category'])
    #         parent_oid = ch
    #         continue
    #     else:
    #         break
    # for i in childrens:
    #     print "{}".format(i.attributes.get('name').encode('utf8', 'ignore') if i.attributes.get('name') else 'Unknown')
    #     find_pass(i)
        # print("ID: {},  Name: {}".format(i.oid, i.attributes.get('name').encode('utf8', 'ignore')))


except Exception as e:
    print(e)
finally:
    st.logout()
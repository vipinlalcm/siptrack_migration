from django.db import models


class Idmap(models.Model):
    st_oid = models.CharField(primary_key=True, max_length=16)
    st_parent_oid = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        db_table = 'idmap'
        app_label = 'api'


class ParentDetails(models.Model):
    STATUS_CHOICES = (
        (0, "Enabled"),
        (1, "Disabled"),
        (2, "NA")
    )

    st_oid = models.ForeignKey(Idmap, on_delete=models.CASCADE, unique=True)
    st_name = models.CharField(max_length=64, blank=True, null=True)
    st_status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    st_class_id = models.CharField(max_length=64, blank=True, null=True)
    ps_oid = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'parent_details'
        app_label = 'api'


class PasswordIdmap(models.Model):
    LOCAL_STATUS_CHOICES = (
        (0, "New"),
        (1, "Exist")
    )

    st_oid = models.CharField(primary_key=True, max_length=16)
    st_parent_oid = models.CharField(max_length=16, blank=True, null=True)
    st_class_id = models.CharField(max_length=64, blank=True, null=True)
    ps_oid = models.CharField(max_length=64, blank=True, null=True)
    st_key_id = models.CharField(max_length=64, blank=True, null=True)
    ps_group_id = models.CharField(max_length=64, blank=True, null=True)
    local_status = models.IntegerField(choices=LOCAL_STATUS_CHOICES, default=0)
    password_viewed = models.CharField(max_length=64, default='NO')
    password_migrated = models.CharField(max_length=64, default='NO')

    class Meta:
        db_table = 'password_idmap'
        app_label = 'api'


class PasswordParentDetails(models.Model):
    STATUS_CHOICES = (
        (0, "Enabled"),
        (1, "Disabled"),
        (2, "NA")
    )
    LOCAL_STATUS_CHOICES = (
        (0, "New"),
        (1, "Exist")
    )

    st_oid = models.CharField(max_length=64, blank=True, null=True, unique=True)
    st_name = models.CharField(max_length=64, blank=True, null=True)
    st_status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    st_class_id = models.CharField(max_length=64, blank=True, null=True)
    local_status = models.IntegerField(choices=LOCAL_STATUS_CHOICES, default=0)

    class Meta:
        db_table = 'password_parent'
        app_label = 'api'


class Passwords(models.Model):
    STATUS_CHOICES = (
        (0, "Pending"),
        (1, "Done")
    )
    st_parent_oid = models.ForeignKey(PasswordParentDetails, on_delete=models.CASCADE)
    username = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True)
    ps_oid = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    class Meta:
        db_table = 'passwords'
        app_label = 'api'




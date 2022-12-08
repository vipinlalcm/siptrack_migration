
class AppDBRouter(object):

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'siptrack_fetch':
            return 'siptrack_fetch'
        return 'api'

    def db_for_write(self, model, **hints):

        if model._meta.app_label == "api":
            return 'api'

    def allow_relation(self, obj1, obj2, **hints):

        return True

    def allow_syncdb(self, db, model):

        if model._meta.app_label == 'api':
            return True

        return False

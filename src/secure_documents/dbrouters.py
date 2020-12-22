class SecureDBRouter:
    router_db = 'secure_documents_db'
    router_apps = {'secure_documents'}

    def db_for_read(self, model, **hints):
        """ reading CompanySecureDocument from secure_documents """
        if model._meta.app_label in self.router_apps:
            return self.router_db
        return None

    def db_for_write(self, model, **hints):
        """ writing CompanySecureDocument to secure_documents """
        if model._meta.app_label in self.router_apps:
            return self.router_db
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        is_current_app = app_label in self.router_apps

        if db == self.router_db:
            return is_current_app

        return not is_current_app

    def allow_relation(self, obj1, obj2, **hints):
        return True

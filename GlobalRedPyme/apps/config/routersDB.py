# Este archivo sirve para configurar las bases de datos con las app
class GRPPERSONASRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'personas_personas', 'personas_historialLaboral', 'personas_rucPersonas',
                        'personas_proveedores'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_portal_personas_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_portal_personas_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_portal_personas_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_portal_personas_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_portal_personas_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_portal_personas_db'
        return None


class GRPCORERouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'core_monedas'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_coop_core_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_core_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_coop_core_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_core_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_coop_core_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_coop_core_db'
        return None


class GRPCORPRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'corp_cobrarSupermonedas', 'corp_autorizaciones', 'corp_empresas', 'corp_movimientoCobros',
                        'corp_pagos', 'corp_creditoPersonas', 'corp_creditoPreaprobados', 'corp_notasPedidos',
                        'corp_monedasEmpresa', 'corp_creditoArchivos', 'corp_envios', 'corp_firmaElectronica',
                        'corp_pagoProveedores', 'corp_pagoEmpleados'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_portal_corp_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_portal_corp_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_portal_corp_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_portal_corp_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_portal_corp_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_portal_corp_db'
        return None


class MDMRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'mdm_clientes', 'mdm_facturas', 'mdm_negocios', 'mdm_prospectosClientes'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_coop_mdm_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_mdm_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_coop_mdm_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_mdm_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_coop_mdm_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_coop_mdm_db'
        return None


class MDPRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'mdp_parametrizaciones', 'mdp_categorias', 'mdp_productos', 'mdp_fichaTecnicaProductos',
                        'mdp_subCategorias'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_coop_mdp_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_mdp_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_coop_mdp_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_mdp_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_coop_mdp_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_coop_mdp_db'
        return None


class MDORouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'mdo_parametrizaciones', 'mdo_generarOferta', 'mdo_prediccionCrosseling',
                        'mdo_prediccionProductosNuevos', 'mdo_prediccionRefil'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_coop_mdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_mdo_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_coop_mdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_mdo_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_coop_mdo_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_coop_mdo_db'
        return None


class GDORouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'gdo_parametrizaciones', 'gdo_gestionOferta'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_coop_gdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_gdo_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_coop_gdo_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_gdo_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_coop_gdo_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_coop_gdo_db'
        return None


class GDERouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'gde_parametrizaciones', 'gde_gestionEntrega'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to grp_g_coop_gde_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_gde_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to grp_g_coop_gde_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'grp_g_coop_gde_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'grp_g_coop_gde_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'grp_g_coop_gde_db'
        return None

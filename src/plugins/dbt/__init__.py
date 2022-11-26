from airflow.plugins_manager import AirflowPlugin


class DbtShiruFlowPlugin(AirflowPlugin):
    name = "DbtShiruFlowPlugin"
    operators = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
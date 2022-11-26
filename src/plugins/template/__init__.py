"""ShiruFlow Template Plugin."""

from airflow.plugins_manager import AirflowPlugin


class ShiruFlowTemplatePlugin(AirflowPlugin):
    name = "ShiruFlowTemplatePlugin"
    operators = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []

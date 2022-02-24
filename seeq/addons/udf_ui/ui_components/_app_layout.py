import traitlets
import ipyvuetify as vue
from pathlib import Path
from ._search_display import SearchDisplay
from ._function_parameters_display import FunctionParametersDisplay
from ._function_documentation import FunctionDocumentation
from ._summary_page import SummaryPage
from ._access_management import AccessManagement
from seeq.addons.udf_ui.backend import MessageType

CURRENT_DIR = Path(__file__).parent.resolve()


class AppLayout(vue.VuetifyTemplate):
    """
    """

    template_file = str(CURRENT_DIR.joinpath('templates', 'AppLayout.vue'))
    confirmation_snackbar_visible = traitlets.Bool(default_value=False).tag(sync=True, allow_null=False)
    success_failure_message = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    api_exception = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    message_color = traitlets.Unicode(allow_none=True, default_value='').tag(sync=True)
    snackbar_timeout = traitlets.Integer(default_value=5000).tag(sync=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_display = SearchDisplay(**kwargs)
        self.function_parameters_display = FunctionParametersDisplay(**kwargs)
        self.function_documentation = FunctionDocumentation(**kwargs)
        self.access_management = AccessManagement(**kwargs)
        self.summary_page = SummaryPage(**kwargs)
        self.components = {
            'search-display': self.search_display,
            'function-parameters-display': self.function_parameters_display,
            'function-documentation': self.function_documentation,
            'access-management': self.access_management,
            'summary-page': self.summary_page
        }

    def on_message_event(self, message_details):
        if self.confirmation_snackbar_visible:
            self.confirmation_snackbar_visible = False
        self.success_failure_message = message_details['message']
        self.message_color = 'green darken-2' if message_details['type'] == MessageType.SUCCESS \
            else 'red darken-2'
        self.snackbar_timeout = 5000 if message_details['type'] == MessageType.SUCCESS \
            else 180000
        self.confirmation_snackbar_visible = True

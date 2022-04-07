from seeq.addons.udf_ui.ui_components import AppLayout
from seeq.addons.udf_ui.backend import BackEnd


class UserDefinedFunctionsUI:
    """
    Main class for the Add-on. Creates an instance of the Add-on UI and passes the
    callbacks for the different backend functionalities that the UI components use.

    This class also facilitates the flow of information from the backend to the
    front end by subscribing the methods in the UI components to backend events.


    Attributes
    ----------
    backend: seeq.addons.udf_ui.backend.BackEnd
        The backend object containing the currently selected package, function, etc

    app: seeq.addons.udf_ui.ui_components.AppLayout
        An instance of the Add-on UI
    """
    def __init__(self):
        self.backend = BackEnd()
        self.app = AppLayout(fetch_packages=self.backend.fetch_udf_packages,
                             update_package_object_on_change=self.backend.update_package_object_on_change,
                             update_function_on_change=self.backend.update_function_object_on_change,
                             parse_params=self.backend.parse_params,
                             fetch_users_autocomplete=self.backend.fetch_users_autocomplete,
                             request_updated_summary_on_review=self.backend.request_updated_summary_on_review,
                             update_params_formula_on_request=self.backend.update_params_formula_on_request,
                             update_doc_on_request=self.backend.update_doc_on_request,
                             update_access_list_on_request=self.backend.update_access_list_on_request,
                             submit_changes=self.backend.submit_changes,
                             archive_object=self.backend.archive_object)

        self.backend.package_change_event.subscribe(self.app.search_display.on_package_change)
        self.backend.package_change_event.subscribe(self.app.function_documentation.on_package_change)
        self.backend.package_change_event.subscribe(self.app.access_management.on_package_change)
        self.backend.package_change_event.subscribe(self.app.summary_page.on_package_change)

        self.backend.function_change_event.subscribe(self.app.function_parameters_display.on_function_change)
        self.backend.function_change_event.subscribe(self.app.function_documentation.on_function_change)
        self.backend.function_change_event.subscribe(self.app.access_management.on_function_change)
        self.backend.function_change_event.subscribe(self.app.summary_page.on_function_change)

        self.backend.summary_update_requested_event.subscribe(self.app.function_documentation.on_update_request)
        self.backend.summary_update_requested_event.subscribe(self.app.access_management.on_update_request)
        self.backend.summary_update_requested_event.subscribe(self.app.function_parameters_display.on_update_request)

        self.backend.summary_update_published_event.subscribe(self.app.summary_page.on_update_summary)

        self.backend.submit_event.subscribe(self.app.search_display.on_submit_refresh)
        
        self.backend.message_event.subscribe(self.app.on_message_event)

    def run(self):
        return self.app

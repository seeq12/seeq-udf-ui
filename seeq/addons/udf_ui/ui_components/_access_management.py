import ipyvuetify as v
import traitlets
from typing import Callable
from pathlib import Path
from seeq.addons.udf_ui.backend import return_func_if_callable, debounce_with_timer

CURRENT_DIR = Path(__file__).parent.resolve()


class AccessManagement(v.VuetifyTemplate):
    """
    """

    template_file = str(CURRENT_DIR.joinpath('templates', 'AccessManagement.vue'))
    class_functionality = traitlets.Unicode(allow_none=True, default_value='Access Control').tag(sync=True)
    access_management_visible = traitlets.Bool(default_value=False).tag(sync=True)
    access_management_open = traitlets.Bool(default_value=False).tag(sync=True)
    users_name_list_searched = traitlets.List(default_value=['Everyone']).tag(sync=True)
    users_name_list_selected = traitlets.List(default_value=['Everyone']).tag(sync=True)
    selected_users_dict = traitlets.List(default_value=[{'name': 'Everyone', 'type': 'UserGroup', 'read': True,
                                                         'write': False, 'manage': False}]).tag(sync=True)
    search = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
    headers = traitlets.List(default_value=[{'text': 'Name', 'value': 'name'}, {'text': 'Type', 'value': 'type'},
                                            {'text': 'Read', 'value': 'read'}, {'text': 'Write', 'value': 'write'},
                                            {'text': 'Manage', 'value': 'manage'},
                                            {'text': 'Delete', 'value': 'actions', 'align': 'center',
                                             'sortable': False}]).tag(sync=True)

    def __init__(self, *args,
                 fetch_users_autocomplete: Callable[[None], str] = None,
                 update_access_list_on_request: Callable[[None], str] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.fetch_users_autocomplete = return_func_if_callable(fn=fetch_users_autocomplete, template_name=self.__class__.__name__)
        self.update_access_list_on_request = return_func_if_callable(fn=update_access_list_on_request,
                                                                     template_name=self.__class__.__name__)

        self.observe(handler=self.vue_update_users_auto, names=['search'])

        self.users_info = self.selected_users_dict
        self.users_name_list_searched = [u['name'] for u in self.selected_users_dict]
        self.users_info_searched = []

    @staticmethod
    def set_default(arg, default, **kwargs):
        return default if kwargs.get(arg) is None else kwargs.get(arg)

    @debounce_with_timer(wait_time=0.3)
    def vue_update_users_auto(self, data):
        self.users_info = self.selected_users_dict
        if self.search:
            self.users_info_searched = self.fetch_users_autocomplete(query=str(self.search))
        self.users_name_list_searched = [u['name'] for u in self.users_info_searched] + self.users_name_list_selected
        self.users_info = self.users_info + self.users_info_searched

    def vue_update_selected_list(self, data):
        user_object_list = []
        for selection in data:
            try:
                user_object_list.append(next(u for u in self.users_info if u['name'] == selection))
            except StopIteration:
                pass
        temp = []
        for user in user_object_list:
            if 'username' not in user:
                user['username'] = ''
            temp.append({'name': user['name'], 'username': user['username'], 'type': user['type'], 'read': user['read'],
                         'write': user['write'], 'manage': user['manage']})
        self.selected_users_dict = []
        self.selected_users_dict = temp

    def vue_delete_user_from_table(self, data):
        temp_list = self.selected_users_dict
        temp_list.remove(data)

        self.selected_users_dict = []
        self.selected_users_dict = temp_list

        temp_list = self.users_name_list_selected
        temp_list.remove(str(data['name']))

        self.users_name_list_selected = []
        self.users_name_list_selected = temp_list

    def vue_initialize_access_list(self, data):
        self.users_info = self.selected_users_dict
        self.users_name_list_selected = [u['name'] for u in self.selected_users_dict]
        self.users_name_list_searched = self.users_name_list_selected

    def on_package_change(self, package_and_functions):
        self.selected_users_dict = package_and_functions['package'].permissions

    def on_function_change(self, function_and_switches):
        self.access_management_visible = function_and_switches['display_switches'].access_management_visible

    def on_update_request(self, update_requested):
        if update_requested:
            self.update_access_list_on_request(self.selected_users_dict)

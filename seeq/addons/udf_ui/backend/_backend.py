from seeq.addons.udf_ui import backend
from rx.subject import Subject
from collections import namedtuple
from seeq.sdk.rest import ApiException
import traceback


class BackEnd:
    """
    The BackEnd class is where the backend functionality of the tool happens. It uses methods from other modules.

    Attributes
    ----------
    selected_package: seeq.addons.udf_ui.backend.UDFPackage
        The UDF package currently selected by the user

    selected_function: seeq.addons.udf_ui.backend.UDFFunction
        The UDF function currently selected by the user

    function_list: list
        List of functions retrieved for the package

    selected_function_dict: dict
        The function in form of a dictionary.

    push_request_summary: dict
        The summary of the items to be pushed to an existing or
        new Seeq UDF formula function or package

    package_change_event: rx.subject.Subject
        An RxPy event of package change

    function_change_event: rx.subject.Subject
        An RxPy event of function change

    summary_update_published_event: rx.subject.Subject
        An RxPy event of summary publication

    summary_update_requested_event: rx.subject.Subject
        An RxPy event of summary request

    submit_event: rx.subject.Subject
        An RxPy event of submit

    message_event: rx.subject.Subject
        An RxPy event of success/error message

    """
    def __init__(self):
        self.selected_package = None
        self.selected_function = None
        self.function_list = []
        self.push_request_summary = {}
        self.selected_function_dict = None
        self.display_visibility_switches = None

        self.package_change_event = Subject()
        self.function_change_event = Subject()
        self.summary_update_published_event = Subject()
        self.summary_update_requested_event = Subject()
        self.submit_event = Subject()
        self.message_event = Subject()

    @staticmethod
    def _format_funcs_params(functions_and_params):
        functions_with_args = []
        for func in functions_and_params:
            functions_with_args.append(func['unique_name'])
        return sorted(functions_with_args)

    def _find_function(self, user_selected_func):
        func = {}
        try:
            func = next(item for item in self.selected_package.functions_and_params
                        if item['unique_name'] == user_selected_func)
        except StopIteration:
            pass
        except Exception:
            self.message_event.on_next({'type': backend.MessageType.ERROR,
                                        'message': f'An unresolved error occurred when obtaining '
                                                   f'the functions:\n {traceback.format_exc()}'})
        if not func:
            func['func_is_new'] = True
            func['parameters'] = []
            func['examples_and_descriptions'] = []
            func['formula'] = ''
            func['description'] = ''
            func['function_updated'] = False
        else:
            func['func_is_new'] = False

        return func

    def fetch_udf_packages(self):
        packages = []
        try:
            packages = backend.fetch_udf_packages()
        except ApiException as e:
            self.message_event.on_next(
                {'type': backend.MessageType.ERROR, 'message': f'An error was encountered when obtaining a '
                                                               f'list if all packages. '
                                                               f'The Seeq API returned:\n{e.body}'})
            if e.status == 401:
                raise PermissionError('Your do not seem to be logged in to Seeq. '
                                      '\nLog in to Seeq if you are outside the Seeq Datalab environment. '
                                      '\nIf you are running the program in Datalab, contact Support')
        except Exception:
            self.message_event.on_next(
                {'type': backend.MessageType.ERROR,
                 'message': f'An unresolved error occurred when '
                            f'obtaining a list of all packages:\n {traceback.format_exc()}'})

        return packages

    def update_package_object_on_change(self, package_name):
        try:
            self.selected_package = backend.UDFPackage(package_name)
        except ApiException as e:
            self.message_event.on_next(
                {'type': backend.MessageType.ERROR,
                 'message': f'An error was encountered when obtaining package {self.selected_package}. '
                            f'The Seeq API returned:\n{e.body}'})
        except Exception:
            self.message_event.on_next(
                {'type': backend.MessageType.ERROR,
                 'message': f'An unresolved error occurred when obtaining '
                            f'package {self.selected_package}:\n {traceback.format_exc()}'})

        self.push_request_summary['package'] = self.selected_package
        self.push_request_summary['package_name'] = self.selected_package.name

        self.function_list = self._format_funcs_params(self.selected_package.functions_and_params)
        self.selected_function = ''
        self.package_change_event.on_next({'package': self.selected_package, 'function_list': self.function_list})

    def update_function_object_on_change(self, selected_function):
        try:
            self.selected_function_dict = self._find_function(selected_function)
            if self.selected_function_dict:
                self.selected_function = backend.UDFFunction(**self.selected_function_dict)
        except ApiException as e:
            self.message_event.on_next({'type': backend.MessageType.ERROR,
                                        'message': f'An error was encountered when obtaining '
                                                   f'function {selected_function}. '
                                                   f'The Seeq API returned:\n{e.body}'})
        except Exception:
            self.message_event.on_next(
                {'type': backend.MessageType.ERROR,
                 'message': f'An unresolved error occurred when obtaining '
                            f'function {selected_function}:\n {traceback.format_exc()}'})

        if not self.selected_function_dict['func_is_new']:
            try:
                self.selected_function.description = backend.fetch_udf_docs(
                    package_name=self.selected_package.name,
                    func_name=self.selected_function.name).description
            except ApiException as e:
                self.message_event.on_next(
                    {'type': backend.MessageType.ERROR, 'message': f'An error was encountered when obtaining '
                                                                   f'the documentation for function '
                                                                   f'{self.selected_function.name}. '
                                                                   f'The Seeq API returned:\n{e.body}'})
            except Exception:
                self.message_event.on_next(
                    {'type': backend.MessageType.ERROR,
                     'message': f'An unresolved error occurred when obtaining the documentation for function '
                                f'{self.selected_function.name}:\n {traceback.format_exc()}'})

            self.selected_function.function_updated = True
            try:
                examples = backend.fetch_udf_docs(package_name=self.selected_package.name,
                                                  func_name=self.selected_function.name).examples
                self.selected_function.examples_and_descriptions = [example.to_dict() for example in examples]
            except ApiException as e:
                self.message_event.on_next(
                    {'type': backend.MessageType.ERROR, 'message': f'An error was encountered when obtaining '
                                                                   f'the examples for function '
                                                                   f'{self.selected_function.name}. '
                                                                   f'The Seeq API returned:\n{e.body}'})
            except Exception:
                self.message_event.on_next(
                    {'type': backend.MessageType.ERROR,
                     'message': f'An unresolved error occurred when obtaining '
                                f'the examples for function '
                                f'{self.selected_function.name}.:\n {traceback.format_exc()}'})

            self.selected_function.func_is_new = False
        else:
            self.selected_function.func_is_new = True
            self.selected_function.name = selected_function

        self.push_request_summary['function'] = self.selected_function
        self.push_request_summary['function_name'] = self.selected_function.name

        DisplaySwitches = namedtuple('DisplaySwitches', 'parameters_visible description_visible '
                                                        'access_management_visible examples_visible')

        self.display_visibility_switches = DisplaySwitches(True, True, True, True)

        self.function_change_event.on_next(
            {'function': self.selected_function, 'display_switches': self.display_visibility_switches})

    def request_updated_summary_on_review(self):
        self.summary_update_requested_event.on_next(True)
        self.summary_update_published_event.on_next(self.push_request_summary)

    def update_doc_on_request(self, doc):
        self.push_request_summary['package_description'] = doc['package_description']
        self.push_request_summary['function_description'] = doc['function_description']
        self.push_request_summary['examples_and_descriptions'] = doc['examples_and_descriptions']

    def update_access_list_on_request(self, users_dict):
        self.push_request_summary['users_dict'] = users_dict

    def update_params_formula_on_request(self, params_and_formula):
        self.push_request_summary['formula'] = params_and_formula['formula']
        self.push_request_summary['params_and_types'] = params_and_formula['params_and_types']

    def submit_changes(self):
        if self.selected_function.func_is_new:
            func_id = ''
        else:
            func_id = self.selected_function.id

        message = backend.push_udf(package_name=self.push_request_summary['package_name'],
                                   selected_function_name=self.push_request_summary['function_name'],
                                   params_and_types=self.push_request_summary['params_and_types'],
                                   formula=self.push_request_summary['formula'],
                                   examples_and_descriptions=
                                   self.push_request_summary['examples_and_descriptions'],
                                   func_description=self.push_request_summary['function_description'],
                                   package_description=self.push_request_summary['package_description'],
                                   users_and_groups_list=self.push_request_summary['users_dict'],
                                   func_id=func_id, is_new=self.selected_function.func_is_new)

        self.message_event.on_next({'type': message['message_type'], 'message': message['message_content']})
        self.submit_event.on_next(self.push_request_summary['package_name'])

    def archive_object(self, selected_for_delete):
        if selected_for_delete.split(':', 1)[0].strip() == 'Function':
            message = backend.delete_udf_func(self.selected_function.id)
            self.submit_event.on_next(self.push_request_summary['package_name'])

        elif selected_for_delete.split(':', 1)[0].strip() == 'Package':
            message = backend.delete_udf_package(self.selected_package.name)
            self.submit_event.on_next('')
        else:
            message = {'message_content': 'Submit was not done', 'message_type': backend.MessageType.ERROR}

        self.message_event.on_next({'type': message['message_type'], 'message': message['message_content']})

    def fetch_users_autocomplete(self, query):
        users_auto_complete = []
        try:
            users_auto_complete = backend.fetch_users_auto(query)
        except ApiException as e:
            self.message_event.on_next(
                {'type': backend.MessageType.ERROR, 'message': f'An error was encountered when searching '
                                                               f' for users. '
                                                               f'The Seeq API returned:\n{e.body}'})
        except Exception:
            self.message_event.on_next(
                {'type': backend.MessageType.ERROR, 'message': f'An unresolved error occurred when searching '
                                                               f' for users. '
                                                               f'The Seeq API returned:\n {traceback.format_exc()}'})

        return users_auto_complete

    @staticmethod
    def parse_params(formula):
        return backend.formula_parser(formula)

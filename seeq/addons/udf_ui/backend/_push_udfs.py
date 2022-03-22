from seeq.sdk.rest import ApiException
import seeq.sdk as sdk
from seeq import spy
from seeq.addons.udf_ui import backend
import traceback


def _define_type(var_type):
    var_map = {'Signal': '1.toSignal()', 'Condition': 'days()', 'Scalar': '1', 'Scalar (Time)': '1d'}
    return var_map[var_type]


def _get_user_group(group_name):
    user_groups_api = sdk.UserGroupsApi(spy.client)
    return user_groups_api.get_user_groups(name_search=group_name)


def _get_user(user_name):
    users_api = sdk.UsersApi(spy.client)
    return users_api.get_users(username_search=user_name)


def push_udf(package_name, selected_function_name, params_and_types, formula, examples_and_descriptions,
             func_description, package_description, users_and_groups_list, func_id, is_new):
    message_content = ''

    formulas_api = sdk.FormulasApi(spy.client)
    items_api = sdk.ItemsApi(spy.client)
    users_api = sdk.UsersApi(spy.client)

    package_input = ''
    package_output = ''
    ace_list = []

    try:
        package_input = sdk.FormulaPackageInputV1(creator_name=spy.user.name,
                                                  creator_contact_info=spy.user.email)
    except ApiException as e:
        message_content = message_content + '\n' + f'An error was encountered when obtaining the credentials of the active user. ' \
                                   f'The Seeq API returned:\n{e.body}'
    except Exception:
        message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    try:
        package_output = formulas_api.put_package(package_name=package_name, body=package_input)
    except ApiException as e:
        message_content = message_content + '\n' + f'An error was encountered when creating or accessing the package. ' \
                                   f'The Seeq API returned:\n{e.body}'
    except Exception:
        message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    param_inputs = []
    for param_type_pair in params_and_types:
        param = sdk.FormulaParameterInputV1(name=param_type_pair['name'], formula=_define_type(param_type_pair['type']),
                                            unbound=True)
        param_inputs.append(param)

    udf_input = sdk.FunctionInputV1(package_name=package_name,
                                    name=selected_function_name,
                                    type='UserDefinedFormulaFunction',
                                    formula=formula,
                                    parameters=param_inputs
                                    )
    if is_new:
        try:
            formulas_api.create_function(body=udf_input)
        except ApiException as e:
            message_content = message_content + '\n' + f'An error was encountered when creating a new function. ' \
                                       f'The Seeq API returned:\n{e.body}'
        except Exception:
            message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'
    else:
        try:
            formulas_api.update_function(id=func_id, body=udf_input)
        except ApiException as e:
            message_content = message_content + '\n' + f'An error was encountered when updating an existing function. ' \
                                       f'The Seeq API returned:\n{e.body}'
        except Exception:
            message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    example_inputs = []
    for examples_and_description in examples_and_descriptions:
        example_input = sdk.FormulaDocExampleInputV1(description=examples_and_description['description'],
                                                     formula=examples_and_description['formula'])
        example_inputs.append(example_input)

    example_list_input = sdk.FormulaDocExampleListInputV1(examples=example_inputs)

    func_doc_input = sdk.FormulaDocInputV1(description=func_description,
                                           examples=example_list_input)
    package_doc_input = sdk.FormulaDocInputV1(description=package_description)

    try:
        formulas_api.put_formula_doc(package_name=package_name, doc_name='index', body=package_doc_input)
        formulas_api.put_formula_doc(package_name=package_name, doc_name=selected_function_name, body=func_doc_input)
    except ApiException as e:
        message_content = message_content + '\n' + f'An error was encountered when creating formula documentation. ' \
                                   f'The Seeq API returned:\n{e.body}'
    except Exception:
        message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    for user_or_group in users_and_groups_list:
        user_or_group_id = None
        if user_or_group['type'] == 'UserGroup':
            try:
                group = _get_user_group(user_or_group['name'])
                user_or_group_id = group.items[0].id
            except ApiException as e:
                message_content = message_content + '\n' + f'An error was encountered when obtaining the user group info. ' \
                                           f'The Seeq API returned:\n{e.body}'
            except Exception:
                message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

        else:
            try:
                user = _get_user(user_or_group['username'])
                user_or_group_id = user.users[0].id
            except ApiException as e:
                message_content = message_content + '\n' + f'An error was encountered when obtaining the user info. ' \
                                           f'The Seeq API returned:\n{e.body}'
            except Exception:
                message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

        if user_or_group_id:
            access_control_input = {'identityId': user_or_group_id, 'permissions': {'read': user_or_group['read'],
                                                                                    'write': user_or_group['write'],
                                                                                    'manage': user_or_group['manage']}}

            ace_list.append(access_control_input)
    ace_input = {'preview': False, 'entries': ace_list, 'localizeInherited': False,
                 'disablePermissionInheritance': False}
    try:
        items_api.set_acl(id=package_output.id, body=ace_input)
    except ApiException as e:
        message_content = message_content + '\n' + f'An error was encountered when adding or removing access. ' \
                                   f'The Seeq API returned:\n{e.body}'
    except Exception:
        message_content = message_content + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    if not message_content:
        message_content = 'Successfully pushed to Seeq'
        message_type = backend.MessageType.SUCCESS
    else:
        message_type = backend.MessageType.ERROR

    return {'message_content': message_content, 'message_type': message_type}


def delete_udf_func(func_id, is_permanent=False):
    message = ''

    items_api = sdk.ItemsApi(spy.client)
    try:
        items_api.archive_item(id=func_id)
    except ApiException as e:
        message = message + '\n' + f'An error was encountered when deleting function. The Seeq API returned:\n{e.body}'
    except Exception:
        message = message + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    if is_permanent:
        try:
            items_api.archive_item(id=func_id, delete=True)
        except ApiException as e:
            message = message + '\n' + \
                      f'An error was encountered when deleting function. The Seeq API returned:\n{e.body}'
        except Exception:
            message = message + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    if not message:
        message = 'Successfully deleted function'
        message_type = backend.MessageType.SUCCESS
    else:
        message_type = backend.MessageType.ERROR

    return {'message_content': message, 'message_type': message_type}


def delete_udf_package(package_name, is_permanent=False):
    message = ''

    formulas_api = sdk.FormulasApi(spy.client)
    items_api = sdk.ItemsApi(spy.client)
    package_id = None
    try:
        package_id = formulas_api.get_package(package_name=package_name).id
        items_api.archive_item(id=package_id)
    except ApiException as e:
        message = message + '\n' + f'An error was encountered when deleting package. The Seeq API returned:\n{e.body}'
    except Exception:
        message = message + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    if is_permanent:
        try:
            items_api.archive_item(id=package_id, delete=True)
        except ApiException as e:
            message = message + \
                      '\n' + f'An error was encountered when deleting package. The Seeq API returned:\n{e.body}'
        except Exception:
            message = message + '\n' + f'An unresolved error occurred:\n {traceback.format_exc()}'

    if not message:
        message = 'Successfully deleted package'
        message_type = backend.MessageType.SUCCESS
    else:
        message_type = backend.MessageType.ERROR

    return {'message_content': message, 'message_type': message_type}

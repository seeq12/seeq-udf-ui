from seeq.sdk.rest import ApiException
import seeq.sdk as sdk
from seeq import spy


def fetch_udf_packages():
    formulas_api = sdk.FormulasApi(spy.client)
    packages = [p.name for p in formulas_api.get_packages().items]
    return sorted(packages)


def fetch_specified_package(package_name):
    formulas_api = sdk.FormulasApi(spy.client)
    package = None
    is_new_package = False
    try:
        package = formulas_api.get_package(package_name=package_name)
    except ApiException as e:
        if e.status == 404:
            is_new_package = True
    return package, is_new_package


def fetch_udf_function(function):
    formulas_api = sdk.FormulasApi(spy.client)
    func = formulas_api.get_function(id=function.id)

    return func


def fetch_udf_param_type(parameter):
    formulas_api = sdk.FormulasApi(spy.client)
    param_type = formulas_api.compile_formula(formula=parameter.formula).return_type

    return param_type


def fetch_udf_docs(package_name, func_name):
    formulas_api = sdk.FormulasApi(spy.client)
    doc = formulas_api.get_formula_doc(package_name=package_name, doc_name=func_name)

    return doc


def fetch_users_auto(query):
    users_api = sdk.UsersApi(spy.client)
    users_or_groups = [{'name': u.name, 'type': u.type, 'username': u.username, 'read': True, 'write': False,
                        'manage': False} for u in users_api.autocomplete_users_and_groups(query=query).items]

    return users_or_groups


def fetch_access_details(package_id):
    items_api = sdk.ItemsApi(spy.client)
    users = []
    items_access_details = items_api.get_access_control_details(id=package_id)

    for user in items_access_details.entries:
        users.append({'name': user.identity.name, 'username': user.identity.username, 'type': user.identity.type,
                      'read': user.permissions.read, 'write': user.permissions.write,
                      'manage': user.permissions.manage})

    return users


def give_current_user_access():
    current_user = spy.user
    return ({'name': current_user.name,
             'username': current_user.username,
             'type': 'User',
             'read': True,
             'write': True,
             'manage': True})

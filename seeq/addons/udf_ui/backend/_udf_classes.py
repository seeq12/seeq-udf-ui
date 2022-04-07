from seeq.addons.udf_ui import backend


class UDFPackage:
    def __init__(self, name):
        self.name = name
        self.package, self.is_new_package = backend.fetch_specified_package(name)

    @property
    def functions(self):
        if self.is_new_package:
            functions = []
        else:
            functions = [func for func in self.package.functions if
                         not func.is_archived]
        return functions

    @property
    def functions_and_params(self):
        funcs_and_params = []
        for func in self.functions:
            params_list = []
            func_object = backend.fetch_udf_function(func)
            func_dict = {'id': func.id, 'name': func.name, 'formula': func_object.formula}
            for param in func_object.parameters:
                param_dict = {'name': param.name, 'type': backend.fetch_udf_param_type(param)}
                params_list.append(param_dict)

            func_dict['parameters'] = params_list
            types = [param['type'] for param in func_dict['parameters']]
            func_dict['unique_name'] = f"{func_dict['name']}(${', $'.join(types)})"

            funcs_and_params.append(func_dict)
        return funcs_and_params

    @property
    def permissions(self):
        permissions = backend.fetch_access_details(self.package.id) if hasattr(self.package, 'id') else \
            [backend.give_current_user_access()]
        return permissions

    @property
    def description(self):
        if not self.is_new_package:
            return backend.fetch_udf_docs(package_name=self.name, func_name='index').description
        else:
            return ''


class UDFFunction:
    def __init__(self, **entries):
        self.__dict__.update(entries)

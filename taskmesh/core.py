import importlib


def import_class(module_path, function_name):
    module = importlib.import_module(module_path)
    return getattr(module, function_name)


def process_task(data):
    module = data["module"]
    function_name = data["function"]
    args = data["args"]
    kwargs = data["kwargs"]
    func = import_class(module, function_name)
    return func(*args, **kwargs)

import os
import importlib


def get_modules(package="./scripts"):
    """
    获取当前包所有非__init__的模块名
    """
    modules = []
    files = os.listdir(package)

    for file in files:
        if not file.startswith("__") and file not in ["dymanicLoad.py"]:
            name, ext = os.path.splitext(file)
            modules.append(name)

    import_modules_list = {}
    for module in modules:
        pkg = importlib.import_module(__package__ + '.' + module)
        import_modules_list[module] = pkg

    return import_modules_list

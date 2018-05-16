def _import_all_modules():
    """dynamically imports all modules in the package"""
    import traceback
    import os
    global __all__
    __all__ = []
    globals_, locals_ = globals(), locals()

    # dynamically import all the package modules
    for filename in os.listdir(__name__):
        # process all python files in directory that don't start with underscore
        # (which also keeps this module from importing itself)
        if filename[0] != '_' and filename.split('.')[-1] in ('py', 'pyw'):
            modulename = filename.split('.')[0]  # filename without extension
            package_module = '.'.join([__name__, modulename])
            try:
                module = __import__(package_module, globals_, locals_, [modulename])
            except:
                traceback.print_exc()
                raise
            for name in module.__dict__:
                if not name.startswith('_'):
                    globals_[name] = module.__dict__[name]
                    __all__.append(name)

_import_all_modules()
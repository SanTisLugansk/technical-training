{
    "name": "Estate account",  # The name that will appear in the App list
    "version": "16.0.0.0.1",  # Version
    "application": True,  # This line says the module is an App,
                          # and not a module
    "depends": ['base',
                'estate',
                'account'],  # dependencies
    "installable": True,
    'license': 'LGPL-3',
}

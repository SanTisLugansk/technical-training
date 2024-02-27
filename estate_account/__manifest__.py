{
    "name": "Real estate account",  # The name that will appear in the App list
    "version": "16.0.0.0.1",  # Version
    "depends": ['base',
                'estate',
                'account'],  # dependencies
    "application": True,    # This line says the module is an App,
                            # and not a module
    "installable": True,
    # "auto_install": True,
    'license': 'LGPL-3',
}

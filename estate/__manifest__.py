{
    "name": "Real Estate",  # The name that will appear in the App list
    "version": "16.0.0.0.1",  # Version
    "depends": ["base", "web"],  # dependencies
    "data": ['security/ir.model.access.csv',
             'views/estate_property_tag_views.xml',
             'views/estate_property_views.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_offer_views.xml',
             'views/estate_menu.xml',
             'views/res_users_views.xml',
             'report/estate_property_templates.xml',
             'report/estate_property_reports.xml',
             'data/estate.property.type.csv',
             'demo/estate.property.csv',
             'demo/estate_property_data.xml',
             'demo/estate_property_offer_data.xml'
             ],
    "application": True,  # This line says the module is an App, and not a module
    "installable": True,
    'license': 'LGPL-3',
}

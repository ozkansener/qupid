from flask_restplus import Api

from .multi import api as multi_api

api = Api(
    title='Information Gadget',
    version='0.1',
    description='Vrije Universiteit, Universiteit van Amsterdam, Centrum Wiskunde & Informatica'
)

api.add_namespace(multi_api)

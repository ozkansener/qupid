from flask_restplus import Api

from .single import api as single_api
from .multi import api as multi_api

api = Api(
    title='Inspector Gadget',
    version='1.0',
    description='Vrije Universiteit, Universiteit van Amsterdam, Centrum Wiskunde & Informatica'
)

api.add_namespace(single_api)
api.add_namespace(multi_api)

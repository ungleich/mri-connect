"""
Service with a smile
http://flask-restplus.readthedocs.io
"""

from flask_restplus import Resource

from . import db, api_rest
from ..models import Person, Organisation

ns = api_rest.namespace('search',
    description = 'Search API'
)

def personModel(p):
    return p.dict()

@ns.route('/updated')
class PeopleUpdated(Resource):
    """ List latest people updates """

    @ns.doc('latest_people')
    def get(self):
        return [personModel(p) for p in Person.query
                .limit(50)
                .all()]

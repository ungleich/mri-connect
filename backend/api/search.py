"""
Service with a smile
http://flask-restplus.readthedocs.io
"""

from flask_restplus import Resource
from flask import request

from . import db, api_rest
from sqlalchemy.sql import and_, or_, not_

from ..models import Person, Organisation
from ..schema import PersonSchema, OrganisationSchema

person_schema = PersonSchema()
organisation_schema = OrganisationSchema()

ns = api_rest.namespace('search',
  description = 'Search API'
)

@ns.route('/updated')
class PeopleUpdated(Resource):
  """ List latest people updates """

  @ns.doc('latest_people')
  def get(self):
    return [person_schema.dump(p) for p in Person.query
        .limit(10).all()]

@ns.route('/keyword')
class PeopleByKeyword(Resource):
  """ List people by keyword """

  @ns.doc('search_people')
  def get(self):
    q = request.args.get("q")
    if not q: return []
    q = q.strip()
    if not q or len(q) < 3: return []

    query = Person.query
    clauses = [Person._indexer.ilike('%{0}%'.format(k)) for k in q.split(" ")]
    query = query.filter(*clauses)

    # if ra.get('country') and len(ra.get('country')) > 2:
    #     query = query.filter(
    #         Person.country.ilike("%" + ra.get('country').strip().lower() + "%")
    #     )
    # if ra.get('range') and len(ra.get('range')) > 2:
    #     query = query.join(Person.ranges).filter(
    #         Range.name.ilike("%" + ra.get('range').strip().lower() + "%")
    #     )
    # if ra.get('field') and len(ra.get('field')) > 2:
    #     query = query.join(Person.research_fields).filter(
    #         Field.name.ilike("%" + ra.get('field').strip().lower() + "%")
    #     )
    # if ra.get('taxon') and len(ra.get('taxon')) > 2:
    #     query = query.join(Person.research_taxa).filter(
    #         Taxon.name.ilike("%" + ra.get('taxon').strip().lower() + "%")
    #     )

    query = query.order_by(Person.last_name.asc())
    query = query.limit(10)
    return [person_schema.dump(p) for p in query.all()]

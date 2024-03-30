from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from datetime import datetime
from src.model.agency import Agency
from src.model.newspaper import Newspaper
import random
import string
newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })
statpaper_model = newspaper_ns.model('NewspaperStatsModel', {
    'number_of_subscribers': fields.Integer(required=True,
            help='The number of subscribers of the newspaper'),
    'monthly_revenue': fields.Float(required=True,
            help='The monthly revenue of the newspaper'),
    'annual_revenue': fields.Float(required=True, help='The annual revenue of the newspaper')
    })


@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        paper_id = int(datetime.now().strftime("%Y%m%d%H%M%S"))
        # create a new paper object and add it
        if newspaper_ns.payload['name'] == "string" or newspaper_ns.payload['frequency'] == 0 or newspaper_ns.payload['price'] <0:
            return jsonify("Please provide a valid input")
        else:
            new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
            Agency.get_instance().add_newspaper(new_paper)
            # return the new paper
            return new_paper


    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result.to_dict()

    @newspaper_ns.doc(description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().update_newspaper(targeted_paper, newspaper_ns.payload['name'], newspaper_ns.payload['frequency'], newspaper_ns.payload['price'])
        return targeted_paper.to_dict()

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")
@newspaper_ns.route('/<int:paper_id>/stats')
class NewspaperStats(Resource):
    @newspaper_ns.doc(description="Get statistics of a newspaper")
    @newspaper_ns.marshal_with(statpaper_model, envelope='newspaper')
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        stats = Agency.get_instance().get_stats_paper(targeted_paper)
        return stats


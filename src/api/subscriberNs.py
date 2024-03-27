import random
from flask import jsonify, Response
from flask_restx import Namespace, Resource, fields
from src.model.agency import Agency
from src.model.subscriber import Subscriber
import string
from datetime import datetime
from src.api.issueNs import issue_model
subscriber_ns = Namespace("subscriber", description="Subscriber related operations")
subscriber_model = subscriber_ns.model('SubscriberModel', {
    'id': fields.Integer(required=False, help='The unique identifier of a subscriber'),
    'sub_name': fields.String(required=True, help='The name of the subscriber'),
    'address': fields.String(required=True, help='The email of the subscriber'),
})
subscribtion_model = subscriber_ns.model('SubscriberSubscribtionModel', {
    'newspaper_id': fields.Integer(required=True, help='The unique identifier of the newspaper')
})
numb_of_issues_model = subscriber_ns.model('SubscriberNumbOfIssuesModel', {
    'paper_id': fields.Integer(required=True, help='The unique identifier of the newspaper'),
    'number_of_issues': fields.Integer(required=True, help='The number of issues of the subscriber')
})
stats_model = subscriber_ns.model('SubscriberStats', {
    'number_of_subscriptions': fields.Integer(required=True, help='The number of subscriptions of the subscriber'),
    'monthly_cost': fields.Float(required=True, help='The monthly cost of the subscriber'),
    'annual_cost': fields.Float(required=True, help='The annual cost of the subscriber'),
    'newspapers': fields.List(fields.Nested(numb_of_issues_model), required=True, help='The list of newspapers that the subscriber is subscribed to')
})
@subscriber_ns.route('/')
class SubscriberAPI(Resource):
    @subscriber_ns.doc(subscriber_model, description="Add a new subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self):
        part_id = datetime.now().strftime("%Y%m%d%H%M%S")
        subscriber_id = int(part_id[:4]+part_id[4:8]+part_id[:8])+random.randint(0, 100)
        # create a new editor object and add it
        if subscriber_ns.payload['sub_name'] == "string" or subscriber_ns.payload['address'] == "string":
            return jsonify("Please provide a valid input")
        else:
            new_subscriber = Subscriber(id=subscriber_id,
                              sub_name = subscriber_ns.payload['sub_name'],
                              address=subscriber_ns.payload['address'])
            Agency.get_instance().add_subscriber(new_subscriber)
            # return the new editor
            return new_subscriber
    @subscriber_ns.marshal_list_with(subscriber_model, envelope='subscriber')
    def get(self):
        return Agency.get_instance().all_subscribers()
@subscriber_ns.route('/<int:sub_id>')
class SubscriberID(Resource):
    @subscriber_ns.doc(description="Get a subscriber")
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def get(self, sub_id):
        search_result = Agency.get_instance().get_subscriber(sub_id)
        return search_result.to_dict()
    @subscriber_ns.doc(description="Update a subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, sub_id):
        search_result = Agency.get_instance().get_subscriber(sub_id)
        search_result.sub_name = subscriber_ns.payload['sub_name']
        search_result.address = subscriber_ns.payload['address']
        return search_result.to_dict()
    @subscriber_ns.doc(description="Delete a subscriber")
    def delete(self, sub_id):
        search_result = Agency.get_instance().get_subscriber(sub_id)
        Agency.get_instance().remove_subscriber(search_result)
        message = f"Subscriber with ID {sub_id} has been deleted"
        return Response(message, status=200, mimetype='text/plain')
@subscriber_ns.route('/<int:sub_id>/subscribe')
class SubsriberSubscribe(Resource):
    @subscriber_ns.doc(description="Subscribe to a newspaper")
    @subscriber_ns.expect(subscribtion_model, validate=True)
    def post(self, sub_id):
        search_result = Agency.get_instance().get_subscriber(sub_id)
        search_result.subscribe(subscriber_ns.payload['newspaper_id'])
        message = f"Subscriber with ID {sub_id} has subscribed to paper with ID {subscriber_ns.payload['newspaper_id']}"
        return Response(message, status=200, mimetype='text/plain')
@subscriber_ns.route('/<int:sub_id>/missingissues')
class SubscriberMissingIssues(Resource):
    @subscriber_ns.doc(description="Get all missing issues of a subscriber")
    @subscriber_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, sub_id):
        search_result = Agency.get_instance().get_subscriber(sub_id)
        missing_issues = Agency.get_instance().missing_issues(search_result)
        missing_issues = [issue.to_dict() for issue in missing_issues]
        return missing_issues
@subscriber_ns.route('/<int:sub_id>/stats')
class SubscriberStats(Resource):
    @subscriber_ns.doc(description="Get statistics of a subscriber")
    @subscriber_ns.marshal_with(stats_model, envelope='stats')
    def get(self, sub_id):
        search_result = Agency.get_instance().get_subscriber(sub_id)
        stats = Agency.get_instance().get_stats(search_result)
        return stats
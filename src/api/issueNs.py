import random
from flask import jsonify, Response
from flask_restx import Namespace, Resource, fields
from src.model.agency import Agency
from src.model.issue import Issue
import string
from src.model.editor import Editor

issue_ns = Namespace("newspaper", description="Newspaper issue related operations")

issue_model = issue_ns.model('NewspaperIssueModel', {
    'issue_id': fields.Integer(required=False, help='The unique identifier of an issue'),
    'release_date': fields.DateTime(required=True, help='The release date of the issue'),
    'released': fields.Boolean(required=True, help='The release status of the issue', default=False),
    'editor_id': fields.Integer(required=True, help='The unique identifier of the editor'),
    'number_of_pages': fields.Integer(required=True, help='The number of pages in the issue')
})
editor_model = issue_ns.model('NewspaperEditorModel', {
    'editor_id': fields.Integer(required=True, help='The unique identifier of the editor')
})
deliver_model = issue_ns.model('NewspaperDeliverModel', {
    'subscriber_id': fields.Integer(required=True, help='The unique identifier of the subscriber')
})

@issue_ns.route('/<int:paper_id>/issue')
class NewspaperIssue(Resource):
    @issue_ns.doc(description="All issues of a newspaper")
    @issue_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify({"message": f"Newspaper with ID {paper_id} was not found"}),404
        issues = targeted_paper.all_issues()
        issues1 = [issue.to_dict() for issue in issues]
        return issues1

    @issue_ns.doc(issue_model, description="Add a new issue to a newspaper")
    @issue_ns.expect(issue_model, validate=True)
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):

        targeted_paper = Agency.get_instance().get_newspaper(paper_id)

          #  return jsonify(f"Newspaper with ID {paper_id} was not found"), 404
        issue_id = "".join(str(paper_id)[::-3])+"".join(random.choices(string.digits, k=2))
        issue = Issue(
            releasedate=issue_ns.payload['release_date'],
            released=issue_ns.payload['released'],
            id=int(issue_id),
            editor_id=issue_ns.payload['editor_id'],
            number_of_pages=issue_ns.payload['number_of_pages']
        )
        targeted_paper.add_issue(issue)

        return issue.to_dict()
@issue_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class NewspaperIssueID(Resource):
    @issue_ns.doc(description="Get an issue of a newspaper")
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def get(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"),404
        issue = targeted_paper.get_issue(issue_id)
        if not issue:
            return jsonify(f"Issue with ID {issue_id} was not found"),404
        return issue.to_dict()


@issue_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class NewspaperIssueRelease(Resource):
    @issue_ns.doc(description="Release an issue of a newspaper")
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"),404
        issue = targeted_paper.get_issue(issue_id)
        if not issue:
            return jsonify(f"Issue with ID {issue_id} was not found"),404
        issue.released = True
        return issue.to_dict()
@issue_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor')
class NewspaperIssueEditor(Resource):
    @issue_ns.doc(description="Update the editor of an issue of a newspaper")
    @issue_ns.expect(editor_model, validate=True)
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id,issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"),404
        issue = targeted_paper.get_issue(issue_id)
        if not issue:
            return jsonify(f"Issue with ID {issue_id} was not found"),404
        issue.set_editor(issue_ns.payload['editor_id'])
        editor = Agency.get_instance().get_editor(issue_ns.payload['editor_id'])
        editor.add_newspaper(targeted_paper)
        return issue.to_dict()
@issue_ns.route('/<int:paper_id>/issue/<int:issue_id>/deliver')
class NewspaperIssueDeliver(Resource):
    @issue_ns.doc(description="Deliver an issue of a newspaper")
    @issue_ns.expect(deliver_model, validate=True)

    def post(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"),404
        issue = targeted_paper.get_issue(issue_id)
        if not issue:
            return jsonify(f"Issue with ID {issue_id} was not found"),404
        if issue.released:
            message = issue.deliver(issue_ns.payload['subscriber_id'])
            return Response(message, status=200, mimetype='text/plain')
        else:
            return jsonify(f"Issue with ID {issue_id} is not released"),404
import random
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from src.model.agency import Agency
from src.model.issue import Issue
import string

issue_ns = Namespace("newspaper", description="Newspaper issue related operations")

issue_model = issue_ns.model('NewspaperIssueModel', {
    'issue_id': fields.Integer(required=False, help='The unique identifier of an issue'),
    'release_date': fields.DateTime(required=True, help='The release date of the issue'),
    'released': fields.Boolean(required=True, help='The release status of the issue'),
    'editor_id': fields.Integer(required=True, help='The unique identifier of the editor')
})

@issue_ns.route('/<int:paper_id>/issue')
class NewspaperIssue(Resource):
    @issue_ns.doc(description="All issues of a newspaper")
    @issue_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify({"message": f"Newspaper with ID {paper_id} was not found"})
        issues = targeted_paper.all_issues()
        issues1 = [issue.to_dict() for issue in issues]
        return issues1


    @issue_ns.doc(issue_model, description="Add a new issue to a newspaper")
    @issue_ns.expect(issue_model, validate=True)
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        issue_id = "".join(str(paper_id)[::-3])+''.join(random.choices(string.digits, k=3))
        issue = Issue(
            releasedate=issue_ns.payload['release_date'],
            released=issue_ns.payload['released'],
            id=int(issue_id),
            editor_id=issue_ns.payload['editor_id']
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
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        issue = targeted_paper.get_issue(issue_id)
        if not issue:
            return jsonify(f"Issue with ID {issue_id} was not found")
        return issue.to_dict()


@issue_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class NewspaperIssueRelease(Resource):
    @issue_ns.doc(description="Release an issue of a newspaper")
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        issue = targeted_paper.get_issue(issue_id)
        if not issue:
            return jsonify(f"Issue with ID {issue_id} was not found")
        issue.released = True
        return issue.to_dict()
@issue_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor')
class NewspaperIssueEditor(Resource):
    @issue_ns.doc(description="Update the editor of an issue of a newspaper")
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        issue = targeted_paper.get_issue(issue_id)
        if not issue:
            return jsonify(f"Issue with ID {issue_id} was not found")
        issue.set_editor(issue_ns.payload['editor_id'])
        return issue.to_dict()

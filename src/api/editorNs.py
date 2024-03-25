import random
from flask import jsonify, Response
from flask_restx import Namespace, Resource, fields
from src.model.agency import Agency
from src.model.editor import Editor
import string
from datetime import datetime
from src.api.issueNs import issue_model
editor_ns = Namespace("editor", description="Editor related operations")
editor_model = editor_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=False, help='The unique identifier of an editor'),
    'editor_name': fields.String(required=True, help='The name of the editor'),
    'address': fields.String(required=True, help='The email of the editor'),
})
@editor_ns.route('/')
class EditorAPI(Resource):
    @editor_ns.doc(editor_model, description="Add a new editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        part_id = datetime.now().strftime("%Y%m%d%H%M%S")
        editor_id = int(part_id[:8]+part_id[4:8]+part_id[:4]+"".join(random.choices(string.digits, k=2)))
        # create a new editor object and add it
        if editor_ns.payload['editor_name'] == "string" or editor_ns.payload['address'] == "string":
            return jsonify("Please provide a valid input")
        else:
            new_editor = Editor(editor_id=editor_id,
                              editor_name = editor_ns.payload['editor_name'],
                              address=editor_ns.payload['address'])
            Agency.get_instance().add_editor(new_editor)
            # return the new editor
            return new_editor
    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def get(self):
        return Agency.get_instance().all_editors()
@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):
    @editor_ns.doc(description="Get an editor")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        return search_result.to_dict()
    @editor_ns.doc(description="Update an editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        search_result.editor_name = editor_ns.payload['editor_name']
        search_result.address = editor_ns.payload['address']
        return search_result.to_dict()
    @editor_ns.doc(description="Delete an editor")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def delete(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        Agency.get_instance().remove_editor(search_result)
        message = f"Editor with ID {editor_id} has been deleted"
        return Response(message, status=200, mimetype='text/plain')
@editor_ns.route('/<int:editor_id>/issues')
class EditorIssue(Resource):
    @editor_ns.doc(description="All issues of an editor")
    @editor_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify({"message": f"Editor with ID {editor_id} was not found"}),404
        issues = targeted_editor.all_issues()
        issues1 = [issue.to_dict() for issue in issues]
        return issues1
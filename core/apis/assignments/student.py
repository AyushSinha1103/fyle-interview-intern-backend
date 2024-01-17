from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from flask import Response
from core.libs.exceptions import FyleError
from .schema import AssignmentSchema, AssignmentSubmitSchema

student_assignments_resources = Blueprint('student_assignments_resources', __name__)

@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)

@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    assignment = AssignmentSchema().load(incoming_payload)
    
    # Assignment content can't be empty
    if not assignment.content:
        return Response(
            "Content cannot be null",
            status=400,
        )
    
    assignment.student_id = p.student_id

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)
    assignment_id = incoming_payload.get('id')
    assignment = Assignment.get_by_id(assignment_id)

    # Assignment can only be submitted when it is in DRAFT state
    if assignment.state == AssignmentStateEnum.SUBMITTED.value or assignment.state == AssignmentStateEnum.GRADED.value:
        raise FyleError(
            status_code=400, 
            message='only a draft assignment can be submitted'
        )
    
    
    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p
    )
    
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)
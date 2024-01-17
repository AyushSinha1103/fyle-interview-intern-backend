from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.models.teachers import Teacher
from flask import Response

principal_assignments_resources= Blueprint('principal_assignments_resources',__name__)


@principal_assignments_resources.route('/assignments', methods = ['GET'], strict_slashes = False)
@decorators.authenticate_principal
def list_submitted_graded_assignments(p):
    """List all submitted and graded assignments"""
    submitted_graded_assignments = Assignment.get_submitted_graded_assignments()
    submitted_graded_assignments_dump = AssignmentSchema().dump(submitted_graded_assignments, many=True)
    return APIResponse.respond(data=submitted_graded_assignments_dump)


@principal_assignments_resources.route('/teachers', methods = ['GET'], strict_slashes = False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all the teachers"""
    teachers_list = Teacher.list_teachers()
    teachers_list_dump = AssignmentSchema().dump(teachers_list, many=True)
    return APIResponse.respond(data=teachers_list_dump)


@principal_assignments_resources.route('/assignments/grade', methods =['POST'], strict_slashes = False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # cant grade assignment in DRAFT state
    if assignment.state == AssignmentStateEnum.DRAFT.value:
        return Response(
        "Cant grade a drafted assignment",
        status=400,
    )

    graded_assignment = Assignment.mark_grade(
        _id = grade_assignment_payload.id,
        grade = grade_assignment_payload.grade,
        auth_principal=p
    )

    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
import app.repositories.enrolment_repo


def test_course_repo():
    methods = [
        "create_enrolment",
        "post_enrolment",
        "get_enrolment_shared_secret",
        "get_enrolment_request",
        "enrolment_exists",
        "is_reference_unique",
        "get_enrolment_status",
        "get_callbacks_list",
        "get_callback",
    ]

    for method in methods:
        assert (
            method in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
        )

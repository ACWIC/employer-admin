import app.repositories.enrolment_repo


def test_course_repo1():
    assert (
        "create_enrolment"
        in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
    )


def test_course_repo3():
    assert (
        "get_enrolment"
        in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
    )


def test_course_repo4():
    assert (
        "enrolment_exists"
        in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
    )


def test_course_repo5():
    assert (
        "is_reference_unique"
        in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
    )


def test_course_repo6():
    assert (
        "get_enrolment_status"
        in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
    )


def test_course_repo7():
    assert (
        "get_callbacks_list"
        in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
    )


def test_course_repo8():
    assert (
        "get_callback"
        in app.repositories.enrolment_repo.EnrolmentRepo.__abstractmethods__
    )

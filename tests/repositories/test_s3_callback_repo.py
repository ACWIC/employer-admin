"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from unittest.mock import patch  # ,MagicMock
from uuid import UUID

from app.config import settings
from app.repositories.s3_callback_repo import S3CallbackRepo


@patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3CallbackRepo()
    boto_client.assert_called_once()


@patch("uuid.uuid4")
@patch("boto3.client")
def test_save_callback(boto_client, uuid4):
    """
    Ensure the S3CallbackRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    callback_id = str(UUID("1dad3dd8-af28-4e61-ae23-4c93a456d10e"))
    uuid4.return_value = callback_id
    e_id = "the_employer_generated_this_identifier"
    k = "the_employer_generated_this_secret"
    tp_seq = 9876543
    pl = {"say": "what?"}
    repo = S3CallbackRepo()
    # settings.CALLBACK_BUCKET= "some-bucket"
    settings.CALLBACK_BUCKET = "some-bucket"
    callback = repo.save_callback(
        enrolment_id=e_id, key=k, tp_sequence=tp_seq, payload=pl
    )

    # TODO: assert enrollment is of the appropriate domain model type
    assert callback.callback_id == callback_id
    assert str(callback_id) == "1dad3dd8-af28-4e61-ae23-4c93a456d10e"

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(callback.json(), "utf-8"),
        Key=f"{callback.enrolment_id}/{callback.callback_id}.json",  # NOQA
        Bucket="some-bucket",
    )


# @patch("uuid.uuid4")
# @patch("boto3.client")
# def test_get_callbacks_list(boto_client, uuid4):
#     """
#     Ensure the S3Enrolmentrepo returns an object with OK data
#     and that an appropriate boto3 put call was made.
#     """
#     print("test_get_callbacks_list()")
#     enrolment_id = "look-at-my-enrolment-id"
#     fixed_uuid_str = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
#     fixed_uuid_str_ = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
#     uuid4.return_value = UUID(fixed_uuid_str)
#     repo = S3CallbackRepo()
#     settings.ENROLMENT_BUCKET = "some-bucket"
#     settings.CALLBACK_BUCKET = "some-bucket1"

# with patch(
#     "json.loads",
#     MagicMock(
#         side_effect=[
#             {
#                 "enrolment_id": "look-at-my-enrolment-id",
#                 "shared_secret": fixed_uuid_str,
#                 "internal_reference": fixed_uuid_str_,
#                 "created": "2020-10-07 15:37:16.727308",
#             }
#         ]
#     ),
# ):
#     callbacks_list = repo.get_callbacks_list(enrolment_id=enrolment_id)
#     print("test callbacks_list", callbacks_list)
#
# assert callbacks_list == {"callbacks_list": []}
# boto_client.return_value.list_objects.assert_called_once_with(
#     Bucket="some-bucket1", Prefix="{}/".format(enrolment_id)
# )
# boto_client.return_value.get_object.assert_called_once_with(
#     Key=f"{enrolment_id}.json", Bucket="some-bucket"
# )

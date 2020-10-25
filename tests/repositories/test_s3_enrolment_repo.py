"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from unittest.mock import patch

from app.config import settings
from app.domain.entities.enrolment import NewEnrolmentSecret
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from tests.test_data.data_provider import DataProvider


@patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3EnrolmentRepo()
    boto_client.assert_called_once()


@patch("app.utils.random.Random.get_uuid")
@patch("boto3.client")
def test_create_enrolment(boto_client, get_uuid):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"

    sample_uuid = DataProvider().sample_uuid
    enrolment_id = sample_uuid
    shared_secret = sample_uuid
    shared_secret_ = {"shared_secret": shared_secret}
    shared_secret_ = NewEnrolmentSecret(**shared_secret_)
    sample_enrolment = DataProvider().crete_enrolment_response
    internal_reference = DataProvider().internal_reference

    get_uuid.return_value = sample_uuid
    enrolment = repo.create_enrolment(internal_reference)

    assert enrolment == sample_enrolment
    boto_client.return_value.put_object.assert_called_with(
        Body=bytes(shared_secret_.json(), "utf-8"),
        Key=f"enrolments/{enrolment_id}.json",
        Bucket="some-bucket",
    )


@patch("json.loads")
@patch("boto3.client")
def test_post_enrolment(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"

    enrolment_id = DataProvider().enrolment_id
    shared_secret = DataProvider().shared_secret
    request = DataProvider().sample_enrolment
    extra_details = DataProvider().sample_enrolment_request_dict

    json_loads.return_value = {"shared_secret": shared_secret}
    enrolment = repo.post_enrolment(extra_details)

    assert enrolment == request
    boto_client.return_value.get_object.assert_called_once_with(
        Key="enrolments/" + enrolment_id + ".json",
        Bucket="some-bucket",
    )
    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(enrolment.json(), "utf-8"),
        Key="enrolment_request/" + extra_details["enrolment_id"] + ".json",
        Bucket="some-bucket",
    )


@patch("json.loads")
@patch("boto3.client")
def test_get_enrolment_request(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"

    enrolment_id = DataProvider().enrolment_id
    sample_enrolment = DataProvider().sample_enrolment
    sample_enrolment_dict = DataProvider().sample_enrolment_dict

    json_loads.return_value = sample_enrolment_dict
    enrolment = repo.get_enrolment_request(enrolment_id)

    assert enrolment == sample_enrolment
    boto_client.return_value.get_object.assert_called_once_with(
        Key="enrolment_request/" + enrolment_id + ".json",
        Bucket="some-bucket",
    )


@patch("json.loads")
@patch("boto3.client")
def test_get_callbacks_list(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = DataProvider().enrolment_id
    callback = DataProvider().sample_callback_dict

    boto_client.return_value.list_objects = list_objects_sample_content
    json_loads.return_value = callback

    callbacks_list = repo.get_callbacks_list(enrolment_id)

    assert callbacks_list == DataProvider().callbacks_list
    boto_client.return_value.get_object.assert_called_once_with(
        Key="callbacks/" + enrolment_id + ".json",
        Bucket="some-bucket",
    )


@patch("json.loads")
@patch("boto3.client")
def test_get_enrolment_status(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = DataProvider().enrolment_id
    callback = DataProvider().sample_callback_dict

    boto_client.return_value.list_objects = list_objects_sample_content
    json_loads.return_value = callback

    enrolment_status = repo.get_enrolment_status(enrolment_id)
    print("enrolment_status", enrolment_status)

    assert enrolment_status == DataProvider().enrolment_status
    boto_client.return_value.get_object.assert_called_once_with(
        Key="callbacks/" + enrolment_id + ".json",
        Bucket="some-bucket",
    )


@patch("json.loads")
@patch("boto3.client")
def test_get_callback(boto_client, json_loads):
    repo = S3EnrolmentRepo()
    settings.CALLBACK_BUCKET = "some-bucket"

    enrolment_id = DataProvider().enrolment_id
    callback_id = DataProvider().callback_id
    sample_callback = DataProvider().sample_callback

    boto_client.return_value.list_objects = list_objects_sample_content
    json_loads.return_value = DataProvider().sample_callback_dict
    enrolment = repo.get_callback(enrolment_id, callback_id)

    assert enrolment == sample_callback
    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"callbacks/{enrolment_id}.json",
        Bucket="some-bucket",
    )


def test_is_reference_unique():
    repo = S3EnrolmentRepo()
    r = repo.is_reference_unique("test-hash")
    assert r is True


@patch("boto3.client")
def test_enrolment_exists(boto_client):
    repo = S3EnrolmentRepo()
    settings.ENROLMENT_BUCKET = "some-bucket"

    enrolment_id = DataProvider().enrolment_id
    response = repo.enrolment_exists(enrolment_id, bucket=settings.ENROLMENT_BUCKET)

    assert response is True
    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"enrolments/{enrolment_id}.json",
        Bucket="some-bucket",
    )


def list_objects_sample_content(Bucket, Prefix):
    return {
        "Contents": [
            {
                "enrolment_id": DataProvider().enrolment_id,
                "bucket": Bucket,
                "prefix": Prefix,
                "Key": "callbacks/" + DataProvider().enrolment_id + ".json",
            }
        ]
    }


def list_objects_sample_content_empty():
    return {}

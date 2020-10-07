"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from os import environ
from uuid import UUID
from unittest.mock import patch
from unittest.mock import MagicMock
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo


@patch('boto3.client')
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3EnrolmentRepo()
    boto_client.assert_called_once()


@patch('uuid.uuid4')
@patch('boto3.client')
def test_save_enrolment(boto_client, uuid4):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    fixed_uuid_str = '1dad3dd8-af28-4e61-ae23-4c93a456d10e'
    uuid4.return_value = UUID(fixed_uuid_str)
    repo = S3EnrolmentRepo()
    environ['ENROLMENT_BUCKET'] = 'some-bucket'
    enrolment = repo.save_enrolment(enrolment_id='look-at-my-enrolment-id')

    # TODO: mock datetime.datetime.now and assert that too
    assert str(enrolment.enrolment_id) == 'look-at-my-enrolment-id'
    assert str(enrolment.key) == fixed_uuid_str

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(enrolment.json(), 'utf-8'),
        Key=f'{enrolment.enrolment_id}.json',  # NOQA
        Bucket='some-bucket'
    )


@patch('uuid.uuid4')
@patch('boto3.client')
def test_get_enrolment(boto_client, uuid4):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    fixed_uuid_str = '1dad3dd8-af28-4e61-ae23-4c93a456d10e'
    uuid4.return_value = UUID(fixed_uuid_str)
    repo = S3EnrolmentRepo()
    environ['ENROLMENT_BUCKET'] = 'some-bucket'
    with patch("json.loads", MagicMock(side_effect=[
        {"created": "2020-10-07T15:37:16.727308", "enrolment_id": "look-at-my-enrolment-id", "key": fixed_uuid_str}])
               ):
        enrolment = repo.get_enrolment(enrolment_id='look-at-my-enrolment-id')

    assert str(enrolment.enrolment_id) == 'look-at-my-enrolment-id'
    assert str(enrolment.key) == fixed_uuid_str

    boto_client.return_value.get_object.assert_called_once_with(
        Key=f'{enrolment.enrolment_id}.json',  # NOQA
        Bucket='some-bucket'
    )

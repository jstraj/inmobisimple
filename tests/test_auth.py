from pytest import fixture

from inmobisimple.inmobi import InmobiAuth
from inmobisimple.models import Auth


@fixture
def sample_auth_json_response():
    return {
        "respList": [{
            "sessionId": "b8************************d31942",
            "accountId": "4028cb************************14",
            "subAccounts": None
        }],
        "error": False,
        "errorList": []
    }


@fixture
def auth_main_keys():
    return ['respList', 'error', 'errorList']


@fixture
def auth_resp_list_keys():
    return ['sessionId', 'accountId', 'subAccounts']


def test_sample_auth_response(sample_auth_json_response, auth_main_keys, auth_resp_list_keys):
    """" Tests Inmobi Auth """

    # Sample auth response
    #response = sample_auth_json_response

    auth = InmobiAuth(username="rajat.panwar@example.com", secret_key="xxxxxxxxxxxxxxxxxxxxxxxx")

    auth_session = auth.generate_session()
    print(auth_session)

    assert isinstance(auth_session, Auth), "The session received is not an instance of Auth class."

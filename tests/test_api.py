from pytest import fixture

from inmobisimple.inmobi import InmobiAuth, Inmobi
from inmobisimple.models import Auth


@fixture
def auth_main_keys():
    return ['respList', 'error', 'errorList']


@fixture
def auth_resp_list_keys():
    return ['sessionId', 'accountId', 'subAccounts']

@fixture
def report_main_keys():
    return ['error', 'respList']


def test_api(auth_main_keys, auth_resp_list_keys, report_main_keys):

    auth = InmobiAuth(username="rajat.panwar@example.com", secret_key="xxxxxxxxxxxxxxxxxxxxxxxxxx")

    auth_session = auth.generate_session()

    assert isinstance(auth_session, Auth), "The session received is not an instance of Auth class."

    print("auth_session - {0}".format({
        "session_id": auth_session.session_id,
        "account_id": auth_session.account_id,
        "secret_key": auth_session.secret_key,
        "password": auth_session.password,
        "username": auth_session.username
    }))

    inmobi = Inmobi(auth_session)

    payload = {
        "reportRequest": {
            "metrics": ['adImpressions'],
            "groupBy": ['date', 'country'],
            "timeFrame": "{start_date}:{end_date}".format(start_date="2019-01-30", end_date="2019-01-31")
        }
    }

    print("The payload - ", payload)

    report = inmobi.create_report(payload)

    page = 1
    while report.has_next_page():

        response = report.get_next_page(length=100)  # default page_length is 5000 (if not included)
        print('page - {page_number}, response - {response}'.format(page_number=page, response=response))
        page = page + 1

        assert isinstance(response, dict), "The Create Session Response is not json"
        assert response['error'] == False, "The session creation API call returned an error"
        assert set(report_main_keys).issubset(response.keys()), "All Keys should be in the main response"

        page = page + 1


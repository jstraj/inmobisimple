from pytest import fixture

from inmobisimple.inmobi import Inmobi
from inmobisimple.models import Auth


@fixture
def report_json_response():
    return {
        "error": False,
        "respList": [{
            "adImpressions": 1786296,
            "date": "2017-07-24 00:00:00"
            }, {
            "adImpressions": 1951438,
            "date": "2017-07-25 00:00:00"
            }, {
            "adImpressions": 8062637,
            "date": "2017-07-29 00:00:00"
            }, {
            "adImpressions": 11151057,
            "date": "2017-07-30 00:00:00"
            }, {
            "adImpressions": 4190525,
            "date": "2017-07-21 00:00:00"
            }, {
            "adImpressions": 10044183,
            "date": "2017-07-27 00:00:00"
            }, {
            "adImpressions": 3881191,
            "date": "2017-07-22 00:00:00"
            }, {
            "adImpressions": 9841295,
            "date": "2017-07-20 00:00:00"
            }, {
            "adImpressions": 4605890,
            "date": "2017-07-26 00:00:00"
            }, {
            "adImpressions": 6175605,
            "date": "2017-07-28 00:00:00"
            }, {
            "adImpressions": 2247567,
            "date": "2017-07-23 00:00:00"
            }]
        }


@fixture
def report_main_keys():
    return ['error', 'respList']


def test_report_response(report_json_response, report_main_keys):
    """" Tests Inmobi Reporting API """

    # Sample auth response
    #response = sample_auth_json_response

    auth_session = Auth(
                session_id="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
                account_id="zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
                secret_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )

    inmobi = Inmobi(auth_session)

    payload = {
        "reportRequest": {
            "metrics": ['adImpressions'],
            "groupBy": ['date','country'],
            "timeFrame": "{start_date}:{end_date}".format(start_date="2019-01-30", end_date="2019-01-31")
        }
    }

    report = inmobi.create_report(payload)

    page = 1
    while report.has_next_page():

        response = report.get_next_page(length=100) # default page_length is 5000 (if not included)

        print('page - {page_number}, response - {response}'.format(page_number=page, response=response))
        page = page + 1

        assert isinstance(response, dict), "The Create Session Response is not json"
        assert response['error'] == False, "The session creation API call returned an error"
        assert set(report_main_keys).issubset(response.keys()), "All Keys should be in the main response"

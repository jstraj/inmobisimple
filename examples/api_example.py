from inmobisimple.inmobi import InmobiAuth, Inmobi
from inmobisimple.models import Auth


def call_api():
    auth = InmobiAuth(username="rajat.panwar@example.com", secret_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

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


if __name__ == "__main__":
    call_api()
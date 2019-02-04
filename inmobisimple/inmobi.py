import json
import requests

from inmobisimple import DEFAULT_REPORTING_VERSION, DEFAULT_AUTH_VERSION
from inmobisimple.exceptions import InmobiReportError
from inmobisimple.models import Auth
from inmobisimple.utils import raise_for_error


class InmobiAuth(object):

    def __init__(self, username, secret_key, password=None, version=DEFAULT_AUTH_VERSION):

        self.username = username
        self.password = password
        self.secret_key = secret_key

        self.auth_uri = "https://api.inmobi.com/v{version}/generatesession/generate".format(version=version)

    def generate_session(self):
        """
              Generates an Inmobi Session. Returns Auth object
        """

        header = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "userName": self.username,
                "secretKey": self.secret_key
        }

        if self.password is not None:
            header['password'] = self.password

        response = requests.get(self.auth_uri, headers=header)

        raise_for_error(response, type='Auth')

        response_json = response.json()

        session_id = response_json['respList'][0]['sessionId']
        account_id = response_json['respList'][0]['accountId']

        return Auth(session_id=session_id, account_id=account_id,
                    username=self.username, password=self.password, secret_key=self.secret_key)


class Inmobi(object):

    def __init__(self, auth, version=DEFAULT_REPORTING_VERSION):
        self.auth = auth

        if isinstance(version, float):
            version = str(version)  # Eliminate any weird float behavior
        self.uri = "https://api.inmobi.com/v{version}/reporting/publisher".format(version=version)

    def create_report(self, payload):
        return InmobiReport(self.auth, payload, self.uri)


class InmobiReport(object):

    DEFAULT_PAGE_LENGTH = 5000

    def __init__(self, auth, payload, uri):

        self.next_page_status = True
        self.last_offset = 0

        self.headers = {
            "accountId": auth.account_id,
            "secretKey": auth.secret_key,
            "sessionId": auth.session_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.main_payload = payload
        self.uri = uri

    def _make_request(self, offset, length):
        """
              A wrapper around the api call. Returns a JSON-decoded dictionary.
        """

        current_payload = self.main_payload.copy()
        current_payload['reportRequest']['offset'] = offset
        current_payload['reportRequest']['length'] = length

        response = requests.post(self.uri, data=json.dumps(current_payload), headers=self.headers)
        raise_for_error(response, 'Report')
        return response.json()

    def has_next_page(self):
        """
              Checks whether there are any results remaining.
        """

        return self.next_page_status

    def get_next_page(self, length=DEFAULT_PAGE_LENGTH):
        """
              Fetches the Inmobi Publisher Report
        """

        if not self.next_page_status:
            raise InmobiReportError("There's no next page.")

        #print('calling for offset - {offset} and page_length - {page_length}'.format(offset=self.last_offset,
                                                                                #page_length=length))
        resp = self._make_request(offset=self.last_offset, length=length)
        self.last_offset = self.last_offset + length

        if 'respList' in resp:
            self.next_page_status = True
        else: # This one is the last page
            resp['respList'] = []
            self.next_page_status = False
        return resp

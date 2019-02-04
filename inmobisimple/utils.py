from inmobisimple.exceptions import InmobiAuthError, InmobiReportError, InmobiError


def raise_for_error(response, type):
    """
          Checks the HTTP Response and raises errors accordingly
    """

    response.raise_for_status()
    resp_json = response.json()
    if resp_json['error']:
        handle_inmobi_errors(resp_json, type)


def handle_inmobi_errors(response_json, type):

    if type == 'Auth':
        raise InmobiAuthError(response_json)
    elif type == 'Report':
        raise InmobiReportError(response_json)
    else:
        raise InmobiError(response_json)

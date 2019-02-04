class Auth(object):

    def __init__(self, session_id, account_id, secret_key, password=None, username=None):
        self.session_id = session_id
        self.account_id = account_id
        self.secret_key = secret_key
        self.password = password
        self.username = username

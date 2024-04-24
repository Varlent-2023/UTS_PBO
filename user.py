from admin import Operator

class User:
    def __init__(self, user_id, password, user_type):
        if not isinstance(user_id, str) or not isinstance(password, str) or not isinstance(user_type, str):
            raise ValueError("user_id, password, and user_type must be strings")
        self._user_id = user_id
        self._password = password
        self._user_type = user_type

    def login(self, user_id, password):
        return True

    def get_user_id(self):
        return self._user_id
    
    def logout(self):
        return False
    
    def get_user_type(self):
        return self._user_type
    
    def report_bug(self, operator, bug_description):
        if not isinstance(operator, Operator):
            raise ValueError("Invalid operator object")
        bug_report = operator.create_bug_report(self, bug_description)
        return bug_report
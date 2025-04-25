
class User:
    
    def __init__(self, login, password):
        self._login = login
        self._password = password
        self._documents = []
        self._notifications = []

    @property
    def notifications(self):
        return self._notifications

    def notify(self, message):
        self._notifications.append(message)
    
    def get_notifications(self):
        return self._notifications.copy()
    

    def redact_roles(self, document, r_or_v, user):
        if (self._login == document._author._login):
            if(r_or_v): document.add_redactor(user)
            else: document.add_visitor(user)
        else: raise Exception("You are not author of the file")


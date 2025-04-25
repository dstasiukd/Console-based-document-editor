from .User import User
from .Document import Document
import os
import dropbox

TOKEN = "sl.u.AFqosj3aYeGw7YVCdHqXEeahhKf6mo6M0pudz3hO8tIt4IncS0Cd5ceLCP2vbDPZ1cKVH2NWHDcWHSnR6dXQUE0SEX32adcaF56QlPoRSWwIBOIj_ViHW7Ruc3iSDaGi-IleR4f2VtohHtuStMdABabmSu9-rr4ofYDTx8nxQa2VX0-MOswu7tJkbnHRHALBiLhSOIacBL_u6eXY2BPMCiE2gaulnchP6Qir31NRPafEAdpRSna9Et-BB7ibXc-RBwCzd2ssOyMSH3-aPbuhGlMOqNxaTKjIa2VgBfzLzql0-QZPSgrmGTcVIkxvwjJcQ59u9aaDxeenvOcOMK_GmWGSLFREgBg0jSt63oisX96QEAeGRhr15M3j7DBE32JIEq9XJSUahLYBEDphlh_IcoN-BbLd8FZSMIdze_LsPQ8H8mMWWMv6g0OzFrK2ABctsN6e_qdvSE_JpvVkDs9dxG_zyFq1aK_1p1zmzg38SsC0SVmbZ0NwQSRVm2o2uIRGeLct3gD4wzQfbEJ2Q4OSn66dff_na42YPF_V74IfEeDZZgzJ8Hl6vknceGybchzNJA5R-wm6uEzjiJlexOhvCDLgluqmlxHNshvpCK_zqC03simM-jqQA6pf4xpBbmi1kSXpvckKk30r0Ro-ERyxfEIV3nDWGMgzvMmOgKcga-1z2H9Kzc7V2_5rsqU4NUr9yKecbT41ckstwa3BKUjKdSkDVgVadsrBRPii4_p_pIskB0bbtUy0BV7CrSMqoRKWw8B2BvW1QamqbOFCf3ZsKDU3Jlpa5CcBtnicilQYJPb0lA3SjOAGBO_Tzt5cnxlhcwrMLEMv6NlYpdxagm9sjxBISaueK2Ha8UbcheCt8OCWRtyVlIaC-H6TPt9HNoMu_T4WFGw-FYp8G6lymRIKNoZPU8twwPZ-N_xqdFQ6oQf0qmAKm08TVpqiauZp29yHdTX3U-dvHWO3NurC2Wa6whGvMkCzJHIhhbiJlRxmUco-ld3GnZdYmgje-lTouUpmFb3JZsPgE8MT8kVXIeKwLEZOwa2_eaP6dNmKbRYG5ShKnlwV8ugMAHNCrbqp8sCepejP6SwIQX9Km8VUQHKVX0kmSTAAjHO-_cr1jJwOWaAl6o0p4yhKNiLHD9UCXBmOZ9L8FVhOnFNuC7mPvAGddjycYkGNk-00GLRyhkWTdhXxkW6kBljuIXNqNH2EosFdLON8YyDIlH9NfV-UkDFv1ySBwm0b0uPo6k_Oha8H-gXIZrIW6J4JKJ7jkuPhYWT64FVeHTsKRArXrWtYJfBLLNqu55D6nPq2G5BodLCRBggox5s-U6_WImWXZO8QdHlJSMDYin3jhFhisBklAMAHOnYLS0qLrGHOo5uHtkYSgPqHI2T3SwENev4sDzhUyoBxbQ8lB2_LPgCUo1zk4L5pQvm7jXagvuCB0-2pL_8PzeYnC8Xf73fbAgpKSvvvad-v_T12oyEgrUtogC-RkgjGmga1"
def file_exists(dbx, file_path):
    try:
        dbx.files_get_metadata(file_path)
        return True
    except dropbox.exceptions.ApiError as err:
        if err.error.is_path() and err.error.get_path().is_not_found():
            return False
        raise

class TextEditor:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._users = []
        self._authorized_user = None
        self._documents = {}
        self._current_document = None
        self._text = None

    @property
    def documents(self):
        return self._documents

    @property
    def current_document(self):
        return self._current_document
    
    @current_document.setter
    def current_document(self,value):
        self._current_document = value

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self,value):
        self._text = value
    
    @property
    def users(self):
        return self._users
    
    @property
    def authorized_user(self):
        return self._authorized_user

    @authorized_user.setter
    def authorized_user(self,value):
        self._authorized_user = value

    def sign_in(self, login, password):
        if(any(user._login == login for user in self.users)):
            raise Exception("account with that login is already existing")
        else:
            self.users.append(User(login, password))
            self._authorized_user = self.users[-1]
        
        

    def log_in(self, login, password):
        if (self.authorized_user != None):
            raise Exception("user already logined")
        for user in self.users:
            if(user._login == login and user._password == password):
                self.authorized_user = user
                break
        if (self.authorized_user == None):
            raise Exception("no user with this login info")

    def log_out(self):
        self.authorized_user = None
        self.close_document()      

    def close_document(self):
        self._current_document = None
        self._text = None

    def check_extension(self,s):
        return s[-4:] == ".txt" or s[-4:] == ".xml" or s[-5:] == ".json" or s[-3:] == ".md"
    
    def redactor_or_visitor(self,s):
        if (self.authorized_user._login == self.documents[s]._author._login or 
        any(user._login == self.authorized_user._login for user in self.documents[s].redactors)):
            return True
        else:
            return False
        

    def open_document(self, s):
        if (self.authorized_user != None):
            if (os.path.exists(f"documents/{s}")):
                self.current_document = self.documents[s]
                if (self.check_extension(s)):
                    with open("documents/" + s, 'r', encoding='utf-8') as file:
                        self.text = file.read()
                else:
                    raise Exception("this extention not supported")
            else: 
                #добавить в документс документ
                if (self.check_extension(s)):
                    self.documents[s] = Document(s, self.authorized_user)
                    self.current_document = self.documents[s]
                    with open("documents/" + s, 'r', encoding='utf-8') as file:
                        self.text = file.read()
                else:
                    raise Exception("this extention not supported")
        else: raise Exception("no authorization")

    def save_document(self):
        if (self.current_document != None):
            with open(f"documents/{self.current_document._name}", 'w', encoding='utf-8') as f:
                f.write(self.text)
            if self._authorized_user != self._current_document._author:
                message = f"document '{self._current_document._name}' was changed by {self._authorized_user._login}"
                self._current_document._author.notify(message)
        else: raise Exception("document not opened")

    def save_document_cloud(self):
        if self.current_document is not None:
            dbx = dropbox.Dropbox(TOKEN)
            dbx.files_upload(
                self.text.encode("utf-8"),
                f"/{self.current_document._name}",
                mode=dropbox.files.WriteMode.overwrite
            )

            # уведомление, если сохраняет не автор
            if self._authorized_user != self._current_document._author:
                message = f"document '{self._current_document._name}' was changed by {self._authorized_user._login}"
                self._current_document._author.notify(message)
        else:
            raise Exception("document not opened")

    def delete_document(self):
        file_path = f"documents/{self.current_document._name}"
        os.remove(file_path)
        del self.documents[self.current_document._name]
        self.text = ""
        self.current_document = None
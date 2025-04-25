from .TextEditor import TextEditor
from .serializer import save_editor_state, load_editor_state
from .TextEditorWidget import TextEditorWidget
from .Adapter import DocumentAdapter, JsonToXmlAdapter, XmlToJsonAdapter

def convert_document(adapter: DocumentAdapter, data):
    return adapter.convert(data)

class TextEditorApp():

    def __init__(self):
        self.editor = TextEditor()
        

    def serialize(self):
        save_editor_state(self.editor, "data/data.json")

    def deserialize(self):
        self.editor = load_editor_state("data/data.json")


    def start(self):
        self.deserialize()
        self.editor.log_in("Dasha","705")
        self.editor.open_document("hello.txt")
        print("\033[33m------------------------------------CONSOLE-BASED DOCUMENT EDITOR------------------------------------\033[0m")
        while(True):
            if(self.editor.authorized_user != None):
                print (f"\033[32mAuthorized user:\033[0m {self.editor.authorized_user._login}")
            else: print("\033[31mNo authorized user\033[0m")

            if(self.editor.current_document!= None):
                print (f"\033[32mCurrent document:\033[0m {self.editor.current_document._name}") 
            else: print("\033[31mNo current document\033[0m")
            print("""\033[33m------------------------------------OPTION MENU------------------------------------------------------
0. Quit
1. Sign in
2. Log in 
3. Log out
4. Open document (if not exist -> create new file)
5. Enter edit mode
6. Redact roles
7. Convert current document (json to xml or xml to json)
8. Delete current document
------------------------------------------------------------------------------------------------------
            \033[0m""")
            c = input("\033[35mEnter a number: \033[0m")
            if (c == '0'):
                break

            elif (c == '1'):
                login = input("Enter login: ")
                password = input("Enter password: ")

                try:
                    self.editor.sign_in(login, password)
                except Exception as e:
                    print(e)

            elif (c == '2'):
                if (self.editor.authorized_user != None):
                    print("User already logined")
                    continue
                else:
                    login = input("Enter login: ")
                    password = input("Enter password: ")
                    try:
                        self.editor.log_in(login, password)
                    except Exception as e:
                        print(e)
            elif (c == '3'):
                if (self.editor.authorized_user == None):
                    print("User is not logined")
                    continue
                else:
                    self.editor.log_out()
                    self.editor.close_document()
            elif (c == '4'):
                while(True):
                        name = input("Enter name of the document: ")
                        try:
                            self.editor.open_document(name)
                            break
                        except Exception as e:
                            print(e)


                
            elif (c == '5'):
                if(self.editor.current_document != None):
                    try:
                        widget = TextEditorWidget(self.editor.text, self.editor)
                        widget.run()
                    except Exception as e:
                        print(e)
                else:
                    print("\033[31mDocument is not opened\033[0m")

            elif (c == '6'):
                if(self.editor.current_document != None):
                    try:
                        i = 0
                        
                        if(self.editor.current_document._author._login == self.editor.authorized_user._login):
                            print("\033[32mUSERS LIST:\033[0m")
                            for user in self.editor.users:
                                print (user._login)
                            s = input("Enter login which you want to add to redactor list of current document: ")
                            for user in self.editor.users:
                                if user._login == s:
                                    self.editor.current_document.add_redactor(user)
                                    break
                            
                        else: print("\033[31mYou are not an author of current document\033[0m")
                    except Exception as e:
                        print(e)
                else: print("\033[31mDocument is not opened\033[0m")
            elif (c == '7'):
                if(self.editor.current_document != None):
                    if(self.editor.current_document._name[-5:] == ".json"):
                        json_to_xml_adapter = JsonToXmlAdapter()
                        json_data = self.editor.text
                        self.editor.open_document(self.editor.current_document._name[:-5] + ".xml")
                        self.editor.text = convert_document(json_to_xml_adapter, json_data)
                        self.editor.save_document()

                    elif(self.editor.current_document._name[-4:] == ".xml"):
                        xml_to_json_adapter = XmlToJsonAdapter()
                        xml_data = self.editor.text
                        self.editor.open_document(self.editor.current_document._name[:-4] + ".json")
                        self.editor.text = convert_document(xml_to_json_adapter, xml_data)
                        self.editor.save_document()

                    else: print("\033[31mNot supported extension\033[0m")

                else: print("\033[31mDocument is not opened\033[0m")
            elif (c == '8'):
                if(self.editor.current_document != None):
                    try:
                        self.editor.delete_document()
                    except Exception as e:
                        print(e)
                else: print("\033[31mDocument is not opened\033[0m")
            else: print("\033[31mWrong input\033[0m")

    def stop(self):
        self.editor.log_out()
        self.editor.close_document()
        self.serialize()

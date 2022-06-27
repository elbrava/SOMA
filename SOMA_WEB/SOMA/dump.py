
class Signup_Screen():
    invalidates = []

    def __init__(self, *args, **kwargs):
        self.link_verification = ''
        self.email = ""
        self.password = ""
        self.password1 = ""
        self.dict = {}

    def user_add(self):

            try:
                auth.create_user(uid=self.password, email=self.email, password=self.password)
                self.link_verification = auth.generate_email_verification_link(self.email)
            except Exception as e:
                print(e)
                User_Exists().open()
            else:
                ref = db.reference('/')
                ref.set(self.password)
                self.ids.sign_up.text = "Successfully Added"
                t = threading.Thread(target=self.email_send)
                t.start()
                return self.password


    def validate(self):
        Signup_Screen.invalidates = []
        self.password = self.ids.password.text
        self.password1 = self.ids.password_confirm.text
        if self.password == "" or self.password1 == "":
            if not Signup_Screen.invalidates.__contains__("password"):
                Signup_Screen.invalidates.append("password")
        self.email = self.ids.email.text
        self.password = hashlib.pbkdf2_hmac(
            'sha256', self.email.encode(), self.password.encode(), 7777).hex()
        self.password1 = hashlib.pbkdf2_hmac(
            'sha256', self.email.encode(), self.password1.encode(), 7777).hex()
        try:
            if not self.email_validate(self.email):
                Signup_Screen.invalidates.append("email")
            if not self.password == self.password1:
                if not Signup_Screen.invalidates.__contains__("password"):
                    Signup_Screen.invalidates.append("password")
            print(Signup_Screen.invalidates)
        except:
            pass
        if not Signup_Screen.invalidates:
            ssd = str(self.user_add())
            if ssd is None:
                self.ids.email.text = ""
                self.ids.password.text = ""
            else:
                store = JsonStore("users.json")
                store.clear()
                d = {"SSD": self.password, **self.dict}
                store[self.email] = d
                print(store.get(store.store_keys()[0]))

        else:
            Invalids(Signup_Screen.invalidates).open()

        # email validation
        # internet error
        # fireBase

    def save(self):
        """"
        saave user and database

        """
        pass

    def email_send(self):
        import smtplib
        from email.message import EmailMessage
        if online():
            psrd = "xvbiephtkeqwynhb"
            sender = "bravo.ale.mando@gmail.com"
            recipient = self.email
            subject = "ACCOUNT ACTIVATION"
            message = "ACTIVATE YOUR ACCOUNT"
            msg = EmailMessage()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.set_content(message)
            t = Template("""
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sara</title>
</head>

<body>
    <div>
        Thank you for creating<br /> An account with Sara <br /> Click button below to activate
    </div>
    <div class="button">
        <a href=$link>
            <button><h1>ACTIVATE</h1></button>
        </a>
    </div>

    <style>
        body {
            background: rgb(112, 41, 99);
        }

        div {
            color: rgb(143, 214, 156);
            text-align: center;
            font-size: 300%;
        }

        a {
            margin: 0 auto;
        }

        button {
            background: rgb(143, 214, 156);
            color: rgb(112, 41, 99);
            border: 4px solid white;
            border-radius: 49px;
            margin: 0 auto;
        }
    </style>
</body>

</html>

    """)

            msg.add_alternative(t.substitute({"link": f"{self.link_verification}"}), subtype="html")
            # issue detected pass *args
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, psrd)
                smtp.send_message(msg)

class Login_Screen(Screen):

    def __init__(self, **kwargs):
        super(Login_Screen, self).__init__(**kwargs)

        self.dict = {}
        self.email = self.ids.email.text
        self.passwrd = ''

    def on_enter(self, *args):
        self.ids.log_in.text = "LOG IN"

    def log_in(self):
        try:
            SSD = self.passwrd
            print(SSD)
            user = auth.get_user(SSD)
        except Exception as e:
            print(e)
            Wrong_Credentials().open()
        else:

            return SSD

    invalidates = []

    def email_validate(self, email):
        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def validate(self):
        Signup_Screen.invalidates = []
        self.passwrd = hashlib.pbkdf2_hmac('sha256', self.ids.email.text.encode(), self.ids.password.text.encode(),
                                           iterations=7777).hex()
        self.email = self.ids.email.text
        try:
            if not self.email_validate(self.email):
                Signup_Screen.invalidates.append("email")
        except:
            pass
        if not Signup_Screen.invalidates:
            if online():
                ssd = str(self.log_in())
                if ssd is None:
                    self.ids.email.text = ''
                    self.ids.password.text = ''
                else:
                    try:
                        ref = db.reference(ssd)
                        self.dict = ref.get()
                        if self.dict is not None:
                            store = JsonStore("users.json")
                            store.clear()
                            store[self.email] = {"SSD": self.passwrd, **self.dict}
                            print(store.get(store.store_keys()[0]))
                            store2 = JsonStore("../../SOMA/results.json")
                            for use_r in self.dict.keys():
                                store2[use_r] = {}

                            self.ids.log_in.text = "Successfully Logged In"
                    except Exception:
                        self.ids.email.text = ''
                        self.ids.password.text = ''
                        Wrong_Credentials().open()
        else:
            Invalids(Signup_Screen.invalidates).open()

        # email validation
        # internet error
        # fireBase

    def save(self):
        """"
        saave user and database

        """
        pass
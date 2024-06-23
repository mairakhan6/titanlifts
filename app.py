import typing
from PyQt6.QtWidgets import QApplication, QDateEdit, QComboBox, QMainWindow, QLabel, QFileDialog, QPushButton, QDialog, QVBoxLayout, QWidget, QLineEdit, QDialogButtonBox, QRadioButton, QTableWidget, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6 import QtCore, uic
from PyQt6.QtGui import QPixmap, QPixmapCache
import pyodbc 
import re
#screens defined in flow diagram

global a_cnic
test= [# database connection to server
# server = 'LAPTOP-9EVG30TP\TAHASERVER'
# database = 'TitanLifts'  # Name of your database
# use_windows_authentication = True  # Set to True to use Windows Authentication

# connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# connection_string =f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:thelocalhost.database.windows.net,1433;Database=TitanLift;Uid=maira;Pwd={reallyStrongPwd123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
# conn = odbc.connect(connection_string)
]

SERVER = 'thelocalhost.database.windows.net,1433'
DATABASE = 'TitanLift'
USERNAME = 'maira'
PASSWORD = 'reallyStrongPwd123'

connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}; Encrypt=yes; TrustServerCertificate=no; Connection Timeout=30;'

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        self.Continue = self.findChild(QPushButton,'Continue')
        self.Close = self.findChild(QPushButton, 'Close')
        
        self.Continue.clicked.connect(self.welcome_screen)
        self.Close.clicked.connect(self.quitting)
        
    def welcome_screen(self): # move on to welcome screen where u can login or register
        self.welcome = WelcomeScreen()
        self.close()
        self.welcome.show()
        
    def quitting(self):
        self.close()

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('welcome.ui', self)
        #loads the welcome screen - three buttons (screen 1)
        
        self.CreateAccount = self.findChild(QPushButton, 'CreateAccount')
        self.LoginButton = self.findChild(QPushButton, 'LoginButton')
        self.QuitButton = self.findChild(QPushButton, 'QuitButton')
        
        self.CreateAccount.clicked.connect(self.open_account_window)
        self.QuitButton.clicked.connect(self.on_quit_button_clicked)
        self.LoginButton.clicked.connect(self.show_login)
        

    def open_account_window(self):
        self.account_window = AccountWindow()
        self.close()
        self.account_window.show() # displays the create account screen (screen 2)
        # self.accept()
        
    def on_quit_button_clicked(self):
        self.close() #app closes
        
    def show_login(self):
        self.login = LoginPortal()
        self.close()
        self.login.show() # move to login

class LoginPortal(QWidget):
    
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.loginEmail = self.findChild(QLineEdit, 'loginEmail')
        self.loginPassword = self.findChild(QLineEdit, 'loginPassword')
        self.ProceedLogin = self.findChild(QPushButton, 'ProceedLogin')
        self.Back = self.findChild(QPushButton, 'Back')
        
        # self.loginEmail.textChanged.connect(self.email_entered)
        # self.loginPassword.textChanged.connect(self.password_entered)
        self.ProceedLogin.clicked.connect(self.check_valid)
        self.Back.clicked.connect(self.back)
        self.loginPassword.textChanged.connect(self.toggle_password_visibility)
    def toggle_password_visibility(self):
        # show/back to hidden
        if self.loginPassword.echoMode() == QLineEdit.EchoMode.Password:
            self.loginPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.loginPassword.setEchoMode(QLineEdit.EchoMode.Password)
    def check_valid(self):
        # check queries here in DB users
        email = self.loginEmail.text()
        pwd = self.loginPassword.text()
        
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        
        # check if email pwd exists in admin
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        sql = '''
        SELECT email,pwd FROM admin_details
        '''
        csr.execute(sql)
        admin_info = csr.fetchall()
        # print(ans)
        conn.commit()
        conn.close()
    
        if bool(match):
            for i in admin_info:
                if email == i[0]:
                    if pwd == i[1]:
                        self.adminscreen = AdminWindow()
                        self.close()
                        self.adminscreen.show()
                
                else:
                # check if email pwd exists in athlete
                    conn= pyodbc.Connection = pyodbc.connect(connection_string)
                    csr: pyodbc.Cursor = conn.cursor()
                    sql = '''
                    SELECT email,pwd FROM athlete_details
                    '''
                    csr.execute(sql)
                    athlete_info = csr.fetchall()
                    # print(ans)
                    conn.commit()
                    conn.close()
        
                    for j in athlete_info:
                        if email == j[0]:
                            if pwd == j[1]:
                                global a_email
                                global a_pwd
                                global a_fname
                                global a_lname
                                global a_city
                                global a_cnic
                                global a_contact_number
                                global a_gender
                                sqls = '''SELECT * from athlete_details where athlete_details.email = ?'''
                                csr.execute(sqls,email)
                                athleteinfo  = csr.fetchone()
                                conn.commit()
                                # for i in athleteinfo:
                                a_email = athleteinfo[0]
                                a_pwd = athleteinfo[1]
                                a_fname = athleteinfo[2]
                                a_lname = athleteinfo[3]
                                a_city = athleteinfo[4]
                                a_cnic = athleteinfo[5]
                                a_contact_number = athleteinfo[6]
                                a_gender = athleteinfo[7]
                                    # break
                                self.athport = AthletePortal()
                                self.close()
                                self.athport.show()
                        else:
                            conn= pyodbc.Connection = pyodbc.connect(connection_string)
                            csr: pyodbc.Cursor = conn.cursor()
                            sql = '''
                            SELECT email,pwd FROM judge_details
                            '''
                            csr.execute(sql)
                            judge_info = csr.fetchall()
                            # print(ans)
                            conn.commit()
                            
                            for k in judge_info:
                                if email == k[0]:
                                    if pwd == k[1]:
                                        global j_email
                                        global j_pwd
                                        global j_fname
                                        global j_lname
                                        global j_city
                                        global j_cnic
                                        global j_contact_number
                                        global j_gender
                                        sqls = '''SELECT * from judge_details where judge_details.email = ?'''
                                        csr.execute(sqls,email)
                                        judgeinfo  = csr.fetchall()
                                        conn.commit()
                                        for i in judgeinfo:
                                            j_email = i[0]
                                            j_pwd = i[1]
                                            j_fname = i[2]
                                            j_lname = i[3]
                                            j_city = i[4]
                                            j_cnic = i[5]
                                            j_contact_number = i[6]
                                            j_gender = i[7]
                                            break
                                            # (j_email, j_pwd, j_fname, j_lname, j_city, j_cnic, j_contact_number, j_gender) = judgeinfo
                                        
                                        
                                        self.judport = JudgePortal()
                                        self.close()
                                        self.judport.show()
        else:
            QMessageBox.critical(self, "Error", "Incorrect Email or Password.")
        conn.close()     
    def get_cnic():
        return a_cnic
    def back(self):
        self.back = WelcomeScreen()
        self.close()
        self.back.show()

class AdminWindow(QWidget):
    def __init__  (self):
        super().__init__() 
        uic.loadUi('admin.ui',self)
        
        self.ManageLifts = self.findChild(QPushButton, 'ManageLifts')
        self.ManageEvent = self.findChild(QPushButton, 'ManageEvent')
        self.CheckLifts = self.findChild(QPushButton, 'CheckLifts')
        self.Close = self.findChild(QPushButton, 'Close')
        
        self.ManageLifts.clicked.connect(self.lift_manager)
        self.ManageEvent.clicked.connect(self.event_manager)
        self.CheckLifts.clicked.connect(self.lift_checker)
        self.Close.clicked.connect(self.quitter)
        
    def lift_manager(self):
        self.lifts = LiftManager()
        self.close()
        self.lifts.show()
        
    def event_manager(self):
        self.event = EventManager()
        self.close()
        self.event.show()
        
    def lift_checker(self):
        self.checker = AdminLiftWindow()
        self.close()
        self.checker.show()
    
    def quitter(self):
        self.closer = WelcomeScreen()
        self.close()
        self.closer.show()
         
class LiftManager(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('managelifts.ui',self)
    
        # add lifts
        self.NameBox = self.findChild(QComboBox, 'NameBox')
        self.EventBox = self.findChild(QComboBox, 'EventBox')
        self.AddLift = self.findChild(QPushButton, 'AddLift')
        
        self.Squat1 = self.findChild(QLineEdit, 'Squat1')
        self.Squat2 = self.findChild(QLineEdit, 'Squat2')
        self.Squat3 = self.findChild(QLineEdit, 'Squat3')  
        self.Bench1 = self.findChild(QLineEdit, 'Bench1')   
        self.Bench2 = self.findChild(QLineEdit, 'Bench2')  
        self.Bench3 = self.findChild(QLineEdit, 'Bench3')  
        self.Deadlift1 = self.findChild(QLineEdit, 'Deadlift1')
        self.Deadlift2 = self.findChild(QLineEdit, 'Deadlift2')
        self.Deadlift3 = self.findChild(QLineEdit, 'Deadlift3')
        
        self.Points = self.findChild(QLineEdit, 'Points')
        self.Total = self.findChild(QLineEdit, 'Total')
        self.Done = self.findChild(QPushButton, 'Done')
        self.Cancel = self.findChild(QPushButton, 'Cancel')
        
        self.AddLift.clicked.connect(self.lift_adder)
        self.Cancel.clicked.connect(self.back)
        self.Done.clicked.connect(self.added)
        
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()

        sql = '''
        SELECT CONCAT(first_name, ' ', last_name) FROM athlete_details;
        '''
        csr.execute(sql)
        names = csr.fetchall()
        for i in names:
            list=(i[0]) 
            self.NameBox.addItem(list)
        conn.commit()
        conn.close()
        
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()

        sql = '''
        SELECT event_name FROM event_schedule;
        '''
        csr.execute(sql)
        names = csr.fetchall()
        for i in names:
            list2=(i[0]) 
            self.EventBox.addItem(list2)
        conn.commit()
        conn.close()
        
    def lift_adder(self):
        squat1 = float(self.Squat1.text())
        squat2 = float(self.Squat2.text())
        squat3 = float(self.Squat3.text())
        bench1 = float(self.Bench1.text())
        bench2 = float(self.Bench2.text())
        bench3 = float(self.Bench3.text())
        deadlift1 = float(self.Deadlift1.text())
        deadlift2 = float(self.Deadlift2.text())
        deadlift3 = float(self.Deadlift3.text())
        athname = self.NameBox.currentText()
        evname = self.EventBox.currentText()
        
        firstname, lastname = athname.split(maxsplit=1)
        
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        sql1 = '''
        SELECT cnic from athlete_details where [athlete_details].first_name = ? and [athlete_details].last_name =? ;
        '''
        csr.execute(sql1,firstname,lastname)
        id = csr.fetchone()[0]
        
        sql2 = '''
        SELECT event_id from event_schedule where [event_schedule].event_name = ?  ;
        '''
        csr.execute(sql2, evname)
        event = csr.fetchone()[0]
        
        sql3 = '''
        INSERT INTO lifts(athleteID, event_id, lift_num, lift_type, lift_amount)
        VALUES
        (?,?,1,?,?),(?,?,2,?,?), (?, ?, 3, ?, ?);
        '''

        csr.execute(sql3, id, event, 'squat',squat1,id,event,'squat',squat2,id,event,'squat',squat3)
        conn.commit()
        csr.execute(sql3,id,event,'bench',bench1,id,event,'bench',bench2,id,event,'bench',bench3)
        conn.commit()
        csr.execute(sql3,id,event,'deadlift',deadlift1,id,event,'deadlift',deadlift2,id,event,'deadlift',deadlift3)
        conn.commit()
        
        sql4 =''' SELECT athleteID, event_ID from lifts '''
        csr.execute(sql4)
        check = csr.fetchall()
        conn.commit()
        
        
        message_box = QMessageBox()
        message_box.setWindowTitle("Information Updated")
        message_box.setText("Lifter information updated!")
        message_box.exec()
        # global total
        if squat3 and bench3 and deadlift3:
            total = squat3+bench3+deadlift3
        
        sql5 = '''SELECT bodyweight from athlete_details where athlete_details.cnic =?'''
        csr.execute(sql5,id)
        bw = csr.fetchone()[0]
        conn.commit

        # Calculate the IPF GL score
        ipf_gl_score = (((total) / 3) * (500 / float(bw))/10)
        # print(ipf_gl_score)
        gl_points = round(ipf_gl_score,2)
        
        self.Total.setText(f'{total:.2f}')
        self.Points.setText(f'{gl_points:.2f}')
            
        conn.close()
        
    def added(self):
        self.next = ThanksUpdate()
        self.close()
        self.next.show()
        
    def back(self):
        self.goback = AdminWindow()
        self.close()
        self.goback.show()
        
class ThanksUpdate(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('thanksadded.ui',self)
            
        self.Done = self.findChild(QPushButton, 'Done')
            
        self.Done.clicked.connect(self.quitter)
            
    def quitter(self):
        self.back = AdminWindow()
        self.close()
        self.back.show()       
         
class EventManager(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('eventmanager.ui',self)
        
        # adding event
        self.EventName = self.findChild(QLineEdit, 'EventName')
        self.EventCity = self.findChild(QComboBox, 'EventCity')
        self.EventStart = self.findChild(QDateEdit, 'EventStart')
        self.EventEnd = self.findChild(QDateEdit, 'EventEnd')
        self.EventVenue = self.findChild(QComboBox, 'EventVenue')
        self.AddEvent = self.findChild(QPushButton, 'AddEvent')
        self.Judge = self.findChild(QComboBox, 'Judge')
        
        # view event
        self.EventOptions = self.findChild(QComboBox, 'EventOptions')
        self.EventLocation = self.findChild(QLineEdit,'EventLocation')
        self.EventJudges = self.findChild(QLineEdit,'EventJudges')
        self.EventAthletes = self.findChild(QLineEdit,'EventAthletes')
        self.EventDate = self.findChild(QLineEdit,'EventDate')
        self.VenueCapacity = self.findChild(QLineEdit,'VenueCapacity')
        
        #general
        self.Back = self.findChild(QPushButton, 'Back')
        
        # event city options
        event_cities = ["Which city would you like to host an event in?","Karachi", "Lahore", "Islamabad"]
        self.EventCity.addItems(event_cities)
        
        # for view events part
        self.EventOptions.currentIndexChanged.connect(self.view_event_details)
        
        # connect everythign 
        self.AddEvent.clicked.connect(self.event_adder)
        self.Back.clicked.connect(self.goback)
        self.EventCity.currentIndexChanged.connect(self.choose_venues)
        
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        
        sqlname = '''
        SELECT CONCAT(first_name, ' ', last_name) FROM judge_details;
        '''
        csr.execute(sqlname)
        names = csr.fetchall()
        for i in names:
            list=(i[0]) 
            self.Judge.addItem(list)
        conn.commit()
        
        sql2 = '''
        SELECT event_name FROM event_schedule;
        '''
        csr.execute(sql2)
        names = csr.fetchall()
        for i in names:
            list=(i[0]) 
            self.EventOptions.addItem(list)
        conn.commit()
        conn.close()
        
    def choose_venues(self):
            selected_city = self.EventCity.currentText()
            #event venue options
            event_venues_khi = ["Fitcon", "Dynamik Studios", "Goldstar"]
            event_venues_lhr = ["Shapes", "IronBox", "Alphalete"]
            event_venues_isl = ["Gritfit", "Jacked Fitness Arena", "Islamabad Club"]
            if selected_city == "Karachi":
                self.EventVenue.addItems(event_venues_khi)
            elif selected_city == "Lahore":
                self.EventVenue.addItems(event_venues_lhr)
            elif selected_city == "Islamabad":
                self.EventVenue.addItems(event_venues_isl)
            else:
                self.EventVenue.addItem("Choose event city first.")   
        
            
    # WRITE CONDITIONS OF ADDING    
    def event_adder(self):
        venue_name = self.EventVenue.currentText()
        city = self.EventCity.currentText()
        event_name = self.EventName.text()
        start_date = self.EventStart.date().toString("yyyy-MM-dd")
        end_date = self.EventEnd.date().toString("yyyy-MM-dd")
        judge = self.Judge.currentText()
        
        # conditions 
        # if judge1 == "":
        #     QMessageBox.critical(self, "Error", "Choose three different judges.")
        if city == "Which city would you like to host an event in?":
            QMessageBox.critical(self, "Error", "Choose city.")
        elif venue_name == "Choose event city first.":
            QMessageBox.critical(self, "Error", "Choose venue.")
        else:
            # sql query update event table
            # Provide the  connection string to connect to the lifters database
            conn= pyodbc.Connection = pyodbc.connect(connection_string)
            csr: pyodbc.Cursor = conn.cursor()
            
            query = '''SELECT venue_id FROM venue_details WHERE venue_name = ? AND city = ?'''
            csr.execute(query,venue_name,city)
            venid = csr.fetchone()[0]
            conn.commit()
            
            firstname1, lastname1 = judge.split(maxsplit=1)
            
            queryy = '''
            SELECT cnic from judge_details where [judge_details].first_name = ? and [judge_details].last_name =? ;
            '''
            csr.execute(queryy,firstname1,lastname1)
            id1 = csr.fetchone()
            conn.commit()
            

            if venid is not None:
                    # Use parameterized query to avoid SQL injection
                    addquery = '''INSERT INTO event_schedule (event_name, venue_id, startdate, enddate,judge_id) VALUES (?, ?, ?, ?,?)'''
                    csr.execute(addquery, event_name, venid, start_date, end_date,id1[0])
                    conn.commit()
            message_box = QMessageBox()
            message_box.setWindowTitle("Information Updated")
            message_box.setText("Event Added!")
            message_box.exec()
            conn.commit()
            conn.close()
        
    def view_event_details(self):
        selected_event = self.EventOptions.currentText()    
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        
        #get event id
        sql23 = '''
        SELECT event_id FROM event_schedule WHERE event_name = ?'''
        csr.execute(sql23, selected_event)
        evid = csr.fetchone()[0]
        conn.commit()
        # query here !
        viewer = '''
                SELECT 
                    CONCAT(v.venue_name,' ', v.city) as Location, CONVERT(varchar, startdate, 23) + '-' + CONVERT(varchar, enddate, 23) AS EventDate, 
                    CONCAT(j1.first_name,' ',j1.last_name) as Judges, 
                    COUNT(lifts.athleteID) as AthletesRegistered, v.capacity as VenueCapacity
                
                FROM 
                    event_schedule es
                    JOIN venue_details v ON es.venue_id = v.venue_id
                    LEFT JOIN judge_details j1 ON es.judge_id = j1.cnic
                    LEFT JOIN lifts ON es.event_id = lifts.event_id

                WHERE
                    es.event_name = ?
                GROUP BY
                    es.startdate, es.enddate, j1.first_name,j1.last_name, v.venue_name, v.city, v.capacity;
            '''

        csr.execute(viewer, selected_event)
        results = csr.fetchall()

        if results:
            for result in results:
                (event_location, event_date, event_judges, event_athletes, venue_capacity) = result

                # Display the results in the corresponding QLineEdits
                self.EventLocation.setText(event_location)
                self.EventDate.setText(event_date)
                self.EventJudges.setText(event_judges)
                self.EventAthletes.setText(str(event_athletes))
                self.VenueCapacity.setText(str(venue_capacity))

        else:
            print(f"Error: Event not found")
                
    def goback(self):
        self.back = AdminWindow()
        self.close()
        self.back.show()
        
class AthletePortal(QWidget):
    def __init__(self, a_cnic):
        super().__init__()
        uic.loadUi('athleteportal.ui', self)
        self.a_cnic = a_cnic
        
        self.Register = self.findChild(QPushButton, 'Register')
        self.CheckLifts = self.findChild(QPushButton, 'CheckLifts')
        
        self.Register.clicked.connect(self.register)
        self.CheckLifts.clicked.connect(self.check_lifts)
        
    def register(self):
        self.reg = AthleteDetailsWindow(self.a_cnic)
        self.close()
        self.reg.show()       

    def check_lifts(self):
        self.lifts = AthleteCheckLifts()
        self.close()
        self.lifts.show()
        
class JudgePortal(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('judgeportal.ui', self)
        
        self.Register = self.findChild(QPushButton, 'Register')
        self.CheckLifts = self.findChild(QPushButton, 'CheckLifts')
        
        self.Register.clicked.connect(self.register)
        self.CheckLifts.clicked.connect(self.check_lifts)
        
        
    def register(self):
        self.reg = JudgeEvent()
        self.close()
        self.reg.show()       

    def check_lifts(self):
        self.lifts = JudgeCheckLifts()
        self.close()
        self.lifts.show()
                  
class AccountWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi('createaccount.ui', self)
        
        self.EnterFirstName = self.findChild(QLineEdit, 'EnterFirstName')
        self.EnterLastName = self.findChild(QLineEdit, 'EnterLastName')
        self.EnterContact = self.findChild(QLineEdit, 'EnterContact')
        self.EnterEmail = self.findChild(QLineEdit, 'EnterEmail')
        self.EnterPassword = self.findChild(QLineEdit, 'EnterPassword')
        self.EnterCNIC = self.findChild(QLineEdit, 'EnterCNIC')
        self.EnterGender = self.findChild(QComboBox, 'EnterGender')
        self.EnterCity = self.findChild(QComboBox, 'EnterCity')
        self.ShowButton = self.findChild(QPushButton,'ShowButton')
        self.AthleteButton = self.findChild(QRadioButton, 'AthleteButton')
        self.JudgeButton = self.findChild(QRadioButton, 'JudgeButton')
        self.OKCancelBox = self.findChild(QDialogButtonBox, 'OKCancelBox')
        
        #connect to name checker
        self.EnterFirstName.textChanged.connect(self.firstname_checker)
        self.EnterLastName.textChanged.connect(self.lastname_checker)
        
        # connect to CNIC checker
        self.EnterCNIC.textChanged.connect(self.cnic_check)
        
        # connect to contact input checker
        self.EnterContact.textChanged.connect(self.check_contact_input)
        
        # connect to email format checker
        self.EnterEmail.textChanged.connect(self.email_check)

        # connect to password input checker and make password asteriks and show button
        self.EnterPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.EnterPassword.textChanged.connect(self.check_password_input)
        self.ShowButton.clicked.connect(self.toggle_password_visibility)

        #OKCancel button
        self.OKCancelBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.OKCancelBox.accepted.connect(self.check_and_accept) #user pressed OK
        self.OKCancelBox.rejected.connect(self.go_back) #user pressed Cancel

        # add to combo box
        cities = [
                "Karachi",
                "Lahore",
                "Islamabad",
                "Faisalabad",
                "Rawalpindi",
                "Peshawar",
                "Multan",
                "Quetta",
                "Abbottabad",
                "Abbottabad",
                "Arifwala",
                "Attock",
                "Badin",
                "Bahawalnagar",
                "Bahawalpur",
                "Bannu",
                "Bhakkar",
                "Burewala",
                "Chaman",
                "Chiniot",
                "Chishtian",
                "Dadu",
                "Daska",
                "Dera Ghazi Khan",
                "Dera Ismail Khan",
                "Faisalabad",
                "Ghotki",
                "Gujranwala",
                "Gujrat",
                "Gwadar",
                "Hafizabad",
                "Hangu",
                "Haripur",
                "Hasilpur",
                "Havelian",
                "Hazro",
                "Hub",
                "Islamabad",
                "Jacobabad",
                "Jampur",
                "Jamshoro",
                "Jaranwala",
                "Jatoi",
                "Jhang",
                "Jhelum",
                "Kabirwala",
                "Kahror Pakka",
                "Kamber Ali Khan",
                "Kamoke",
                "Kamra",
                "Kandhkot",
                "Kandiaro",
                "Kanganpur",
                "Karak",
                "Karachi",
                "Kasur",
                "Khairpur",
                "Khairpur Nathan Shah",
                "Khanewal",
                "Kharian",
                "Khuzdar",
                "Khyber",
                "Kohat",
                "Kohlu",
                "Kot Addu",
                "Kotri",
                "Kundian",
                "Larkana",
                "Liaquatpur",
                "Loralai",
                "Mandi Bahauddin",
                "Mardan",
                "Matli",
                "Mian Channu",
                "Mianwali",
                "Mingora",
                "Mirpur Khas",
                "Moradabad",
                "Moro",
                "Multan",
                "Muridke",
                "Murree",
                "Mustafabad",
                "Muzaffarabad",
                "Muzaffargarh",
                "Nankana Sahib",
                "Narowal",
                "Nasirabad",
                "Naudero",
                "Naukot",
                "Nawabshah",
                "Nowshera",
                "Okara",
                "Pakpattan",
                "Pano Aqil",
                "Pasni",
                "Peshawar",
                "Pind Dadan Khan",
                "Pindigheb",
                "Pir Mahal",
                "Quetta",
                "Rajanpur",
                "Rahim Yar Khan",
                "Rawala Kot",
                "Rawalpindi",
                "Risalpur",
                "Rohri",
                "Rustam",
                "Sadiqabad",
                "Sahiwal",
                "Sakrand",
                "Sanghar",
                "Sargodha",
                "Shahdadkot",
                "Shahdadpur",
                "Shakargarh",
                "Sheikhupura",
                "Shikarpur",
                "Shujaabad",
                "Sibi",
                "Sohbatpur",
                "Sukheke",
                "Sukkur",
                "Swabi",
                "Swat",
                "Tandlianwala",
                "Tando Adam",
                "Tando Allahyar",
                "Tando Muhammad Khan",
                "Tank",
                "Thatta",
                "Timargara",
                "Toba Tek Singh",
                "Topi",
                "Turbat",
                "Umarkot",
                "Wah Cantonment",
                "Wazirabad",
                "Yazman",
                "Zhob"]
        self.EnterCity.addItems(cities)

    #name letters checker
    def firstname_checker(self):
        if self.EnterFirstName.text().replace(" ","").isalpha() :
            # int - text is valid/ black 
            self.EnterFirstName.setStyleSheet("color: black;")
        else:
            # not int - text goes red
            self.EnterFirstName.setStyleSheet("color: red;")
        
    #name letters checker
    def lastname_checker(self):
        if self.EnterLastName.text().replace(" ","").isalpha() :
            # int - text is valid/ black 
            self.EnterLastName.setStyleSheet("color: black;")
        else:
            # not int - text goes red
            self.EnterLastName.setStyleSheet("color: red;")
                
    def cnic_check(self):
        cnic = self.EnterCNIC.text()
        pattern = r'^[0-9]{5}-[0-9]{7}-[0-9]{1}+$'
        match = re.match(pattern, cnic)
        if not bool(match):
            self.EnterCNIC.setStyleSheet("color: red;")
        else:      
            self.EnterCNIC.setStyleSheet("color: black;")

    #contact data type checker
    def check_contact_input(self):
        if self.EnterContact.text().isdigit():
            # int - text is valid/ black 
            self.EnterContact.setStyleSheet("color: black;")
        else:
            # not int - text goes red
            self.EnterContact.setStyleSheet("color: red;")
            
    # email format checker
    def email_check(self):
        enteremailtext = self.EnterEmail.text()
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, enteremailtext)
        if not bool(match):
            self.EnterEmail.setStyleSheet("color: red;")
        else:      
            self.EnterEmail.setStyleSheet("color: black;")
            
    def toggle_password_visibility(self):
        # show/back to hidden
        if self.EnterPassword.echoMode() == QLineEdit.EchoMode.Password:
            self.EnterPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.EnterPassword.setEchoMode(QLineEdit.EchoMode.Password)
    
    # conditions for password input
    def check_password_input(self):
        # password conditions
        password = self.EnterPassword.text()
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        is_length_valid = len(password) >= 5

        # red if youre not following conditions
        if has_lower and has_upper and has_digit and is_length_valid:
            self.EnterPassword.setStyleSheet("color: black;")
        else:
            self.EnterPassword.setStyleSheet("color: red;")
            
    # all conditions checked once you click OK. if you click Cancel, you go back to welcome            
    def check_and_accept(self):
        #check enter first name isnt null
        firstnametext = self.EnterFirstName.text()
        if (not firstnametext) or firstnametext.replace(" ","").isalpha() == False:
            QMessageBox.critical(self, "Error", "Please enter your first name. Letters only.")
        else:
            #check enter last name isnt null
            lastnametext = self.EnterLastName.text()
            if (not lastnametext) or lastnametext.replace(" ","").isalpha() == False:
                QMessageBox.critical(self, "Error", "Please enter your last name. Letters only.")
            else:
                # cnic valid
                numcnic = self.EnterCNIC.text()
                if not numcnic or numcnic.replace("-","").isdigit() == False:
                    QMessageBox.critical(self, "Error", "Please enter your CNIC in the format 12345-67891234-5, with dashes.")
                else:
                    #check city
                    selected_city = self.EnterCity.currentText()
                    if selected_city == "Choose Your City of Residence.":
                        # error they chose default
                        QMessageBox.critical(self, "Error", "Please choose your city of residence.")
                    else:
                        selected_gender = self.EnterGender.currentText()
                        if selected_gender == "Choose Your Gender.":
                            # error message they chose default
                            QMessageBox.critical(self, "Error", "Please choose your gender.")
                        else:
                            # checking data type for integer
                            if not self.EnterContact.text().isdigit() or len(self.EnterContact.text()) != 11:
                                # error msg bcs user entered non-integers
                                QMessageBox.critical(self, "Error", "Please enter your 11-digit contact number.")
                            else:
                                #check email isnt null
                                enteremailtext = self.EnterEmail.text()
                                if not enteremailtext:
                                    QMessageBox.critical(self, "Error", "Please enter your email address.")
                                else:
                                    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                                    match = re.match(pattern, enteremailtext)
                                    if not bool(match):
                                        self.EnterEmail.setStyleSheet("color: red;")
                                        QMessageBox.critical(self, "Error", "Please enter a valid email address.")
                                    else:
                                        # valid continue to check password
                                        password = self.EnterPassword.text()
                                        has_lower = any(c.islower() for c in password)
                                        has_upper = any(c.isupper() for c in password)
                                        has_digit = any(c.isdigit() for c in password)
                                        is_length_valid = len(password) >= 5

                                        # error message 
                                        if not (has_lower and has_upper and has_digit and is_length_valid):
                                            error_message = "Please ensure that the password meets the following conditions:\n" \
                                                            "- At least 5 characters long\n" \
                                                            "- Contains both lower and upper case letters\n" \
                                                            "- Contains at least 1 number"
                                            QMessageBox.critical(self, "Error", error_message)
                                        else:
                                            global fname
                                            global lname                    
                                            global email
                                            global contact
                                            global cnic
                                            global pwd
                                            global gender
                                            global city
                                                        

                                            fname = self.EnterFirstName.text()
                                            lname = self.EnterLastName.text()
                                            email = self.EnterEmail.text()
                                            contact = int(self.EnterContact.text())
                                            cnic = self.EnterCNIC.text()
                                            pwd = self.EnterPassword.text()
                                            gender = self.EnterGender.currentText()
                                            city = self.EnterCity.currentText()
                                            # valid check for athlete/judge
                                            if self.AthleteButton.isChecked():
                                                        # AthleteButton is selected
                                                        
                                                        conn= pyodbc.Connection = pyodbc.connect(connection_string)
                                                        csr: pyodbc.Cursor = conn.cursor()
                                                        athlete = '''
                                                            INSERT INTO athlete_details(email, pwd, gender, first_name, last_name,city, cnic, contact_number)
                                                            VALUES 
                                                            (?,?,?,?,?,?,?,?);
                                                        '''
                                                        csr.execute(athlete,email,pwd,gender,fname,lname,city,cnic,contact)
                                                        conn.commit()
                                                        conn.close()
                                                        # self.athlete_portal = AthletePortal()
                                                        # self.close()
                                                        # self.athlete_portal.show()  # Use show() instead of exec_()
                                                        self.login = LoginPortal()
                                                        self.close()
                                                        self.login.show()
                                            elif self.JudgeButton.isChecked():
                                                        # JudgeButton is selected
                                                        conn= pyodbc.Connection = pyodbc.connect(connection_string)
                                                        csr: pyodbc.Cursor = conn.cursor()
                                                        judge = '''
                                                            INSERT INTO judge_details(email, pwd, first_name, last_name, city, cnic, contact_number, gender)
                                                            VALUES 
                                                            (?,?,?,?,?,?,?,?);
                                                        '''
                                                        csr.execute(judge,email,pwd,fname,lname,city,cnic,contact,gender)
                                                        conn.commit()
                                                        conn.close()
                                                        # self.judge_portal = JudgePortal()
                                                        # self.close()
                                                        # self.judge_portal.show()
                                                        self.login = LoginPortal()
                                                        self.close()
                                                        self.login.show()
                                            else:
                                                        print("error")
                                        #self.accept() -- otherwise itll close the app on password error message!!     
                                
         
                 
    def go_back(self):
        # back to welcome
        self.back = WelcomeScreen()
        self.close()
        self.back.show()
   
class AthleteDetailsWindow(QWidget):
    def __init__(self,a_cnic):
        super(). __init__()
        uic.loadUi('athletedetails.ui',self)  
        
        #inputs
        self.BodyWeight = self.findChild(QLineEdit, 'BodyWeight')
        self.NextDetails = self.findChild(QPushButton, 'NextDetails') 
        self.CancelDetails = self.findChild(QPushButton, 'CancelDetails') 
        self.a_cnic = a_cnic
        
        # check bodyweight
        self.BodyWeight.textChanged.connect(self.bodyweight_check)
        
        #if next clicked
        self.NextDetails.clicked.connect(self.check_and_next)
        #if cancel clicked
        self.CancelDetails.clicked.connect(self.go_back)       
            
    def bodyweight_check(self):
        bw = self.BodyWeight.text()
        pattern = r'^\d+(\.\d{2})?$'
        match = re.match(pattern, bw)
        if not bool(match):
            self.BodyWeight.setStyleSheet("color: red;")
        else:      
            self.BodyWeight.setStyleSheet("color: black;")
             
    def check_and_next(self):
        # Provide the  connection string to connect to the lifters database
            
            #valid proceed
                # gender valid, proceed
            bw_type = self.BodyWeight.text()
            #valid data type
            input_pattern = re.compile(r'^\d+\.\d{2}$')
            if not (input_pattern).match(bw_type):
                #error for not rounding to 2 dp
                QMessageBox.critical(self,"Error","Please enter your bodyweight rounded up to 2 decimal places. For example, 86.95 or 120.00")
                        
            else:                    
                #valid BW
                bw = float(self.BodyWeight.text())
                conn= pyodbc.Connection = pyodbc.connect(connection_string)
                csr: pyodbc.Cursor = conn.cursor()
                
                addbw = '''
                        UPDATE athlete_details SET bodyweight = ? WHERE cnic =?;
                        '''
                print(a_cnic)
                csr.execute(addbw,bw,self.a_cnic)
                conn.commit()
                conn.close()
                self.athEVENT = AthleteEvent(self.a_cnic)
                self.close()
                self.athEVENT.show()
                                
    def go_back(self):
        # back to create account
        self.back = AthletePortal()
        self.close()
        self.back.show()
     
class AthleteEvent(QWidget):
    def __init__(self):
        super(). __init__()
        uic.loadUi('athleteevent.ui',self)   
        self.a_cnic = a_cnic
        self.AthleteEventBox = self.findChild(QComboBox, 'AthleteEventBox')
        self.Next = self.findChild(QPushButton, 'Next')
        self.Back = self.findChild(QPushButton, 'Back')     
        
        self.Next.clicked.connect(self.process)
        self.Back.clicked.connect(self.back)
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        
        sql2 = '''
        SELECT event_name FROM event_schedule;
        '''
        csr.execute(sql2)
        names = csr.fetchall()
        for i in names:
            list=(i[0]) 
            self.AthleteEventBox.addItem(list)
        conn.commit()
        conn.close()
    def process(self):
        evname = self.AthleteEventBox.currentText()
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        
        eventid = '''
                SELECT event_id FROM event_schedule WHERE event_name = ?;
                '''
        csr.execute(eventid,evname)
        id = csr.fetchone()[0]
        conn.commit()
        add = '''
                UPDATE lifts SET athleteID = ? WHERE eventID = ?;

            '''
        csr.execute(add, self.a_cnic, id)
        conn.commit()
        conn.close()
    
    def back(self):
        self.quit = AthletePortal(self.a_cnic)
        self.close()
        self.quit.show()
        
class JudgeEvent(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('judgeevent.ui',self)
        
        self.JudgeEventBox = self.findChild(QComboBox, 'JudgeEventBox')
        self.Next = self.findChild(QPushButton, 'Next')
        self.Back = self.findChild(QPushButton, 'Back')  
        
        self.Next.clicked.connect(self.process)
        self.Back.clicked.connect(self.back)
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        
        
        
        sql2 = '''
        SELECT event_name FROM event_schedule;
        '''
        csr.execute(sql2)
        names = csr.fetchall()
        for i in names:
            list=(i[0]) 
            self.JudgeEventBox.addItem(list)
        conn.commit()
        conn.close()
    def process(self):
        evname = self.JudgeEventBox.currentText()
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        
        eventid = '''
                SELECT event_id FROM event_schedule WHERE event_name = ?;
                '''
        csr.execute(eventid,evname)
        iid = csr.fetchone()[0]
        conn.commit()
        add = '''
                UPDATE event_schedule SET judge_ID = ? WHERE event_id = ?;
                (?,?)
            '''
        csr.execute(add,j_cnic,iid)
        conn.commit()
        conn.close()
    
    def back(self):
        self.quit = JudgePortal()
        self.close()
        self.quit.show()

class AthleteCheckLifts(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('athletechecklifts.ui',self)
        
       #will be done with connectivity
        self.NameBox = self.findChild(QComboBox,'NameBox')
        self.EventBox = self.findChild(QComboBox, 'EventBox')
        self.WeightCat = self.findChild(QLineEdit, 'WeightCat')
        self.Squat = self.findChild(QLineEdit, 'Squat')
        self.Bench = self.findChild(QLineEdit, 'Bench')
        self.Deadlift = self.findChild(QLineEdit, 'Deadlift')
        self.Total = self.findChild(QLineEdit, 'Total')
        self.Points = self.findChild(QLineEdit, 'Points')
        self.ShowLift = self.findChild(QPushButton, 'ShowLift')
        self.Done = self.findChild(QPushButton, 'Done')
        
        self.ShowLift.clicked.connect(self.checker)
        self.Done.clicked.connect(self.go_back)
        # for view events part
        # self.NameBox.currentIndexChanged.connect(self.showevents)
        
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()

        sql_athletes = '''
        SELECT CONCAT(first_name, ' ', last_name) FROM athlete_details;
        '''
        csr.execute(sql_athletes)
        athlete_names = [item[0] for item in csr.fetchall()]
        self.NameBox.addItems(athlete_names)
        
        conn.commit()

        # Fetch and populate event names
        sql_events = '''
        SELECT event_name FROM event_schedule;
        '''
        csr.execute(sql_events)
        event_names = [item[0] for item in csr.fetchall()]
        self.EventBox.addItems(event_names)
        
        conn.commit()
        conn.close()
        
    def checker(self):
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        athname = self.NameBox.currentText()
        evname = self.EventBox.currentText()
        nfirst,nlast = athname.split(maxsplit=1) 
        sql2 = '''
                SELECT cnic FROM athlete_details 
                WHERE  first_name = ? and last_name = ?;
        '''
        csr.execute(sql2, nfirst, nlast)
        athid = csr.fetchone()[0]
        conn.commit()
        
        sql45 = '''
             SELECT event_ID FROM event_schedule WHERE event_name =?;  
        '''
        csr.execute(sql45, evname)
        nmes = csr.fetchone()[0]
        conn.commit()  
        
        s1 = '''
                    SELECT bodyweight, lift_amount FROM athlete_details ad 
                    JOIN lifts l ON ad.cnic = l.athleteID
                    WHERE ad.cnic = ? and l.event_id = ? and l.lift_type = 'squat' and l.lift_num =3;
        '''
        csr.execute(s1,athid,nmes)
        results = csr.fetchall()
        conn.commit()
        
        if results:
            for result in results:
                # (bodyweight, squat3) = result
                bodyweight = results[0][0]
                squat3 = results[0][1]

                # Display the results in the corresponding QLineEdits
                self.WeightCat.setText(str(bodyweight))
                self.Squat.setText(str(squat3))
                
        else: 
            QMessageBox.critical(self, "Error", "Please exisitng athlete and database")

        
        s2 = '''
            SELECT lift_amount FROM lifts l
                    WHERE l.athleteID = ? and l.lift_type = 'bench' and l.lift_num =3;
        '''        
        csr.execute(s2,athid)
        benchnum = csr.fetchall()
        conn.commit()
        for b in benchnum:
            self.Bench.setText(str(b))
        
        s3 = '''
            SELECT lift_amount FROM lifts l
                    WHERE l.athleteID = ? and l.lift_type = 'deadlift' and l.lift_num =3;
        '''        
        csr.execute(s3,athid)
        dl = csr.fetchall()
        conn.commit()
        for d in dl:
            self.Deadlift.setText(str(d))
        
        total = results[0][1]+benchnum[0]+dl[0]
        
        # Calculate the IPF GL score
        ipf_gl_score = (((total) / 3) * (500 / float(results[0][0]))/10)
        # print(ipf_gl_score)
        gl_points = round(ipf_gl_score,2)
        
        self.Total.setText(f'{total:.2f}')
        self.Points.setText(f'{gl_points:.2f}')
            
    def go_back(self):
        self.back = AthletePortal()
        self.close()
        self.back.show()

class JudgeCheckLifts(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('judgechecklifts.ui',self)
        
       #will be done with connectivity
        self.NameBox = self.findChild(QComboBox,'NameBox')
        self.EventBox = self.findChild(QComboBox, 'EventBox')
        self.WeightCat = self.findChild(QLineEdit, 'WeightCat')
        self.Squat = self.findChild(QLineEdit, 'Squat')
        self.Bench = self.findChild(QLineEdit, 'Bench')
        self.Deadlift = self.findChild(QLineEdit, 'Deadlift')
        self.Total = self.findChild(QLineEdit, 'Total')
        self.Points = self.findChild(QLineEdit, 'Points')
        self.ShowLift = self.findChild(QPushButton, 'ShowLift')
        self.Done = self.findChild(QPushButton, 'Done')
        
        self.ShowLift.clicked.connect(self.checker)
        self.Done.clicked.connect(self.go_back)
        # for view events part
        # self.NameBox.currentIndexChanged.connect(self.showevents)
        
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()

        sql_athletes = '''
        SELECT CONCAT(first_name, ' ', last_name) FROM athlete_details;
        '''
        csr.execute(sql_athletes)
        athlete_names = [item[0] for item in csr.fetchall()]
        self.NameBox.addItems(athlete_names)
        
        conn.commit()

        # Fetch and populate event names
        sql_events = '''
        SELECT event_name FROM event_schedule;
        '''
        csr.execute(sql_events)
        event_names = [item[0] for item in csr.fetchall()]
        self.EventBox.addItems(event_names)
        
        conn.commit()
        conn.close()
        
    def checker(self):
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        athname = self.NameBox.currentText()
        evname = self.EventBox.currentText()
        nfirst,nlast = athname.split(maxsplit=1) 
        sql2 = '''
                SELECT cnic FROM athlete_details 
                WHERE  first_name = ? and last_name = ?;
        '''
        csr.execute(sql2, nfirst, nlast)
        athid = csr.fetchone()[0]
        conn.commit()
        
        sql45 = '''
             SELECT event_ID FROM event_schedule WHERE event_name =?;  
        '''
        csr.execute(sql45, evname)
        nmes = csr.fetchone()[0]
        conn.commit()  
        
        s1 = '''
                    SELECT bodyweight, lift_amount FROM athlete_details ad 
                    JOIN lifts l ON ad.cnic = l.athleteID
                    WHERE ad.cnic = ? and l.event_id = ? and l.lift_type = 'squat' and l.lift_num =3;
        '''
        csr.execute(s1,athid,nmes)
        results = csr.fetchall()
        conn.commit()
        
        if results:
            for result in results:
                # (bodyweight, squat3) = result
                bodyweight = results[0][0]
                squat3 = results[0][1]

                # Display the results in the corresponding QLineEdits
                self.WeightCat.setText(str(bodyweight))
                self.Squat.setText(str(squat3))
        
        s2 = '''
            SELECT lift_amount FROM lifts l
                    WHERE l.athleteID = ? and l.lift_type = 'bench' and l.lift_num =3;
        '''        
        csr.execute(s2,athid)
        benchnum = csr.fetchall()
        conn.commit()
        for b in benchnum:
            self.Bench.setText(str(b))
        
        s3 = '''
            SELECT lift_amount FROM lifts l
                    WHERE l.athleteID = ? and l.lift_type = 'deadlift' and l.lift_num =3;
        '''        
        csr.execute(s3,athid)
        dl = csr.fetchall()
        conn.commit()
        for d in dl:
            self.Deadlift.setText(str(d))
        
        total = results[0][1]+benchnum[0]+dl[0]
        
        # Calculate the IPF GL score
        ipf_gl_score = (((total) / 3) * (500 / float(results[0][0]))/10)
        # print(ipf_gl_score)
        gl_points = round(ipf_gl_score,2)
        
        self.Total.setText(f'{total:.2f}')
        self.Points.setText(f'{gl_points:.2f}')
        
    def go_back(self):
        self.back = JudgePortal()
        self.close()
        self.back.show()

class AdminLiftWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('adminchecklifts.ui',self)
        
        #will be done with connectivity
        self.NameBox = self.findChild(QComboBox,'NameBox')
        self.EventBox = self.findChild(QComboBox, 'EventBox')
        self.WeightCat = self.findChild(QLineEdit, 'WeightCat')
        self.Squat = self.findChild(QLineEdit, 'Squat')
        self.Bench = self.findChild(QLineEdit, 'Bench')
        self.Deadlift = self.findChild(QLineEdit, 'Deadlift')
        self.Total = self.findChild(QLineEdit, 'Total')
        self.Points = self.findChild(QLineEdit, 'Points')
        self.ShowLift = self.findChild(QPushButton, 'ShowLift')
        self.Done = self.findChild(QPushButton, 'Done')
        
        self.ShowLift.clicked.connect(self.checker)
        self.Done.clicked.connect(self.go_back)
        # for view events part
        # self.NameBox.currentIndexChanged.connect(self.showevents)
        
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()

        sql_athletes = '''
        SELECT CONCAT(first_name, ' ', last_name) FROM athlete_details;
        '''
        csr.execute(sql_athletes)
        athlete_names = [item[0] for item in csr.fetchall()]
        self.NameBox.addItems(athlete_names)
        
        conn.commit()

        # Fetch and populate event names
        sql_events = '''
        SELECT event_name FROM event_schedule;
        '''
        csr.execute(sql_events)
        event_names = [item[0] for item in csr.fetchall()]
        self.EventBox.addItems(event_names)
        
        conn.commit()
        conn.close()
        
    def checker(self):
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        athname = self.NameBox.currentText()
        evname = self.EventBox.currentText()
        nfirst,nlast = athname.split(maxsplit=1) 
        sql2 = '''
                SELECT cnic FROM athlete_details 
                WHERE  first_name = ? and last_name = ?;
        '''
        csr.execute(sql2, nfirst, nlast)
        athid = csr.fetchone()[0]
        conn.commit()
        
        sql45 = '''
             SELECT event_ID FROM event_schedule WHERE event_name =?;  
        '''
        csr.execute(sql45, evname)
        nmes = csr.fetchone()[0]
        conn.commit()  
        
        s1 = '''
                    SELECT bodyweight, lift_amount FROM athlete_details ad 
                    JOIN lifts l ON ad.cnic = l.athleteID
                    WHERE ad.cnic = ? and l.event_id = ? and l.lift_type = 'squat' and l.lift_num =3;
        '''
        csr.execute(s1,athid,nmes)
        results = csr.fetchone()
        conn.commit()
        
        # if results:
        #     for result in results:
        #         # (bodyweight, squat3) = result
        #         bodyweight = results[0][0]
        #         squat3 = results[0][1]

                # Display the results in the corresponding QLineEdits
        self.WeightCat.setText(str(results[0]))
        self.Squat.setText(str(results[1]))
        
        s2 = '''
            SELECT lift_amount FROM lifts l
                    WHERE l.athleteID = ? and l.lift_type = 'bench' and l.lift_num =3;
        '''        
        csr.execute(s2,athid)
        benchnum = csr.fetchone()[0]
        conn.commit()
        self.Bench.setText(str(benchnum))
        
        s3 = '''
            SELECT lift_amount FROM lifts l
                    WHERE l.athleteID = ? and l.lift_type = 'deadlift' and l.lift_num =3;
        '''        
        csr.execute(s3,athid)
        dl = csr.fetchone()[0]
        conn.commit()
        self.Deadlift.setText(str(dl))
        
        total = results[1]+benchnum+dl
        
        # Calculate the IPF GL score
        ipf_gl_score = (((total) / 3) * (500 / float(results[0]))/10)
        # print(ipf_gl_score)
        gl_points = round(ipf_gl_score,2)
        
        self.Total.setText(f'{total:.2f}')
        self.Points.setText(f'{gl_points:.2f}')
            
    def go_back(self):
        self.back = AdminWindow()
        self.close()
        self.back.show()

class AthleteDisplayInfo(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('athletedisplayinfo.ui',self)
        
        self.nameDisplay = self.findChild(QLineEdit, 'nameDisplay')
        self.contactDisplay = self.findChild(QLineEdit, 'contactDisplay')
        self.genderDisplay = self.findChild(QLineEdit, 'genderDisplay')
        self.cnicDisplay = self.findChild(QLineEdit, 'cnicDisplay')
        self.EditDetails = self.findChild(QPushButton, 'EditDetails')
        self.ConfirmDetails = self.findChild(QPushButton, 'ConfirmDetails')
        
        #done confirmed
        self.ConfirmDetails.clicked.connect(self.last_screen)
        
        #edit needed - restart 
        self.EditDetails.clicked.connect(self.back)
        
    def last_screen(self):
        self.thanks = AthleteThankYou()
        self.close()
        self.thanks.show()
        
    def back(self):
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        sql90 = '''DELETE FROM athlete_details WHERE cnic = ?;'''
        csr.execute(sql90,a_cnic)
        conn.commit()
        # sql92 = '''UPDATE participants SET athleteID = NULL WHERE athleteID =? '''
        # csr.execute(sql92, a_cnic)
        # conn.commit()
        sql34 = '''DELETE FROM lifts  WHERE athleteID =?;'''
        csr.execute(sql34,a_cnic)
        conn.commit()
        conn.close()
        self.edit = AthletePortal()
        self.close()
        self.edit.show()  
              
class JudgeDisplayInfo(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('judgedisplayinfo.ui', self)
        
        self.nameDisplay = self.findChild(QLineEdit, 'nameDisplay')
        self.contactDisplay = self.findChild(QLineEdit, 'contactDisplay')
        self.cnicDisplay = self.findChild(QLineEdit, 'cnicDisplay')
        self.genderDisplay = self.findChild(QLineEdit, 'genderDisplay')
        self.EditDetails = self.findChild(QPushButton, 'EditDetails')
        self.ConfirmDetails = self.findChild(QPushButton, 'ConfirmDetails')
        
        #done confirmed
        self.ConfirmDetails.clicked.connect(self.last_screen)
        
        #edit needed - restart 
        self.EditDetails.clicked.connect(self.back)
        
        fullname = fname+" "+lname
        self.nameDisplay.setText(fullname)
        self.contactDisplay.setText(str(contact))
        self.cnicDisplay.setText(str(cnic))
        self.genderDisplay.setText(gender)
        
    def last_screen(self):
        self.thanks = JudgeThankYou()
        self.close()
        self.thanks.show()
        
    def back(self): 
        conn= pyodbc.Connection = pyodbc.connect(connection_string)
        csr: pyodbc.Cursor = conn.cursor()
        sql32 = '''DELETE FROM judge_details WHERE cnic = ?;'''
        csr.execute(sql32,j_cnic)
        conn.commit()
        # sql33 = '''UPDATE participants SET judgeID = NULL WHERE judgeID =? '''
        # csr.execute(sql33, j_cnic)
        # conn.commit()
        sql34 = '''UPDATE event_schedule SET judge_ID = NULL WHERE judge_ID =?;'''
        csr.execute(sql34,j_cnic)
        conn.commit()
        conn.close()
        self.edit = JudgePortal()
        self.close()
        self.edit.show()  
          
class AthleteThankYou(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('athletethankyou.ui', self)
        
        self.CloseButton = self.findChild(QPushButton, 'CloseButton')
        self.CheckLift = self.findChild(QPushButton, 'CheckLift')
        
        self.CloseButton.clicked.connect(self.end)
        self.Back.clicked.connect(self.checker)
        
    def end(self):
        self.close()
        
    def checker(self):
        self.back = AthleteCheckLifts()
        self.close()
        self.back.show()

class JudgeThankYou(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('judgethankyou.ui', self)
        
        self.CloseButton = self.findChild(QPushButton, 'CloseButton')
        self.CheckLift = self.findChild(QPushButton, 'CheckLift')
        
        self.CloseButton.clicked.connect(self.end)
        self.Back.clicked.connect(self.checker)
        
    def end(self):
        self.close()
        
    def checker(self):
        self.back = JudgeCheckLifts()
        self.close()
        self.back.show()
        
if __name__ == '__main__':
    app = QApplication([])
    main_screen = main()
    main_screen.show()
    app.exec()
    
import wx
import gspread
import datetime
passInit = 'buzzisourlogo'
gc = gspread.login('energyclubgatech@gmail.com', passInit)
sh = gc.open("Membership Tracking")
worksheet = sh.sheet1
list_of_lists = worksheet.get_all_values()
# print list_of_lists
global gtidList
gtidList = worksheet.col_values(2)
global nameList
nameList = worksheet.col_values(3)
username = ""


class MemberPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Image
        # image = wx.Image(self,'EClogo.jpg', wx.BITMAP_TYPE_JPEG, pos=(20,10), size=(100,100))
        # imageBitmap = wx.StaticBitmap(ExamplePanel, wx.ID_ANY, wx.BitmapFromImage(image))

        self.EClogo = wx.StaticBitmap(self, -1, wx.Bitmap("EClogo.jpg", wx.BITMAP_TYPE_ANY), pos=(50, 10))


        ''' Page 1 '''

        # GTID Box
        self.numLabel = wx.StaticText(self, label="Scan your Buzzcard!", pos=(20,120))
        self.num = wx.TextCtrl(self, value="", pos=(150, 150), size=(140,-1), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.num)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.num)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtEnter, self.num)

        # Event Type Combobox
        self.type = 'Energy Chat'
        self.eventType = ['Energy Chat', 'Lecture Series', 'Tour', 'Expo', 'Other']
        self.eventLabel = wx.StaticText(self, label="What kind of event is this?", pos=(20, 210))
        self.eventBox = wx.ComboBox(self, pos=(150, 240), size=(120, -1), choices=self.eventType, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.eventBox)
        # self.Bind(wx.EVT_TEXT, self.EvtText,self.eventBox)

        # Preferences button
        self.pref = wx.Button(self, label="Preferences", pos=(150, 300))
        self.Bind(wx.EVT_BUTTON, self.Pref1, self.pref)

        ''' Page 2 '''

        # Mailing List CheckBox
        self.checked = False
        self.checkBox = wx.CheckBox(self, -1, label="Do you want to sign up for our mailing list?", pos=(20, 360))
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox,self.checkBox)

        # Submit Button
        self.submit =wx.Button(self, label="Submit", pos=(150, 400))
        self.Bind(wx.EVT_BUTTON, self.Submit1, self.submit)

        # Name Entry
        self.name = wx.TextCtrl(self, value="", pos=(150,150), size=(140,-1))
        self.nameLabel = wx.StaticText(self, label="Enter your name (First and Last):", pos=(20, 120))
        self.Bind(wx.EVT_TEXT, self.NameEntry, self.name)

        # Email Entry
        self.email = wx.TextCtrl(self, value="", pos=(150,230), size=(140,-1))
        self.emailLabel = wx.StaticText(self, label="Enter your email address:", pos=(20,200))
        self.Bind(wx.EVT_TEXT, self.EmailEntry, self.email)
       
        # Major Selection
        self.majorType = "N/A"
        self.majorLabel = wx.StaticText(self, label="Select your major:", pos=(20, 280))
        self.majors = ["N/A", "Aerospace Engineering", "Biomedical Engineering", "Chemical & Biomolecular Engineering", "Civil Engineering",
                        "Computer Engineering", "Electrical Engineering", "Environmental Engineering", "Industrial Engineering",
                        "Materials Science & Engineering", "Mechanical Engineering", "Nuclear & Radiological Engineering"]
        self.majorSel = wx.ComboBox(self, pos=(150, 310), size=(200, -1), choices=self.majors, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.majorEnter, self.majorSel)

        ''' Page 3 '''
        
        # Welcome Message
        username = ""
        self.welcome = wx.StaticText(self, label="Welcome back!", pos=(150, 120))
        self.welcomeName = wx.StaticText(self, label=username, pos=(150,150))

        # Finish Button
        self.finish = wx.Button(self, label="Finish", pos=(150,210))
        self.finish.Bind(wx.EVT_BUTTON, self.Finish, self.finish)

        # Not You? Button
        self.notyou = wx.Button(self, label="Not You?", pos=(150,240))
        self.notyou.Bind(wx.EVT_BUTTON, self.NotYou, self.notyou)

        ''' Page 4 '''

        # Multiple Matches
        self.multi = wx.StaticText(self, label="Multiple Matches Found!", pos=(130,120))

        #Select Your Name
        self.yourname = wx.StaticText(self, label="Select your name", pos=(145, 180))

        # Name Selector
        self.names = ["Kyle Francis", "John Perry", "George P. Burdell"]
        self.nameSel = wx.ComboBox(self, pos=(110, 210), size=(200, -1), choices=self.names, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.Combo4, self.nameSel)

        # Submit
        self.submit2 =wx.Button(self, label="Submit", pos=(150, 270))
        self.Bind(wx.EVT_BUTTON, self.Submit2, self.submit2)

        # None of these are me Button
        self.notyou2 = wx.Button(self, label="None of these are me", pos=(120,320))
        self.notyou2.Bind(wx.EVT_BUTTON, self.NotYou, self.notyou2)

        ''' Page 5 '''

        # Preferences Panel

        # Cancel
        self.cancel =wx.Button(self, label="Cancel", pos=(80, 200))
        self.Bind(wx.EVT_BUTTON, self.Cancel, self.cancel)
        # Submit new pass
        self.subPass =wx.Button(self, label="Submit", pos=(200, 200))
        self.Bind(wx.EVT_BUTTON, self.SubPass, self.subPass)
        # Password entry
        self.newPass = wx.TextCtrl(self, value="", pos=(150,150), size=(140,-1), style=wx.TE_PASSWORD)
        self.passLabel = wx.StaticText(self, label="Enter new password", pos=(20, 120))
        self.Bind(wx.EVT_TEXT, self.passEntry, self.newPass)

        ''' Default Page '''
        self.toPage1(self)

    def EvtComboBox(self, event):
        self.type = event.GetString()
        print "here"

    def Submit1(self,event):
        self.dateRecorder()
        print self.gtid
        worksheet.update_cell(len(gtidList)+1, 2, "'" + str(self.gtid))# GTID
        worksheet.update_cell(len(gtidList)+1, 3, self.nameEnter) # Name
        worksheet.update_cell(len(gtidList)+1, 4, self.emailEnter) # Email Address
        if self.checked:
            worksheet.update_cell(len(gtidList)+1, 5, 'Yes') # Mailing List?
        elif not self.checked:
            worksheet.update_cell(len(gtidList)+1, 5, 'No')
        worksheet.update_cell(len(gtidList)+1, 6, self.majorEnter) # Selected major

        self.toPage1(self)

    def Pref1(self, event):
        self.toPage5(self)

    def passEntry(self,event):
        self.passEnter = event.GetString()

    def Cancel(self, event):
        self.toPage1(self)

    def SubPass(self, event):
        self.toPage1(self)
        self.passInit = self.passEnter

    def Finish(self, event):
        self.dateRecorder()
        self.toPage1(self)
    def Submit2(self, event):
        self.dateRecorder()
        self.toPage1(self)
    def EvtText(self, event):
        # self.logger.AppendText('EvtText: %s\n' % event.GetString())
        self.gtid = event.GetString()
        # pass
    def EvtChar(self, event):
        # self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        # print "char"
        # event.Skip()
        pass
    def EvtCheckBox(self, event):
        self.checked = self.checkBox.GetValue()
        print self.checked

    def EvtEnter(self, event):
        global username
        self.indeces = []
        counter = 0
        self.names = []
        self.gtid = self.gtid[-4:]
        print self.gtid
        for item in gtidList:
            if item == self.gtid:
                self.indeces.append(counter)
            counter += 1
        print self.indeces
        if len(self.indeces) == 1:
            username = nameList[self.indeces[0]]
            self.welcomeName.SetLabel(username)
            print username
            self.toPage3(self)
        elif len(self.indeces) > 1:
            for i in self.indeces:
                self.names.append(nameList[i])
            print self.names
            self.nameSelected = self.names[0]
            self.toPage4(self)
        elif not self.indeces:
            self.toPage2(self)


    def NotYou(self, event):
        self.toPage2(self)
    def NameEntry(self, event):
        self.nameEnter = event.GetString()
    def EmailEntry(self, event):
        self.emailEnter = event.GetString()
    def majorEnter(self, event):
        self.majorEnter = event.GetString()
    def dateRecorder(self):
        if self.type == 'Energy Chat':
            if len(self.indeces) == 1:
                cValue = worksheet.cell(self.indeces[0]+1, 7).value
                worksheet.update_cell(self.indeces[0]+1, 7, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(self.indeces[0]+1, 8).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(self.indeces[0]+1, 8, int(numVal) + 1)
            elif len(self.indeces) > 1:
                idx = nameList.index(self.nameSelected)
                print idx
                cValue = worksheet.cell(idx+1, 7).value
                worksheet.update_cell(idx+1, 7, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(idx+1, 8).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(idx+1, 8, int(numVal) + 1)
            elif len(self.indeces) == 0:
                cValue = worksheet.cell(len(gtidList)+1, 7).value
                worksheet.update_cell(len(gtidList)+1, 7, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(len(gtidList)+1, 8).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(len(gtidList)+1, 8, int(numVal) +1)
        elif self.type == 'Lecture Series':
            if len(self.indeces) == 1:
                cValue = worksheet.cell(self.indeces[0]+1, 9).value
                worksheet.update_cell(self.indeces[0]+1, 9, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(self.indeces[0]+1, 10).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(self.indeces[0]+1, 10, int(numVal) + 1)
            elif len(self.indeces) > 1:
                idx = nameList.index(self.nameSelected)
                print idx
                cValue = worksheet.cell(idx+1, 9).value
                worksheet.update_cell(idx+1, 9, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(idx+1, 10).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(idx+1, 10, int(numVal) + 1)
            elif len(self.indeces) == 0:
                cValue = worksheet.cell(len(gtidList)+1, 9).value
                worksheet.update_cell(len(gtidList)+1, 9, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(len(gtidList)+1, 10).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(len(gtidList)+1, 10, int(numVal) +1)
        elif self.type == 'Tour':
            if len(self.indeces) == 1:
                cValue = worksheet.cell(self.indeces[0]+1, 11).value
                worksheet.update_cell(self.indeces[0]+1, 11, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(self.indeces[0]+1, 12).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(self.indeces[0]+1, 12, int(numVal) + 1)
            elif len(self.indeces) > 1:
                idx = nameList.index(self.nameSelected)
                print idx
                cValue = worksheet.cell(idx+1, 11).value
                worksheet.update_cell(idx+1, 11, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(idx+1, 12).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(idx+1, 12, int(numVal) + 1)
            elif len(self.indeces) == 0:
                cValue = worksheet.cell(len(gtidList)+1, 11).value
                worksheet.update_cell(len(gtidList)+1, 11, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(len(gtidList)+1, 12).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(len(gtidList)+1, 12, int(numVal) +1)
        elif self.type == 'Expo':
            if len(self.indeces) == 1:
                cValue = worksheet.cell(self.indeces[0]+1, 13).value
                worksheet.update_cell(self.indeces[0]+1, 13, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(self.indeces[0]+1, 14).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(self.indeces[0]+1, 14, int(numVal) + 1)
            elif len(self.indeces) > 1:
                idx = nameList.index(self.nameSelected)
                print idx
                cValue = worksheet.cell(idx+1, 13).value
                worksheet.update_cell(idx+1, 13, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(idx+1, 14).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(idx+1, 14, int(numVal) + 1)
            elif len(self.indeces) == 0:
                cValue = worksheet.cell(len(gtidList)+1, 13).value
                worksheet.update_cell(len(gtidList)+1, 13, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(len(gtidList)+1, 14).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(len(gtidList)+1, 14, int(numVal) +1)
        elif self.type == 'Other':
            if len(self.indeces) == 1:
                cValue = worksheet.cell(self.indeces[0]+1, 15).value
                worksheet.update_cell(self.indeces[0]+1, 15, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(self.indeces[0]+1, 16).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(self.indeces[0]+1, 16, int(numVal) + 1)
            elif len(self.indeces) > 1:
                idx = nameList.index(self.nameSelected)
                print idx
                cValue = worksheet.cell(idx+1, 15).value
                worksheet.update_cell(idx+1, 15, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(idx+1, 16).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(idx+1, 16, int(numVal) + 1)
            elif len(self.indeces) == 0:
                cValue = worksheet.cell(len(gtidList)+1, 15).value
                worksheet.update_cell(len(gtidList)+1, 15, cValue + ";" + str(datetime.date.today()))
                numVal = worksheet.cell(len(gtidList)+1, 16).value
                if not numVal:
                    numVal = 0
                worksheet.update_cell(len(gtidList)+1, 16, int(numVal) +1)

    def Combo4(self, event):
        self.nameSelected = event.GetString()
        print "overwriting nameselected"
        print self.nameSelected

    def toPage1(self, event):
        global gtidList
        global nameList

        gtidList = worksheet.col_values(2)
        nameList = worksheet.col_values(3)

        # Page 1
        self.num.Show()
        self.numLabel.Show()
        self.eventBox.Show()
        self.eventLabel.Show()
        self.num.Clear()
        self.majorLabel.Hide()
        self.majorSel.Hide()
        # Page 2
        self.name.Hide()
        self.nameLabel.Hide()
        self.email.Hide()
        self.emailLabel.Hide()
        self.checkBox.Hide()
        self.submit.Hide()
        # Page 3
        self.welcome.Hide()
        self.welcomeName.Hide()
        self.finish.Hide()
        self.notyou.Hide()
        # Page 4
        self.multi.Hide()
        self.yourname.Hide()
        self.nameSel.Hide()
        self.submit2.Hide()
        self.notyou2.Hide()
        # Page 5
        self.pref.Show()
        self.passLabel.Hide()
        self.newPass.Hide()
        self.cancel.Hide()
        self.subPass.Hide()

    def toPage2(self, event):
        # Page 1
        self.num.Hide()
        self.numLabel.Hide()
        self.eventBox.Hide()
        self.eventLabel.Hide()
        self.majorLabel.Show()
        self.majorSel.Show()
        # Page 2
        self.name.Show()
        self.nameLabel.Show()
        self.email.Show()
        self.emailLabel.Show()
        self.checkBox.Show()
        self.submit.Show()
        self.name.Clear()
        self.email.Clear()
        # Page 3
        self.welcome.Hide()
        self.welcomeName.Hide()
        self.finish.Hide()
        self.notyou.Hide()
        # Page 4
        self.multi.Hide()
        self.yourname.Hide()
        self.nameSel.Hide()
        self.submit2.Hide()
        self.notyou2.Hide()
        # Page 5
        self.pref.Hide()
        self.passLabel.Hide()
        self.newPass.Hide()
        self.cancel.Hide()
        self.subPass.Hide()

    def toPage3(self, event):
        # Page 1
        self.num.Hide()
        self.numLabel.Hide()
        self.eventBox.Hide()
        self.eventLabel.Hide()
        self.majorLabel.Hide()
        self.majorSel.Hide()
        # Page 2
        self.name.Hide()
        self.nameLabel.Hide()
        self.email.Hide()
        self.emailLabel.Hide()
        self.checkBox.Hide()
        self.submit.Hide()
        # Page 3
        self.welcome.Show()
        self.welcomeName.Show()
        self.finish.Show()
        self.notyou.Show()
        # Page 4
        self.multi.Hide()
        self.yourname.Hide()
        self.nameSel.Hide()
        self.submit2.Hide()
        self.notyou2.Hide()
        # Page 5
        self.pref.Hide()
        self.passLabel.Hide()
        self.newPass.Hide()
        self.cancel.Hide()
        self.subPass.Hide()

    def toPage4(self, event):
        self.nameSel = wx.ComboBox(self, pos=(110, 210), size=(200, -1), choices=self.names, style=wx.CB_DROPDOWN)

        # Page 1
        self.num.Hide()
        self.numLabel.Hide()
        self.eventBox.Hide()
        self.eventLabel.Hide()
        self.majorLabel.Hide()
        self.majorSel.Hide()
        # Page 2
        self.name.Hide()
        self.nameLabel.Hide()
        self.email.Hide()
        self.emailLabel.Hide()
        self.checkBox.Hide()
        self.submit.Hide()
        # Page 3
        self.welcome.Hide()
        self.welcomeName.Hide()
        self.finish.Hide()
        self.notyou.Hide()
        # Page 4
        self.multi.Show()
        self.yourname.Show()
        self.nameSel.Show()
        self.submit2.Show()
        self.notyou2.Show()
        # Page 5
        self.pref.Hide()
        self.passLabel.Hide()
        self.newPass.Hide()
        self.cancel.Hide()
        self.subPass.Hide()

    def toPage5(self, event):
        # Page 1
        self.num.Hide()
        self.numLabel.Hide()
        self.eventBox.Hide()
        self.eventLabel.Hide()
        self.majorLabel.Hide()
        self.majorSel.Hide()
        # Page 2
        self.name.Hide()
        self.nameLabel.Hide()
        self.email.Hide()
        self.emailLabel.Hide()
        self.checkBox.Hide()
        self.submit.Hide()
        # Page 3
        self.welcome.Hide()
        self.welcomeName.Hide()
        self.finish.Hide()
        self.notyou.Hide()
        # Page 4
        self.multi.Hide()
        self.yourname.Hide()
        self.nameSel.Hide()
        self.submit2.Hide()
        self.notyou2.Hide()
        #Page 5
        self.pref.Hide()
        self.passLabel.Show()
        self.newPass.Show()
        self.cancel.Show()
        self.subPass.Show()


app = wx.App(False)
frame = wx.Frame(None, -1, 'Georgia Tech Energy Club', size=(400,500), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
panel = MemberPanel(frame)
frame.Show()
app.MainLoop()
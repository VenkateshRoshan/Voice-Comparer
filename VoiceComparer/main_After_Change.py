### KIVY libraries
# kivy version - '1.11.1'
# kivy MD version - '2019.0910'
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.spinner import MDSpinner
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty , ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
### ML Model libraries
import os
import mysql.connector
import csv
import python_speech_features as mfcc
from sklearn import preprocessing
import warnings
import librosa
from keras.optimizers import SGD
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import numpy as np
from keras import layers
from keras import models
from keras import optimizers
from keras import regularizers
from keras import losses
from keras.callbacks import ModelCheckpoint,EarlyStopping
import librosa
import librosa.display
from scipy.fftpack import fft,fftfreq
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import IPython.display as ipd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        disabled : True
        NavigationDrawerToolbar:
            title: "Navigation Drawer"
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            id : logged
            text: "LogIn"
            on_press : app.Present_Screen('LogIn')
            on_release: app.root.ids.scr_mngr.current = 'LogIn_Screen'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Home"
            on_press : app.Present_Screen('Home')
            on_release: app.root.ids.scr_mngr.current = 'Home_Screen'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Insert"
            on_press : app.Present_Screen('Insert')
            on_release: app.root.ids.scr_mngr.current = 'Inserting_Screen'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Delete"
            on_press : app.Present_Screen('Delete')
            on_release: app.root.ids.scr_mngr.current = 'Delete_Screen'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Compare"
            on_press : app.Present_Screen('Compare')
            on_release: app.root.ids.scr_mngr.current = 'Compare_Screen'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Add Student"
            on_press : app.Present_Screen('Add Student')
            on_release: app.root.ids.scr_mngr.current = 'Add_Student'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Delete Student"
            on_press : app.Present_Screen('Delete Student')
            on_release: app.root.ids.scr_mngr.current = 'Del_Student'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Themes"
            on_release: app.root.ids.scr_mngr.current = 'Theme'
    BoxLayout:
        orientation: 'vertical'
        sm : scr_mngr
        Toolbar:
            id: toolbar
            title: 'Voice Comparer'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            id: scr_mngr
            Screen :
                name : 'LogIn_Screen'
                BoxLayout :
                    padding : 20
                    orientation : 'vertical'
                    RelativeLayout :
                        size_hint : 1 , 0.3
                        MDLabel:
                            font_style: 'Title'
                            theme_text_color: 'Primary'
                            text: "Voice Comparer"
                            halign: 'center'
                    RelativeLayout :
                        size_hint : 1 , 0.5
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 10
                            MDTextField:
                                id : User
                                hint_text: "Enter UserName"

                            MDTextField:
                                id : Passw
                                hint_text: "Enter Password"
                                password : True

                    RelativeLayout :
                        size_hint : 1 , 0.2
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            MDRaisedButton:
                                text: "LOG IN"
                                on_release : app.LogInCheck(User.text , Passw.text)


            Screen :
                name : 'Home_Screen'
                ScrollView:
                    do_scroll_x: False
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(1500)
                        padding : dp(20)
                        spacing : dp(10)
                        BoxLayout:
                            MDCard :
                                MDLabel :
                                    bold : True
                                    text: "Voice Comparer"
                                    halign: 'center'
                                    theme_text_color : 'Primary'
                        BoxLayout:
                            MDCard :
                                BoxLayout :
                                    orientation : 'vertical'
                                    padding: dp(8)
                                    MDLabel :
                                        text: "Insert"
                                        halign: 'center'
                                        theme_text_color : 'Primary'
                                    MDSeparator :
                                        height : dp(1)
                                    MDLabel :
                                        text : " • Enter Student ID "
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : " • Specify how the speaker related to the attached file"
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : " • Attach File ( *only .wav files )"
                                        theme_text_color : 'Primary'
                        BoxLayout:
                            MDCard :
                                BoxLayout :
                                    orientation : 'vertical'
                                    padding: dp(8)
                                    MDLabel :
                                        bold : True
                                        text: "Delete"
                                        halign: 'center'
                                        theme_text_color : 'Primary'
                                    MDSeparator :
                                        height : dp(1)
                                    MDLabel :
                                        text : " • Enter Student ID and select files that are to be deleted"
                                        theme_text_color : 'Primary'
                        BoxLayout:
                            MDCard :
                                BoxLayout :
                                    orientation : 'vertical'
                                    padding: dp(8)
                                    MDLabel :
                                        bold : True
                                        text: "Compare"
                                        halign: 'center'
                                        theme_text_color : 'Primary'
                                    MDSeparator :
                                        height : dp(1)
                                    MDLabel :
                                        text : " • Enter Student ID "
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : " • Attach audio file which is to compare "
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : " • Attached audio file ( *only .wav files) "
                                        theme_text_color : 'Primary'
                        BoxLayout:
                            MDCard :
                                BoxLayout :
                                    orientation : 'vertical'
                                    padding: dp(8)
                                    MDLabel :
                                        bold : True
                                        text: "Add Student"
                                        halign: 'center'
                                        theme_text_color : 'Primary'
                                    MDSeparator :
                                        height : dp(1)
                                    MDLabel :
                                        text : " • Attach file ( *only .csv accepted) "
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : " The file have to follow this order "
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : "    • (StudentID , Name , Branch , class , section , year of joining- year of ending) "
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : "    • Ex : 317126510001,ABC,CSE,III/IV,A,2017-2021 "
                                        theme_text_color : 'Primary'
                        BoxLayout:
                            MDCard :
                                BoxLayout :
                                    orientation : 'vertical'
                                    padding: dp(8)
                                    MDLabel :
                                        bold : True
                                        text: "Delete Student"
                                        halign: 'center'
                                        theme_text_color : 'Primary'
                                    MDSeparator :
                                        height : dp(1)
                                    MDLabel :
                                        text : " • Enter Student ID / Name / class / Branch / Section / Year of joining and ending "
                                        theme_text_color : 'Primary'
                                    MDLabel :
                                        text : " • search and activate the Student checkbox which you want to remove "
                                        theme_text_color : 'Primary'

            Screen :
                name : 'Inserting_Screen'
                BoxLayout :
                    padding : dp(48)
                    orientation : 'vertical'
                    RelativeLayout :
                        size_hint : 1 , 0.7
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            BoxLayout :
                                orientation : 'vertical'
                                padding : dp(48)
                                spacing : 10
                                MDTextField :
                                    id : StudId_Insert
                                    hint_text : 'Enter Student ID'

                                MDTextField :
                                    id : show_label
                                    hint_text : 'Enter Label ( Father / Mother / Guardian )'
                                BoxLayout :
                                    orientation : 'horizontal'
                                    spacing : 10
                                    MDTextField :
                                        id : Insert_File
                                        hint_text : 'Attach recorded File'
                                        size_hint : .8 , None
                                    MDIconButton :
                                        id : Attach
                                        icon : 'sd'
                                        size_hint : .2 , None
                                        on_release : app.open_FileManager('Inserting_Screen')
                    RelativeLayout :
                        size_hint : 1 , 0.3
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            MDRaisedButton :
                                text : 'Insert'
                                on_release : app.Insert_DB(StudId_Insert.text,Insert_File.text,show_label.text)

            Screen :
                name : 'Delete_Screen'
                BoxLayout :
                    padding : dp(48)
                    orientation : 'vertical'
                    RelativeLayout :
                        size_hint : 1 , 0.3
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            BoxLayout :
                                orientation : 'horizontal'
                                padding : dp(48)
                                spacing : 10
                                MDTextField :
                                    id : SID
                                    hint_text : 'Enter Student ID'
                                    size_hint : .8 , None
                                    required : True
                                MDRaisedButton :
                                    text : 'search'
                                    on_release : app.Del_Sel_Files(SID.text)

                    RelativeLayout :
                        id : rel
                        size_hint : 1 , .5

                    RelativeLayout :
                        size_hint : 1 , 0.2
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            MDRaisedButton :
                                text : 'Delete'
                                on_release : app.Delete_DB(SID.text)

            Screen :
                name : 'Compare_Screen'
                BoxLayout :
                    padding : dp(48)
                    orientation : 'vertical'
                    RelativeLayout :
                        size_hint : 1 , 0.7
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            BoxLayout :
                                orientation : 'vertical'
                                padding : dp(48)
                                spacing : 10
                                MDTextField :
                                    id : StudId_Compare
                                    hint_text : 'Enter Student ID'
                                    required : True
                                BoxLayout :
                                    orientation : 'horizontal'
                                    spacing : 10
                                    MDTextField :
                                        id : Insert_File_Compare
                                        hint_text : 'Attach recorded File'
                                        size_hint : .8 , None
                                    MDIconButton :
                                        id : Attach
                                        icon : 'sd'
                                        size_hint : .2 , None
                                        on_release : app.open_FileManager('Compare_Screen')
                    RelativeLayout :
                        size_hint : 1 , 0.3
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            MDRaisedButton :
                                text : 'Compare'
                                on_release : app.Compare_DB(StudId_Compare.text , Insert_File_Compare.text)

            Screen :
                name : 'Add_Student'
                BoxLayout :
                    orientation : 'vertical'
                    padding : 10
                    RelativeLayout :
                        size_hint : 1 , 0.4
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            BoxLayout :
                                padding : 10
                                orientation : 'horizontal'
                                spacing : 10
                                MDTextField :
                                    id : Insert_Stud
                                    hint_text : 'Attach File'
                                    size_hint : .8 , None
                                MDIconButton :
                                    id : Attach
                                    icon : 'sd'
                                    size_hint : .2 , None
                                    on_release : app.open_FileManager('Add_Student')

                    RelativeLayout :
                        size_hint : 1 , 0.3

                    RelativeLayout :
                        size_hint : 1 , 0.3
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            MDRaisedButton :
                                text : 'ADD'
                                on_release : app.Add_to_DB(Insert_Stud.text)


            Screen :
                name : 'Del_Student'
                BoxLayout :
                    padding : dp(48)
                    orientation : 'vertical'
                    RelativeLayout :
                        size_hint : 1 , 0.3
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            BoxLayout :
                                orientation : 'horizontal'
                                padding : dp(48)
                                spacing : 10
                                MDTextField :
                                    id : Stu_Det
                                    hint_text : 'Enter student ID / Name /sec / Branch / class / year '
                                    size_hint : .8 , None
                                    required : True
                                MDRaisedButton :
                                    text : 'search'
                                    on_release : app.Del_Stud_DB(Stu_Det.text)

                    RelativeLayout :
                        id : rel
                        size_hint : 1 , .5

                    RelativeLayout :
                        size_hint : 1 , 0.2
                        AnchorLayout :
                            anchor_x : 'center'
                            anchor_y : 'center'
                            MDRaisedButton :
                                text : 'Delete'
                                on_release : app.Delete_Student(Stu_Det.text)

            Screen :
                name : 'FileManager'
                BoxLayout :
                    orientation : 'vertical'
                    RelativeLayout :
                        size_hint : 1 , .8
                        FileChooserIconView :
                            id : filechooser
                            multiselect: True


                    BoxLayout :
                        size_hint : 1 , .2
                        orientation : 'horizontal'
                        MDRaisedButton :
                            text : 'Cancel'
                            on_release : app.cancel()
                        MDRaisedButton :
                            id : Load
                            text : 'Load'
                            on_release: app.Load(filechooser.selection)
                            disabled : True if filechooser.selection==[] else False


            Screen:
                name: 'Theme'
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(80)
                    center_y: self.parent.center_y
                    MDRaisedButton:
                        size_hint: None, None
                        size: 3 * dp(48), dp(48)
                        center_x: self.parent.center_x
                        text: 'Change theme'
                        on_release: MDThemePicker().open()
                        opposite_colors: True
                        pos_hint: {'center_x': 0.5}
                    MDLabel:
                        text: "Current: " + app.theme_cls.theme_style + ", " + app.theme_cls.primary_palette
                        theme_text_color: 'Primary'
                        pos_hint: {'center_x': 0.5}
                        halign: 'center'

'''

class KitchenSink(App):
    theme_cls = ThemeManager()
    sm = ObjectProperty(None)
    title = "Voice Comparer"
    previous_screen = ''
    current_screen = ''
    text = ''
    te = ''
    chkref = {}
    Select_Files_To_Del = []
    Selected_Students = []

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        self.theme_cls.theme_style = 'Dark'
        print('Build')
        return main_widget

    def Present_Screen(self,text) :
        self.current_screen = text
        print(self.current_screen)
        self.te = ''
        self.chkref = {}
        self.Select_Files_To_Del = []
        self.Selected_Students = []
        pass

    def LogInCheck(self , _user_ , _pass_) :
        if _user_ == 'a' and _pass_ == '' :
            Snackbar(text="You're LogIn successfully!!!" ).show()
            self.root.ids.scr_mngr.current = 'Home_Screen'
            self.root.ids.nav_drawer.disabled = False
            self.root.ids.logged.disabled = True
        else :
            Snackbar(text="userName or password may be wrong !!!" ).show()
        pass

    def open_FileManager(self , cur) :
        if cur == 'Inserting_Screen' :
            self.root.ids.filechooser.filters = ['*.wav']
            self.root.ids.Load.disabled = True
            self.root.ids.filechooser.multiselect = True

        elif cur == 'Compare_Screen' :
            self.root.ids.filechooser.filters = ['*.wav']
            self.root.ids.Load.disabled = True
            self.root.ids.filechooser.multiselect = False

        else :
            self.root.ids.filechooser.filters = ['*.csv']
            self.root.ids.Load.disabled = True
        self.root.ids.scr_mngr.current = 'FileManager'
        self.previous_screen = cur
        pass

    def Load(self , selection) :
        String = ''
        print(selection)
        print(len(selection))
        j = 0
        for i in selection :
            String += i
            print(i)
            if j == len(selection) - 1 :
                pass
            else :
                String += ','
                j += 1
        if self.previous_screen == 'Inserting_Screen' :
            print(self.previous_screen)
            self.root.ids.scr_mngr.current = self.previous_screen
            self.root.ids.Insert_File.text = String
            print(' Files to Insert ' + String)
            selection = ''
            String = ''
        elif self.previous_screen == 'Compare_Screen' :
            print(self.previous_screen)
            self.root.ids.scr_mngr.current = self.previous_screen
            self.root.ids.Insert_File_Compare.text = String
            print(' Files to Compare ' + String)
            selection = ''
            String = ''
        else :
            print(self.previous_screen)
            self.root.ids.scr_mngr.current = self.previous_screen
            self.root.ids.Insert_Stud.text = String
            print(' Files to Insert ' + String)
            selection = ''
            String = ''
        pass

    def cancel(self):
        self.root.ids.scr_mngr.current = self.previous_screen
        self.root.ids.Load.disabled = True
        pass

    def Add_to_DB(self,text) :
        filename = text
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        #my.execute('create database Voice_Comparer')
        my.execute('use Voice_Comparer')
        try :
            with open(filename) as csvfile:
                ader = csv.reader(csvfile)
                a = 0
                for row in ader:
                    # Inserting into database
                    sql = 'Insert into student values (%s , %s , %s , %s , %s , %s)'
                    values = (row[0] , row[1] , row[2] , row[3] , row[4] , row[5],)
                    sql_ = 'select * from student where StudentID = %s'
                    k = 1
                    my.execute(sql_ , (row[0] ,))
                    myresult = my.fetchall()
                    a += 1
                    if len(myresult) > 0 :
                        k = 0
                    else:
                        k = 1
                    if k == 1 :
                        my.execute(sql , values)
                        print('This record %d is inserted' % a)
                        db.commit()
                    else :
                        print('This record %d is already inserted' % a)
                    print(my.rowcount, "record inserted.")
                    my.execute('select count(*) from student')
                    res = my.fetchone()
                Snackbar(text='Data Added to DataBase').show()
                print('%d rows Presented in The student table ' % res)
        except :
            Snackbar(text='File Not Found').show()
        pass

    def Checking(self,chkbox,value) :
        if self.current_screen == 'Delete' :
            if value :
                self.te += str(self.chkref[chkbox])
                self.Select_Files_To_Del.append(self.te)
            else :
                self.Select_Files_To_Del.remove(str(self.chkref[chkbox]))
            print(self.Select_Files_To_Del, ' selected')

        elif self.current_screen == 'Delete Student' :
            if value :
                self.te += str(self.chkref[chkbox])
                self.Selected_Students.append(self.te)
            else :
                self.Selected_Students.remove(str(self.chkref[chkbox]))
            print(self.Selected_Students, ' selected')
        self.te = ''

    def Del_Sel_Files(self , StudId) :
        self.te = ''
        self.chkref = {}
        self.Select_Files_To_Del = []
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        my.execute('use Voice_Comparer')
        sql = 'select * from Student_Data_By_Path where StudentId = %s'
        val = (StudId,)
        my.execute(sql,val)
        res = my.fetchall()
        print(len(res))
        inner = ScrollView(size_hint=(1, 1),pos_hint={'center_x': 0, 'center_y': .5})
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None,padding=dp(10))
        grid.bind(minimum_height=grid.setter('height'))
        if len(res) > 0 :
            for row in res :
                print(row[1])
                b = BoxLayout(orientation='horizontal', size_hint=(1,None))
                checkbox = MDCheckbox()
                checkbox.bind(active = self.Checking)
                self.chkref[checkbox] = row[1]
                label = MDLabel(text = row[1])
                b.add_widget(label)
                b.add_widget(checkbox)
                grid.add_widget(b)
            inner.add_widget(grid)
        else :
            inner.add_widget(MDLabel(text='There is no files Here!!!'))
            pass
        popup = Popup(  title='Select Files',
                        size_hint=(1,.8),
                        content=inner,
                        auto_dismiss=True)
        popup.open()

    def Insert_DB(self,StudId,File,show_label):
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        my.execute('use Voice_Comparer')
        sql = 'select count(*) from student where StudentId = %s'
        val = (StudId,)
        my.execute(sql,val)
        res = my.fetchall()
        print(File)
        if res[0][0] == 1 :
            Files = list(File.split(","))
            for i in Files :
                if i.endswith('.wav') :
                    sql = 'Insert into Student_Data_By_Path values (%s , %s , %s)'
                    val = (StudId,i,show_label,)
                    my.execute(sql,val,)
                    db.commit()
                    print(i + ' Inserted')
                else :
                    print('Sorry!!! only .wav files accepted')
            Snackbar('Inserted ').show()
            self.root.ids.scr_mngr.current = 'Inserting_Screen'
        else :
            Snackbar('student not exist').show()
        sql = 'select * from Student_Data_By_Path where StudentId = %s'
        val = (StudId,)
        my.execute(sql,val)
        res = my.fetchall()
        for i in res :
            print(i[0])
            print(i[1])
            print(i[2])
        pass

    def Delete_DB(self,StudId):
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        my.execute('use Voice_Comparer')
        print(self.Select_Files_To_Del)
        for i in self.Select_Files_To_Del :
            sql = 'delete from Student_Data_By_Path where File = %s '
            val = (i,)
            my.execute(sql,val,)
            db.commit()
            Snackbar(text='Files Deleted').show()
            print(i+' Deleted')
        pass

    def Del_Stud_DB(self,text) :
        self.te = ''
        self.chkref = {}
        self.Selected_Students = []
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        my.execute('use Voice_Comparer')
        sql = 'select * from student where StudentId = %s or name = %s or Branch = %s or class = %s or sec = %s or year = %s'
        print(type(text))
        val = (text,text,text,text,text,text,)
        my.execute(sql,val,)
        res = my.fetchall()
        print(len(res))
        inner = ScrollView(size_hint=(1, 1),pos_hint={'center_x': 0, 'center_y': .5})
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None,padding=dp(10))
        grid.bind(minimum_height=grid.setter('height'))
        if len(res) > 0 :
            for row in res :
                string = str(row[0]) + ' ' + row[1] + ' ' + row[2]+ ' ' + row[3]+ ' ' + row[4]+ ' ' + str(row[5])
                print(string)
                b = BoxLayout(orientation='horizontal',size_hint=(1,None))
                checkbox = MDCheckbox()
                checkbox.bind(active = self.Checking)
                self.chkref[checkbox] = row[0]
                label = MDLabel(text = string)
                b.add_widget(label)
                b.add_widget(checkbox)
                grid.add_widget(b)
            inner.add_widget(grid)
        else :
            inner.add_widget(MDLabel(text='There is no Students Here!!!'))
            pass
        popup = Popup(  title='Select Files',
                        size_hint=(1,.8),
                        content=inner,
                        auto_dismiss=True)
        popup.open()

    def Delete_Student(self,text) :
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        my.execute('use Voice_Comparer')
        print(self.Selected_Students)
        for i in self.Selected_Students :
            sql = 'delete from Student_Data_By_Path where StudentID = %s '
            val = (i,)
            my.execute(sql,val,)
            db.commit()
            sql = 'delete from student where StudentID = %s '
            val = (i,)
            my.execute(sql,val,)
            db.commit()
            sql = 'select * from student '
            my.execute(sql,)
            res = my.fetchall()
            for j in res :
                print(j)
        pass

    def Compare_DB(self,StudId,File) :
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        my.execute('use Voice_Comparer')
        sql = 'select * from Student_Data_By_Path where StudentId = %s'
        val = (StudId,)
        my.execute(sql,val,)
        res = my.fetchall()
        if len(res) > 0 :
            self.Compare_Res(StudId,File)
        else :
            print('Please Enter the Student ID correctly...')
            inner = ScrollView(size_hint=(1, 1),pos_hint={'center_x': 0, 'center_y': .5})
            inner.add_widget(MDLabel(text='There is No Files here!!!'))
            popup = Popup(  title='Select Files',
                            size_hint=(.8,.8),
                            content=inner,
                            auto_dismiss=True)

        pass

    def get_MFCC(self,i,sr,audio):
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfccs_processed = np.mean(mfccs.T,axis=0)
        print(i,' - ',mfccs)
        return mfccs_processed

    def Compare_Res(self,StudId,Test_File) :
        db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')
        my = db.cursor()
        my.execute('use Voice_Comparer')
        content = BoxLayout(orientation='vertical',padding=20,size_hint=(1,1))
        sql = 'select * from Student_Data_By_Path where StudentID = %s'
        val = (StudId,)
        path = []
        Label = []
        my.execute(sql,val,)
        res = my.fetchall()
        print('Loading Data : ======>>>>>')
        for i in res :
            path.append(i[1])
            #print(i[1],' - ',i[2])
            Label.append(i[2])
        set_Labels = set(Label)
        set_Labels = list(set_Labels)
        Train_audio = []
        Train_label = []
        epochs = 50
        num_labels = len(set_Labels)
        Match_Perc = 85
        for i in path :
            data , sr = librosa.load(i,res_type='kaiser_best')
            Train_audio.append(self.get_MFCC(i,sr,data))
        for i in Label :
            index = set_Labels.index(i)
            Train_label.append(index)
        self.num_labels = len(set_Labels)
        Train_audio = np.array(Train_audio,)
        Train_label = np.array(Train_label,dtype=np.int)
        print('Model Preparing : =====>>>>>')
        model = Sequential()
        activation_fn = 'glorot_normal'
        model.add(layers.Dense(256,input_shape=Train_audio[0].shape,activation='tanh'))
        model.add(Dropout(.3))
        model.add(layers.Dense(64,activation='tanh'))
        model.add(Dropout(.3))
        model.add(layers.Dense(num_labels,init=activation_fn))
        model.add(Activation('softmax'))
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=sgd,
                      metrics=['accuracy'])
        model.summary()
        history = model.fit(Train_audio,Train_label,epochs=epochs,validation_split=.1)
        print(history.history.keys())
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        audio = []
        Files = list(Test_File.split(","))
        Test_File = Files[0]
        print(Test_File)
        try :
            data , sr = librosa.core.load(Test_File,res_type='kaiser_best')
            audio.append(self.get_MFCC(Test_File,sr,data))
            audio = np.array(audio)
            pred = model.predict(audio)
            print("Predicted Result : ")
            print(" ==>> " + str(pred) , ' - ' , str(pred.argmax(-1)) , set_Labels[pred.argmax(axis=-1)[0]] )
            c = 0
            res = 1
            res_Label = ''
            for i in pred[0] :
                string = set_Labels[c] + "'s Mataching - " + str(i*100) + '%'
                print(string)
                if i*100 > res :
                    res = i*100
                    res_Label = set_Labels[c]
                c += 1
                content.add_widget(MDLabel(text=string , theme_text_color='Primary'))
            if res > Match_Perc :
                content.add_widget(MDLabel(text=' • It is not a fake call It Matches with ' + res_Label + ' voice', theme_text_color='Primary'))
            else :
                content.add_widget(MDLabel(text=' • It is a fake call It is not matching with any voice', theme_text_color='Primary'))
        except :
            if Test_File.endswith('.wav') :
                content.add_widget(MDLabel(text='Inserted File is not readable'))
            else :
                content.add_widget(MDLabel(text=' • The File format is not acceptable .wav only acceptable '))
        popup = Popup(  title='Percentage of matching ',
                        size_hint=(.8,.5),
                        content=content)
        popup.open()

if __name__ == '__main__':
    KitchenSink().run()

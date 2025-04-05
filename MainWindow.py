import datetime
import imp
import time
import tkinter as tk
from tkinter import Frame, ttk, messagebox
from Keyboard import KeyBoard
from FlikerScreen import flikerWindow
from CFF_FOVEA import CffFovea
from globalvar import pageDisctonary
from globalvar import currentPatientInfo
from globalvar import globaladc
from Splash import Splash
import tkinter.font as tkfont
import os, json
from header import HeaderComponent

# Modernized constants
FONT_MAIN = ("Helvetica Neue", 16)  # Clean, modern sans-serif font
FONT_SECONDARY = ("Helvetica Neue", 14)  # Slightly smaller for buttons
FONT_TIME = ("Helvetica Neue", 18, "bold")  # Larger for time display

class mainWindow:
    def __init__(self, frame):
        self.frame = frame
        self.frame.configure(bg='black')
        self.selectedGen = "M"
        self.selectedEye = "R"
        self.kb = KeyBoard()

        # Variables for radio buttons
        self.gender_var = tk.StringVar(value="Male")
        self.alcohol_var = tk.StringVar(value="No")
        self.smoking_var = tk.StringVar(value="No")
        self.food_var = tk.StringVar(value="Veg")
        self.eye_side_var = tk.StringVar(value="R")
        self.bp_var = tk.StringVar(value="No")
        self.diabetes_var = tk.StringVar(value="No")

    def Load(self):
        # Time label - centered at the top below header
        self.timelabel = tk.Label(self.frame, font=FONT_TIME, bg="black", fg="white")
        self.updateDateTime()
        self.timelabel.place(x=412, y=60, width=200, height=30)  # Centered within 1024 width

        # Header
        self.header = HeaderComponent(
            self.frame,
            "Macular Densitometer                                                                   Patient Info"
        )

        # Setup modern UI
        self.setup_ui()

        # Navigation buttons - bottom center
        def onfw():
            if self.ValidateUserInput():
                self.save_patient_data()
                pageDisctonary['MainScreen'].hide()
                pageDisctonary['CffFovea'].show()

        def onbw():
            pageDisctonary['MainScreen'].hide()
            pageDisctonary['BrkparaFovea'].show()

        fwButton = tk.Button(self.frame, text=">>", font=FONT_SECONDARY, 
                            command=onfw, bg='#28a745', fg='white', bd=0, 
                            activebackground="#218838", width=10)
        bwButton = tk.Button(self.frame, text="<<", font=FONT_SECONDARY, 
                            command=onbw, bg='#28a745', fg='white', bd=0, 
                            activebackground="#218838", width=10)
        bwButton.place(x=412, y=540, width=100, height=40)  # Left of center
        fwButton.place(x=512, y=540, width=100, height=40)  # Right of center

    def setup_ui(self):
        self.main_frame = tk.Frame(self.frame, bg='black')
        self.main_frame.place(x=20, y=100, width=984, height=420)  # Adjusted to fit within 1024x600

        # Create form fields - aligned in two columns
        # Left column
        self.create_text_field("1st Name", 0, 0, "first name")
        self.create_text_field("DOB", 0, 60, "Date of Birth")
        self.create_text_field("Aadhaar", 0, 120, "Aadhaar No")
        self.create_radio_group("Gender", 0, 180, self.gender_var, [("Male", "Male"), ("Female", "Female")])
        self.create_radio_group("Alcohol", 0, 240, self.alcohol_var, [("Yes", "Yes"), ("No", "No")])
        self.create_radio_group("Smoking", 0, 300, self.smoking_var, [("Yes", "Yes"), ("No", "No")])
        self.create_radio_group("Food Habit", 0, 360, self.food_var, [("Veg", "Veg"), ("Non-Veg", "Non-Veg")])

        # Right column
        self.create_text_field("Mid. Name", 492, 0, "Middle Name")
        self.create_text_field("Surname", 492, 60, "Surname")
        self.create_text_field("Mobile", 492, 120, "+91XXXXXXXXXX")
        self.create_text_field("Nationality", 492, 180, "Enter Nationality")
        self.create_radio_group("Eye Side", 492, 240, self.eye_side_var, [("R", "R"), ("L", "L")])
        self.create_medical_field("Blood Pressure", 492, 300, self.bp_var, "80/120")
        self.create_medical_field("Diabetes", 492, 360, self.diabetes_var, "97")

    def create_text_field(self, label_text, x, y, placeholder):
        label = tk.Label(self.main_frame, text=label_text, font=FONT_MAIN, bg='black', fg='white')
        label.place(x=x, y=y, width=140, height=30)
        entry = tk.Entry(self.main_frame, font=FONT_SECONDARY, bg='#334155', fg='#94a3b8', 
                        insertbackground='white', bd=0, highlightthickness=1, highlightcolor='#42A5F5')
        entry.place(x=x+140, y=y, width=352, height=30)  # Wider entries for consistency
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(entry, placeholder))
        entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(entry, placeholder))
        setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)

    def create_radio_group(self, label_text, x, y, variable, options):
        label = tk.Label(self.main_frame, text=label_text, font=FONT_MAIN, bg='black', fg='white')
        label.place(x=x, y=y, width=140, height=30)
        for i, (value, text) in enumerate(options):
            rb = tk.Radiobutton(self.main_frame, text=text, variable=variable, value=value, 
                               font=FONT_SECONDARY, bg='black', fg='white', selectcolor='black', 
                               activebackground='black', activeforeground='white', 
                               highlightthickness=0, highlightbackground='black', highlightcolor='black')
            rb.place(x=x+140+(i*100), y=y, width=80, height=30)

    def create_medical_field(self, label_text, x, y, variable, placeholder):
        label = tk.Label(self.main_frame, text=label_text, font=FONT_MAIN, bg='black', fg='white')
        label.place(x=x, y=y, width=140, height=30)
        tk.Radiobutton(self.main_frame, text="Yes", variable=variable, value="Yes", 
                      font=FONT_SECONDARY, bg='black', fg='white', selectcolor='black', 
                      activebackground='black', activeforeground='white', highlightthickness=0).place(x=x+140, y=y, width=60, height=30)
        tk.Radiobutton(self.main_frame, text="No", variable=variable, value="No", 
                      font=FONT_SECONDARY, bg='black', fg='white', selectcolor='black', 
                      activebackground='black', activeforeground='white', highlightthickness=0).place(x=x+200, y=y, width=60, height=30)
        entry = tk.Entry(self.main_frame, font=FONT_SECONDARY, bg='#334155', fg='#94a3b8', 
                        insertbackground='white', bd=0, highlightthickness=1, highlightcolor='#42A5F5')
        entry.place(x=x+260, y=y, width=232, height=30)  # Adjusted width to fit right column
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(entry, placeholder))
        entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(entry, placeholder))
        setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)

    def on_button_hover(self, event, button):
        button.configure(bg='#42A5F5', fg='white')

    def on_button_leave(self, event, button):
        button.configure(bg='#1f2836', fg='white')

    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='white')
        self.kb.createAlphaKey(self.frame, entry)

    def on_entry_focus_out(self, entry, placeholder):
        focused = self.frame.focus_get()
        if not (self.kb.current_window and focused and 
                (focused == self.kb.current_window or focused.winfo_toplevel() == self.kb.current_window)):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg='#94a3b8')
            self.frame.after(200, self.check_focus_and_cleanup, entry)

    def check_focus_and_cleanup(self, original_entry):
        focused = self.frame.focus_get()
        if (focused != original_entry and 
            not (self.kb.current_window and focused and 
                 (focused == self.kb.current_window or focused.winfo_toplevel() == self.kb.current_window))):
            pass  # Add cleanup logic if needed

    def save_patient_data(self, show_message=True):
        try:
            dob_raw = self.get_entry_value("dob", "_entry")
            dob_obj = datetime.datetime.strptime(dob_raw, "%d-%m-%Y")
            dob_formatted = dob_obj.strftime("%Y-%m-%d")
            patient_data = {
                "first_name": self.get_entry_value("1st", "_name_entry"),
                "middle_name": self.get_entry_value("mid", "_name_entry"),
                "surname": self.get_entry_value("surname", "_entry"),
                "dob": dob_formatted,
                "aadhaar": self.get_entry_value("aadhaar", "_entry"),
                "mobile": self.get_entry_value("mobile", "_entry"),
                "nationality": self.get_entry_value("nationality", "_entry"),
                "gender": self.gender_var.get(),
                "alcohol": self.alcohol_var.get(),
                "smoking": self.smoking_var.get(),
                "food_habit": self.food_var.get(),
                "bp": {"has_bp": self.bp_var.get(), "value": self.get_entry_value("blood_pressure", "_entry")},
                "diabetes": {"has_diabetes": self.diabetes_var.get(), "value": self.get_entry_value("diabetes", "_entry")},
                "eye_side": self.eye_side_var.get(),
                "is_sync": False,
                "handler_id": 0,
                "CFF_F": '', "CFF_P": '', "f_mpod": '', "f-sd": '',
                "date": self.timelabel.cget("text")
            }
            current_login_usr = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_data", "latest_user.json")
            with open(current_login_usr, 'r') as f:
                user_data = json.load(f)
            patient_data['handler_id'] = user_data['user_id']
            filename = "patient_latest.json"
            filepath = os.path.join(os.path.dirname(filepath), "patient_data", filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(patient_data, f, indent=4)
            if show_message:
                messagebox.showinfo("Success", "Patient data saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving patient data: {str(e)}")
            return False

    def get_entry_value(self, prefix, suffix):
        attribute_name = f"{prefix}{suffix}"
        entry_widget = getattr(self, attribute_name, None)
        if entry_widget is None:
            return ""
        value = entry_widget.get()
        if value in ["first name", "Middle Name", "Surname", "Date of Birth", "Aadhaar No", "+91XXXXXXXXXX", "80/120", "97", "Enter Nationality"]:
            return ""
        return value

    def update_current_patient_info(self):
        currentPatientInfo.Name = f"{self.get_entry_value('1st', '_name_entry')} {self.get_entry_value('mid', '_name_entry')} {self.get_entry_value('surname', '_entry')}"
        currentPatientInfo.Age = self.get_entry_value('dob', '_entry')
        currentPatientInfo.Eye = self.eye_side_var.get()
        currentPatientInfo.Gender = "M" if self.gender_var.get() == "Male" else "F"
        currentPatientInfo.Nationality = self.get_entry_value('nationality', '_entry')
        currentPatientInfo.Aadhaar = self.get_entry_value('aadhaar', '_entry')
        currentPatientInfo.Mobile = self.get_entry_value('mobile', '_entry')
        currentPatientInfo.Alcohol = self.alcohol_var.get() == "Yes"
        currentPatientInfo.Smoking = self.smoking_var.get() == "Yes"
        currentPatientInfo.FoodHabit = self.food_var.get()
        currentPatientInfo.BP = {"has_bp": self.bp_var.get() == "Yes", "value": self.get_entry_value("blood_pressure", "_entry")}
        currentPatientInfo.Diabetes = {"has_diabetes": self.diabetes_var.get() == "Yes", "value": self.get_entry_value("diabetes", "_entry")}
        currentPatientInfo.date = self.timelabel.cget("text")

    def updateDateTime(self):
        raw_dt = datetime.datetime.now()
        time_now = raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
        self.timelabel.config(text=time_now)
        self.timelabel.after(1000, self.updateDateTime)

    def genderSelected(self):
        self.gender_var.set("Female" if self.gender_var.get() == "Male" else "Male")
        self.selectedGen = "M" if self.gender_var.get() == "Male" else "F"

    def eyeSelected(self):
        self.eye_side_var.set("L" if self.eye_side_var.get() == "R" else "R")
        self.selectedEye = self.eye_side_var.get()

    def show(self):
        self.frame.place(width=1024, height=600)
        globaladc.main_Prepair()

    def hide(self):
        self.frame.place_forget()

    @staticmethod
    def getName():
        return "MainScreen"

    def loadValues(self):
        currentPatientInfo.Name = f"{self.get_entry_value('1st', '_name_entry')} {self.get_entry_value('mid', '_name_entry')} {self.get_entry_value('surname', '_entry')}"
        currentPatientInfo.Age = self.get_entry_value('dob', '_entry')
        currentPatientInfo.eye = self.eye_side_var.get()
        currentPatientInfo.Gender = "M" if self.gender_var.get() == "Male" else "F"
        currentPatientInfo.date = self.timelabel.cget("text")

    def ValidateUserInput(self):
        valid = True
        if not self.get_entry_value('1st', '_name_entry'): valid = False
        if not self.get_entry_value('dob', '_entry'): valid = False
        if not self.eye_side_var.get(): valid = False
        if not self.gender_var.get(): valid = False
        if valid:
            self.loadValues()
        return valid

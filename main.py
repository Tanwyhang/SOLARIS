import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pywinstyles
from PIL import Image, ImageTk
import time
import math
import json
import sys
import os


# importing for todolist
from tkcalendar import Calendar
from datetime import datetime
import json
from tkinter import messagebox


class SettingsManager:
    def __init__(self):
        self.settings_file = "app_settings.json"
        self.default_settings = {
            "theme": "dark",
            "scaling": 1.3,
            "color_theme": "green"
        }
    
    def load_settings(self):
        """Load settings from file or create with defaults if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Ensure all default settings exist
                    for key in self.default_settings:
                        if key not in settings:
                            settings[key] = self.default_settings[key]
                    return settings
            return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self, settings):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False


class SOLARIS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize settings manager
        self.settings_manager = SettingsManager()
        saved_settings = self.settings_manager.load_settings()
        
        # Initialize settings variables
        self.current_theme = saved_settings["theme"]
        self.current_scaling = saved_settings["scaling"]
        self.current_color_theme = saved_settings.get("color_theme", "green")

        self.COLOR_THEMES = {
            "green": {
                1: "#F0F7F0", 2: "#E7F0E7", 3: "#DDE8DD", 4: "#D4E1D4", 
                5: "#CBD9CB", 6: "#C2D2C2", 7: "#B9CDB9", 8: "#B0C7B0",
                9: "#A7C2A7", 10: "#9EBCA0", 11: "#95B69B", 12: "#8CB196",
                13: "#84AC91", 14: "#7BA78C", 15: "#72A387", 16: "#699E83",
                17: "#60987F", 18: "#57937A", 19: "#4E8D75", 20: "#458870",
                21: "#03543c"
            },
            "blue": {
                1: "#F0F4F7", 2: "#E7EDF0", 3: "#DDE5E8", 4: "#D4DEE1", 
                5: "#CBD6D9", 6: "#C2CFD2", 7: "#B9C7CD", 8: "#B0C0C7",
                9: "#A7B9C2", 10: "#9EB2BC", 11: "#95ABB6", 12: "#8CA4B1",
                13: "#849DAC", 14: "#7B96A7", 15: "#728FA2", 16: "#69889D",
                17: "#608198", 18: "#577A93", 19: "#4E738E", 20: "#456C89",
                21: "#033c54"
            },
            "purple": {
                1: "#F5F0F7", 2: "#EDE7F0", 3: "#E4DDE8", 4: "#DCD4E1", 
                5: "#D3CBD9", 6: "#CBC2D2", 7: "#C2B9CD", 8: "#BAB0C7",
                9: "#B1A7C2", 10: "#A99EBC", 11: "#A095B6", 12: "#988CB1",
                13: "#8F84AC", 14: "#877BA7", 15: "#7E72A2", 16: "#76699D",
                17: "#6D6098", 18: "#655793", 19: "#5C4E8E", 20: "#544589",
                21: "#3c0354"
            },
            "pink": {
                1: "#F7F0F4", 2: "#F0E7ED", 3: "#E8DDE5", 4: "#E1D4DE", 
                5: "#D9CBD6", 6: "#D2C2CF", 7: "#CDB9C7", 8: "#C7B0C0",
                9: "#C2A7B9", 10: "#BC9EB2", 11: "#B695AB", 12: "#B18CA4",
                13: "#AC849D", 14: "#A77B96", 15: "#A2728F", 16: "#9D6988",
                17: "#986081", 18: "#93577A", 19: "#8E4E73", 20: "#89456C",
                21: "#54033c"
            },
            "red": {
                1: "#F7F0F0", 2: "#F0E7E7", 3: "#E8DDDD", 4: "#E1D4D4", 
                5: "#D9CBCB", 6: "#D2C2C2", 7: "#CDB9B9", 8: "#C7B0B0",
                9: "#C2A7A7", 10: "#BC9E9E", 11: "#B69595", 12: "#B18C8C",
                13: "#AC8484", 14: "#A77B7B", 15: "#A27272", 16: "#9D6969",
                17: "#986060", 18: "#935757", 19: "#8E4E4E", 20: "#894545",
                21: "#540303"
            }
        }

        # assigning structure : self.COLOR_THEMES[self.current_color_theme][19]



        #COLOR SETUP
        self.COLORS = {
            "red": {
                "main": "#dc3545",    # Red - for delete/dangerous actions
                "hover": "#a82835"    # Darker red for hover
            },
            "blue": {
                "main": "#5e71a6",    # Blue-ish - for primary actions
                "hover": "#4d5c87"    # Darker blue for hover
            },
            "green": {
                "main": "#2c8a6e",    # Green - for positive actions
                "hover": "#26755d"    # Darker green for hover
            },
            "purple": {
                "main": "#9679b0",
                "hover": "#765f8a"
            }
        }

        self.grade_colors = {
            "A+": "#5ba05e", "A": "#5ba05e", "A-": "#8ab15c",
            "B+": "#4192d3", "B": "#4192d3", "C": "#daae2c",
            "D": "#de6843", "F": "#d85c53"
    }


        # Window Configuration        
        self.title("SOLARIS - Study & Productivity Hub")
        width = self.winfo_screenwidth()  
        height = self.winfo_screenheight() 
        self.geometry(f"{width}x{height}")


        pywinstyles.apply_style(self, "mica") # window 11 theme 


        ctk.set_default_color_theme("green") 
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_widget_scaling(self.current_scaling)        

        # Show splash screen first
        self.show_splash_screen()
        self.ui_set = False
        # Schedule the main UI setup after splash screen
    
    def get_theme_colors(self, theme="green"):
        theme_colors = {
            "green": [
                # Base Color: #418c65 (Muted green)
                '#ffffff', '#f4faf5', '#e9f5ea', '#dff0e0', '#d4ead6', 
                '#c9e4cc', '#bedfc2', '#b3d9b8', '#a8d3ae', '#9dcea4', 
                '#92c89a', '#87c290', '#7cbc86', '#71b67c', '#418c65',
                
                # Base Color: #2c5e46 (Deep forest green)
                '#ffffff', '#f2f7f4', '#e6efea', '#dae7e0', '#cedfd6', 
                '#c2d7cc', '#b6cfc2', '#aac7b8', '#9ebfae', '#92b7a4', 
                '#86af9a', '#7aa790', 
                
                # Base Color: #134a3f (Dark teal)
                '#ffffff', '#f0f5f4', '#e1ebe9', '#d2e1de', '#c3d7d3', 
                '#b4cdc8', '#a5c3bd', '#96b9b2', '#87afa7', '#78a59c'
            ][::-2],
            
            "blue": [
                # Base Color: #4165A4 (Muted blue)
                '#ffffff', '#f4f6fa', '#e9edf5', '#dfe3f0', '#d4d9ea', 
                '#c9cfe4', '#bec5df', '#b3bbd9', '#a8b1d3', '#9da7ce', 
                '#929dc8', '#8793c2', '#7c89bc', '#717fb6', '#4165A4',
                
                # Base Color: #2C4682 (Deep blue)
                '#ffffff', '#f2f4f7', '#e6e9ef', '#dadee7', '#ced3df', 
                '#c2c8d7', '#b6bdcf', '#aab2c7', '#9ea7bf', '#929cb7', 
                '#8691af', '#7a86a7',
                
                # Base Color: #132C60 (Dark blue)
                '#ffffff', '#f0f2f5', '#e1e5eb', '#d2d8e1', '#c3cbd7', 
                '#b4becd', '#a5b1c3', '#96a4b9', '#8797af', '#788aa5'
            ][::-2],
            
            "purple": [
                # Base Color: #7841A4 (Muted purple)
                '#ffffff', '#f7f4fa', '#efe9f5', '#e7dff0', '#dfd4ea', 
                '#d7c9e4', '#cfbedf', '#c7b3d9', '#bfa8d3', '#b79dce', 
                '#af92c8', '#a787c2', '#9f7cbc', '#9771b6', '#7841A4',
                
                # Base Color: #522C82 (Deep purple)
                '#ffffff', '#f4f2f7', '#e9e6ef', '#dedae7', '#d3cedf', 
                '#c8c2d7', '#bdb6cf', '#b2aac7', '#a79ebf', '#9c92b7', 
                '#9186af', '#867aa7',
                
                # Base Color: #2C1360 (Dark purple)
                '#ffffff', '#f2f0f5', '#e5e1eb', '#d8d2e1', '#cbc3d7', 
                '#beb4cd', '#b1a5c3', '#a496b9', '#9787af', '#8a78a5'
            ][::-2],
            
            "red": [
                # Base Color: #A44141 (Muted red)
                '#ffffff', '#faf4f4', '#f5e9e9', '#f0dfdf', '#ead4d4', 
                '#e4c9c9', '#dfbebe', '#d9b3b3', '#d3a8a8', '#ce9d9d', 
                '#c89292', '#c28787', '#bc7c7c', '#b67171', '#A44141',
                
                # Base Color: #822C2C (Deep red)
                '#ffffff', '#f7f2f2', '#efe6e6', '#e7dada', '#dfcece', 
                '#d7c2c2', '#cfb6b6', '#c7aaaa', '#bf9e9e', '#b79292', 
                '#af8686', '#a77a7a',
                
                # Base Color: #601313 (Dark red)
                '#ffffff', '#f5f0f0', '#ebe1e1', '#e1d2d2', '#d7c3c3', 
                '#cdb4b4', '#c3a5a5', '#b99696', '#af8787', '#a57878'
            ][::-2],
            
            "pink": [
                # Base Color: #A44165 (Muted pink)
                '#ffffff', '#faf4f6', '#f5e9ed', '#f0dfe3', '#ead4d9', 
                '#e4c9cf', '#dfbec5', '#d9b3bb', '#d3a8b1', '#ce9da7', 
                '#c8929d', '#c28793', '#bc7c89', '#b6717f', '#A44165',
                
                # Base Color: #822C46 (Deep pink)
                '#ffffff', '#f7f2f4', '#efe6e9', '#e7dade', '#dfced3', 
                '#d7c2c8', '#cfb6bd', '#c7aab2', '#bf9ea7', '#b7929c', 
                '#af8691', '#a77a86',
                
                # Base Color: #601328 (Dark pink)
                '#ffffff', '#f5f0f2', '#ebe1e5', '#e1d2d8', '#d7c3cb', 
                '#cdb4be', '#c3a5b1', '#b996a4', '#af8797', '#a5788a'
            ][::-2]
        }
        
        return theme_colors.get(theme, theme_colors["green"])


    def show_splash_screen(self):
        self.splash_frame = ctk.CTkFrame(self)
        self.splash_frame.pack(fill="both", expand=True)
        
        # Load and resize image
        self.splash_image = Image.open("intro.png")
        screen_width = 1920
        screen_height = 1080
        self.splash_image = self.splash_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        
        # Create black canvas
        self.splash_canvas = tk.Canvas(self.splash_frame, highlightthickness=0, bg='black',
                                    width=screen_width, height=screen_height)
        self.splash_canvas.pack(fill='both', expand=True)
        
        # Create hidden image
        self.current_photo = ImageTk.PhotoImage(self.splash_image)
        self.splash_id = self.splash_canvas.create_image(screen_width//2, screen_height//2, 
                                                        image=self.current_photo, anchor='center')
        self.splash_canvas.itemconfig(self.splash_id, state='hidden')
        
        # Start fade after 3 seconds
        self.opacity = 0
        self.bind('<Key>', lambda e: self.setup_main_ui())
        self.after(2000, self.fade_in_splash)
        

    def fade_in_splash(self):

        if not hasattr(self, 'splash_frame') or not self.splash_frame.winfo_exists():
            return
        
        if self.opacity < 255:
            # Quadratic easing
            progress = self.opacity / 255
            current_opacity = int(255 * (progress * progress))
            
            # Update image opacity
            transparent_image = Image.new('RGBA', self.splash_image.size, (0, 0, 0, 255 - current_opacity))
            new_img = Image.alpha_composite(self.splash_image.convert('RGBA'), transparent_image)
            self.current_photo = ImageTk.PhotoImage(new_img)
            self.splash_canvas.itemconfig(self.splash_id, image=self.current_photo, state='normal')
            
            self.opacity += 5
            self.after(20, self.fade_in_splash)
        
    def setup_main_ui(self):

        self.ui_set = True
        # Remove splash screen
        self.splash_frame.destroy()
        
        self.unbind('<Key>')

        # PRELOAD DATA
        self.current_semester = None
        self.semesters = self.load_subjects_from_json("subject_data.json")
            
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
            
        # Create Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    
        # Create tabs
        self.tabview.add("GPA Calculator")
        self.tabview.add("Pomodoro Timer")
        self.tabview.add("To-Do List")
        self.tabview.add("Settings")
            
        # CHART HOVER VARS
        self._tooltip_id = None
        self._tooltip_x = 0
        self._tooltip_y = 0
        self._target_x = 0
        self._target_y = 0
        self._animation_active = False
        self._animation_after_id = None  # Track animation callback
        self.editing_subject = False

        # Initialize components
        self.setup_gpa_calculator()
        self.setup_pomodoro_timer()
        self.setup_todo_list()
        self.setup_settings()  # Initialize settings tab
    
    def toggle_theme(self):
            """Toggle between light and dark themes"""
            if self.current_theme == "dark":
                ctk.set_appearance_mode("light")
                self.current_theme = "light"
            else:
                ctk.set_appearance_mode("dark")
                self.current_theme = "dark"


    def setup_gpa_calculator(self):
        tab = self.tabview.tab("GPA Calculator")
        
        # Main container
        main_container = ctk.CTkFrame(tab, fg_color=self.COLOR_THEMES[self.current_color_theme][10])
        main_container.pack(fill="both", expand=True, padx=10, pady=0)
        
        # Configure grid for three columns
        main_container.grid_columnconfigure((0, 1, 2), weight=0)
        main_container.grid_rowconfigure(0, weight=1)

        # Configure grid for three columns with different weights
        main_container.grid_columnconfigure(0, weight=1)  # Left panel - weight 2
        main_container.grid_columnconfigure(1, weight=8)  # Middle panel - weight 3
        main_container.grid_columnconfigure(2, weight=6)  # Right panel - weight 4
        main_container.grid_rowconfigure(0, weight=1)
        
        # Left panel - Semester Selection
        semester_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        semester_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Semester selection header
        ctk.CTkLabel(semester_frame, text="Semesters", 
                    font=("Roboto", 20, "bold"), text_color=self.COLOR_THEMES[self.current_color_theme][21]).pack(pady=10)
        
        # Add semester button
        add_sem_btn = ctk.CTkButton(semester_frame, text="Add Next Semester",
                                command=self.add_new_semester, fg_color=self.COLOR_THEMES[self.current_color_theme][16], hover_color=self.COLOR_THEMES[self.current_color_theme][18], text_color=self.COLOR_THEMES[self.current_color_theme][1], font=ctk.CTkFont(weight="bold"))
        add_sem_btn.pack(pady=5)
        
        # Semester list (scrollable)
        self.semester_list = ctk.CTkScrollableFrame(semester_frame, fg_color=self.COLOR_THEMES[self.current_color_theme][5])
        self.semester_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Middle panel - Subject Display
        middle_frame = ctk.CTkFrame(main_container, fg_color=self.COLOR_THEMES[self.current_color_theme][13])
        middle_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        middle_frame.grid_columnconfigure(0, weight=1)  # Allow middle frame content to resize

        # Add this line before the subjects_scrollable
        self.current_semester_label = ctk.CTkLabel(
            middle_frame, 
            text_color=self.COLOR_THEMES[self.current_color_theme][21],
            text="Please select a semester\n to View / Add subjects",
            font=("Roboto", 20, "bold")
        )
        self.current_semester_label.pack(pady=10)
        
        
        # Subjects scrollable frame
        self.subjects_scrollable = ctk.CTkScrollableFrame(middle_frame, fg_color=self.COLOR_THEMES[self.current_color_theme][7])
        self.subjects_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # GPA display
        # GPA and CGPA display frame
        grades_frame = ctk.CTkFrame(middle_frame, fg_color="transparent")
        grades_frame.pack(pady=10)

        self.gpa_label = ctk.CTkLabel(grades_frame, text="GPA: 0.00", 
                                    font=("Roboto", 30, "bold"), 
                                    text_color=self.COLOR_THEMES[self.current_color_theme][21])
        self.gpa_label.pack(side="left", padx=20)

        self.cgpa_label = ctk.CTkLabel(grades_frame, text="CGPA: 0.00", 
                                    font=("Roboto", 30, "bold"),
                                    text_color=self.COLOR_THEMES[self.current_color_theme][21])
        self.cgpa_label.pack(side="left", padx=20)
        
        # Right panel - Pie Chart
        chart_frame = ctk.CTkFrame(main_container, fg_color=self.COLOR_THEMES[self.current_color_theme][7])
        chart_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
        
        self.animation_progress = 0
        self.pie_chart = ctk.CTkCanvas(chart_frame, background=self.COLOR_THEMES[self.current_color_theme][7], 
                                    highlightthickness=0)
        self.pie_chart.pack(padx=25, pady=25, expand=True, fill="both")
        
        
        self.refresh_semester_list()
        # Add after self.refresh_semester_list()
        cgpa = self.calculate_cgpa()
        self.cgpa_label.configure(text=f"CGPA: {cgpa:.2f}")
    
    def reload_application(self):
            """Reload application settings and refresh UI"""
            # Reload settings
            saved_settings = self.settings_manager.load_settings()
            self.current_theme = saved_settings["theme"]
            self.current_scaling = saved_settings["scaling"]
            
            # Apply settings
            ctk.set_appearance_mode(self.current_theme)
            ctk.set_widget_scaling(self.current_scaling)
            
            # Destroy all tabs
            for tab_name in ["GPA Calculator", "Pomodoro Timer", "To-Do List", "Settings"]:
                if tab_name in self.tabview._tab_dict:
                    self.tabview.delete(tab_name)
            
            # Recreate all tabs
            self.tabview.add("GPA Calculator")
            self.tabview.add("Pomodoro Timer")
            self.tabview.add("To-Do List")
            self.tabview.add("Settings")
            
            # Reinitialize components
            self.setup_gpa_calculator()
            self.setup_pomodoro_timer()
            self.setup_todo_list()
            self.setup_settings()

            # Show confirmation
            messagebox.showinfo("Settings Applied", "All settings have been applied successfully!")

    def add_new_semester(self):
        # Find the next semester number
        existing_numbers = []
        for semester in self.semesters.keys():
            try:
                num = int(semester.split()[1])  # Extract number from "Semester X"
                existing_numbers.append(num)
            except (IndexError, ValueError):
                continue
        
        next_number = 1
        if existing_numbers:
            next_number = max(existing_numbers) + 1
        
        semester_name = f"Semester {next_number}"
        
        if semester_name not in self.semesters:
            self.semesters[semester_name] = {
                "subjects": [],
                "gpa": 0.0
            }
            self.save_subjects_to_json("subject_data.json", self.semesters)
            self.refresh_semester_list()
            # Add after self.refresh_semester_list()
            cgpa = self.calculate_cgpa()
            self.cgpa_label.configure(text=f"CGPA: {cgpa:.2f}")
            self.switch_semester(semester_name)

    def refresh_semester_list(self):
        # Clear existing semester buttons
        for widget in self.semester_list.winfo_children():
            widget.destroy()
        
        # Create buttons for each semester
        for i, semester_name in enumerate(sorted(self.semesters.keys(), key=lambda x: int(x.split()[1]))):
            # Calculate the sine-line gradient index
            sine_index = ((i % 10) / 9) * math.pi
            gradient_index = int(((math.sin(sine_index) + 1) * 5) * 1) + 5
            
            semester_frame = ctk.CTkFrame(self.semester_list, 
                                        fg_color=self.COLOR_THEMES[self.current_color_theme][min(gradient_index, 20)])
            semester_frame.pack(fill="x", pady=2)
            
            btn = ctk.CTkButton(semester_frame, 
                            text=semester_name,
                            command=lambda s=semester_name: self.switch_semester(s),
                            fg_color=self.COLOR_THEMES[self.current_color_theme][min(gradient_index + 1, len(self.COLOR_THEMES[self.current_color_theme]))],
                            hover_color=self.COLOR_THEMES[self.current_color_theme][20],
                            text_color=self.COLOR_THEMES[self.current_color_theme][1], font=ctk.CTkFont(weight="bold"))
            btn.pack(side="left", expand=True, fill="x", padx=2)
            
            del_btn = ctk.CTkButton(semester_frame, 
                                text="×",
                                width=30,
                                command=lambda s=semester_name: self.delete_semester(s),
                                fg_color=self.COLORS['red']['main'],
                                hover_color=self.COLORS['red']['hover']
                                )
            del_btn.pack(side="right", padx=2)

    def switch_semester(self, semester_name):
        self.current_semester = semester_name
        self.current_semester_label.configure(text=semester_name)
        self.clear_subject_display()
        self.show_add_new_subject_btn()
        
        # Load and display subjects for the selected semester
        semester_data = self.semesters[semester_name]
        for subject in semester_data["subjects"]:
            self.display_subject(subject)
        
        # Update GPA display
        self.gpa_label.configure(text=f"GPA: {semester_data['gpa']:.2f}")
        
        # Update pie chart
        self.animation_progress = 0
        self.update_pie_chart()

    def delete_semester(self, semester_name):
        if messagebox.askyesno("Confirm Delete", 
                            f"Delete {semester_name}?"):
            del self.semesters[semester_name]
            self.save_subjects_to_json("subject_data.json", self.semesters)
            self.refresh_semester_list()
            # Add after self.refresh_semester_list()
            cgpa = self.calculate_cgpa()
            self.cgpa_label.configure(text=f"CGPA: {cgpa:.2f}")
            self.clear_subject_display()
            self.current_semester = None
            self.current_semester_label.configure(text="Please select a semester\n to View / Add subjects")

    def clear_subject_display(self):
        for widget in self.subjects_scrollable.winfo_children():
            widget.destroy()
        self.gpa_label.configure(text="GPA: 0.00")
        self.pie_chart.delete("all")

    def add_subject(self):
        if not self.current_semester:
            return messagebox.showerror("Error", "Please select or create a semester first")
        
        grade_to_gpa = {
            "A+": 4.0, "A": 4.0, "A-": 3.75,
            "B+": 3.33, "B": 3.0, "C": 2.0, 
            "D": 1.0, "F": 0.0
        }

        try:
            # Get and validate input values
            subject = self.subject_entry.get().strip() if self.subject_entry.get().strip() else False
            selected_grade = self.grade_var.get() if self.grade_var.get() != "Select Grade" else False
            grade_points = grade_to_gpa[selected_grade] if selected_grade else False
            credits = self.credits_entry.get() if self.credits_entry.get() else False

            if all([not subject, not selected_grade, not credits]):
                return messagebox.showerror("Error", "ALL the fields are EMPTY!! \n Please fill in ALL the entry fields")
            elif all([not subject, not selected_grade]):
                return messagebox.showerror("Error", "Please fill in the SUBJECT NAME field \nand select a GRADE for the subject")
            elif all([not subject, not credits]):
                return messagebox.showerror("Error", "Please fill in the SUBJECT NAME field \nand select the CREDITS weighted for the subject")
            elif all([not selected_grade, not credits]):
                return messagebox.showerror("Error", "Please select a GRADE for the subject \nand select the CREDITS weighted for the subject")
            elif not subject:
                return messagebox.showerror("Error", "Please fill in the SUBJECT NAME field")
            elif not selected_grade:
                return messagebox.showerror("Error", "Please select a GRADE for the subject")
            elif not credits:
                return messagebox.showerror("Error", "Please fill in the CREDITS field")

            credits = float(credits)

            # Create new subject data
            new_subject = {
                "subject": subject,
                "grade": selected_grade,
                "gp": grade_points,
                "credits": credits
            }

            # Add to current semester
            semester_data = self.semesters[self.current_semester]
            
            # Check if subject already exists in this semester
            for i, existing_subject in enumerate(semester_data["subjects"]):
                if existing_subject["subject"] == subject:
                    semester_data["subjects"][i] = new_subject
                    self.clear_subject_display()
                    for subject in semester_data["subjects"]:
                        self.display_subject(subject)
                    break
            else:
                semester_data["subjects"].append(new_subject)
                self.display_subject(new_subject)

            # Update GPA
            self.calculate_semester_gpa(self.current_semester)
            
            # Clear inputs
            self.subject_entry.delete(0, 'end')
            self.credits_entry.delete(0, 'end')
            self.grade_var.set("Select Grade")
            
            # Save and update display
            self.save_subjects_to_json("subject_data.json", self.semesters)
            self.update_pie_chart()
            self.input_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Credits must be a valid number")
        except KeyError:
            messagebox.showerror("Error", "Please select a valid grade")

    def calculate_semester_gpa(self, semester_name):
        semester_data = self.semesters[semester_name]
        subjects = semester_data["subjects"]
        
        total_points = 0
        total_credits = 0
        
        for subject in subjects:
            total_points += subject["gp"] * subject["credits"]
            total_credits += subject["credits"]
        
        if total_credits > 0:
            gpa = total_points / total_credits
            semester_data["gpa"] = gpa
            self.gpa_label.configure(text=f"GPA: {gpa:.2f}")
            
            # Calculate and update CGPA
            cgpa = self.calculate_cgpa()
            self.cgpa_label.configure(text=f"CGPA: {cgpa:.2f}")
        else:
            semester_data["gpa"] = 0.0
            self.gpa_label.configure(text="GPA: 0.00")
            self.cgpa_label.configure(text="CGPA: 0.00")

    def update_pie_chart(self):
        if not self.current_semester:
            return
        
        semester_data = self.semesters[self.current_semester]
        sub_weight = {s["subject"]: s["credits"] for s in semester_data["subjects"]}
        
        self.draw_pie_chart(sub_weight)

    def display_subject(self, subject_info):
        # Create main card frame
        card = ctk.CTkFrame(self.subjects_scrollable, fg_color=self.COLOR_THEMES[self.current_color_theme][5], corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)
        
        # Header frame
        header = ctk.CTkFrame(card, fg_color=self.COLOR_THEMES[self.current_color_theme][17], corner_radius=6)
        header.pack(fill="x", padx=5, pady=5)
        
        # Subject title in header
        subject_label = ctk.CTkLabel(
            header, 
            text=subject_info["subject"],
            font=("Roboto", 16, "bold"),
            anchor="w",
            text_color=self.COLOR_THEMES[self.current_color_theme][3]
        )
        subject_label.pack(side="left", padx=10)
        
        # Buttons frame in header
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=5)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            btn_frame,
            text="✏️",
            width=30,
            command=lambda: self.edit_subject(card, subject_info),
            fg_color="transparent",
            hover_color=self.COLOR_THEMES[self.current_color_theme][10]
        )
        edit_btn.pack(side="left", padx=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️",
            width=30,
            command=lambda s=subject_info["subject"]: self.delete_subject(s),
            fg_color="transparent",
            hover_color=self.COLORS['red']['hover']
        )
        delete_btn.pack(side="left" , padx=2)
        
        # Content frame
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=(0, 10))
        
        # Info grid
        info_data = [
            ("Grade", subject_info["grade"]),
            ("GP", f"{subject_info['gp']:.2f}"),
            ("Credits", f"{subject_info['credits']:.1f}")
        ]
        
        for i, (title, value) in enumerate(info_data):
            frame = ctk.CTkFrame(content, fg_color="transparent")
            frame.pack(side="left", expand=True, fill="x", padx=5)
            
            value_label = ctk.CTkLabel(frame, text=value, font=("Roboto", 24, "bold"), text_color=self.COLOR_THEMES[self.current_color_theme][21])
            value_label.pack()
            
            title_label = ctk.CTkLabel(
                frame, 
                text=title,
                font=("Roboto", 11),
                text_color="gray"
            )
            title_label.pack()

    def edit_subject(self, card_frame, subject_info):

        if self.editing_subject:
            return False
        else:
            self.editing_subject = True

        # Create edit frame
        edit_frame = ctk.CTkFrame(card_frame, fg_color=self.COLOR_THEMES[self.current_color_theme][3])
        edit_frame.pack(fill="x", padx=15, pady=10)
        
        # Grade dropdown
        grade_var = ctk.StringVar(value=subject_info["grade"])
        grade_frame = ctk.CTkFrame(edit_frame, fg_color="transparent")
        grade_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(grade_frame, text="Grade:", text_color="black").pack(side="left", padx=5)
        grade_dropdown = ctk.CTkOptionMenu(
            grade_frame,
            variable=grade_var,
            values=["A+", "A", "A-", "B+", "B", "C", "D", "F"]
        )
        grade_dropdown.pack(side="left", padx=5)
        
        # Credits entry
        credits_frame = ctk.CTkFrame(edit_frame, fg_color="transparent")
        credits_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(credits_frame, text="Credits:", text_color="black").pack(side="left", padx=5)
        credits_entry = ctk.CTkEntry(credits_frame, width=70)
        credits_entry.insert(0, str(subject_info["credits"]))
        credits_entry.pack(side="left", padx=5)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(edit_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=5)

        def cancel_edit():
            self.editing_subject = False
            edit_frame.destroy()
        
        def save_changes():

            try:
                grade_to_gpa = {
                    "A+": 4.0, "A": 4.0, "A-": 3.75,
                    "B+": 3.33, "B": 3.0, "C": 2.0, 
                    "D": 1.0, "F": 0.0
                }
                
                new_grade = grade_var.get()
                new_credits = float(credits_entry.get())
                
                # Update subject info
                semester_data = self.semesters[self.current_semester]
                for subject in semester_data["subjects"]:
                    if subject["subject"] == subject_info["subject"]:
                        subject["grade"] = new_grade
                        subject["gp"] = grade_to_gpa[new_grade]
                        subject["credits"] = new_credits
                        break
                
                # Save changes
                self.save_subjects_to_json("subject_data.json", self.semesters)
                
                # Refresh display
                self.clear_subject_display()
                self.show_add_new_subject_btn()
                for subject in semester_data["subjects"]:
                    self.display_subject(subject)
                
                # Update calculation
                self.calculate_semester_gpa(self.current_semester)
                self.update_pie_chart()
                self.editing_subject = False
                
            except ValueError:
                messagebox.showerror("Error", "Credits must be a valid number")
            except KeyError:
                messagebox.showerror("Error", "Please select a valid grade")
        
        # Save button
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save",
            command=save_changes,
            fg_color="#2c8a6e",
            hover_color="#26755d"
        )
        save_btn.pack(side="left", padx=5, expand=True)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=cancel_edit,
            fg_color="#dc3545",
            hover_color="#a82835"
        )
        cancel_btn.pack(side="left", padx=5, expand=True)

    def delete_subject(self, subject_name):
        if not self.current_semester:
            return
        
        semester_data = self.semesters[self.current_semester]
        semester_data["subjects"] = [
            s for s in semester_data["subjects"] 
            if s["subject"] != subject_name
        ]
        
        self.save_subjects_to_json("subject_data.json", self.semesters)
        self.clear_subject_display()
        self.show_add_new_subject_btn()
        
        for subject in semester_data["subjects"]:
            self.display_subject(subject)
        
        self.calculate_semester_gpa(self.current_semester)
        self.update_pie_chart()
    
    def calculate_gpa(self, gp_and_credits: list):
        total_points = 0
        total_credits = 0
        
        
        for pair in gp_and_credits:
            total_points += pair[0] * pair[1]
            total_credits += pair[1]
        
        if total_credits > 0:
            gpa = total_points / total_credits
            self.gpa_label.configure(text=f"GPA: {gpa:.2f}")
    
    def calculate_cgpa(self):
        total_points = 0
        total_credits = 0
        
        for semester_data in self.semesters.values():
            for subject in semester_data["subjects"]:
                total_points += subject["gp"] * subject["credits"]
                total_credits += subject["credits"]
        
        if total_credits > 0:
            return total_points / total_credits
        return 0.0
    
    

    
    def draw_pie_chart(self, sub_weight_set):
        # Cancel any ongoing animation
        if self._animation_after_id is not None:
            self.after_cancel(self._animation_after_id)
            self._animation_after_id = None
    
        self.pie_chart.delete("all")
        
        subject_weights = sub_weight_set
        total_credits = sum(subject_weights.values())
        
        canvas_width = self.pie_chart.winfo_width()
        canvas_height = self.pie_chart.winfo_height()
        if (canvas_width * canvas_height == 1):
            canvas_width, canvas_height = 850, 600
        
        x = canvas_width // 2
        y = canvas_height // 2
        radius = min(canvas_width, canvas_height) // 2 - 20
        
        colors = self.get_theme_colors(self.current_color_theme)
        
        # Store arc and legend items for animation
        self.pie_items = []
        self.legend_items = []
        
        def animate(current_progress):
            self.pie_chart.delete("all")
            start_angle = 0
            
            if len(subject_weights) > 1:
                for i, (subject, credits) in enumerate(subject_weights.items()):
                    # Calculate the animated extent
                    full_extent = (credits / total_credits) * 360
                    current_extent = full_extent * current_progress
                    
                    # Draw arc with current animation progress
                    arc = self.pie_chart.create_arc(
                        x - radius, y - radius, 
                        x + radius, y + radius,
                        start=start_angle, 
                        extent=current_extent,
                        fill=colors[i % len(colors)],
                        outline=""
                    )
                    
                    # Add hover effect
                    self.pie_chart.tag_bind(arc, '<Enter>', 
                        lambda e, s=subject, c=credits: self.show_tooltip(e, f"{s}: {(c/total_credits)*100:.1f}%"))
                    self.pie_chart.tag_bind(arc, '<Motion>', self.update_tooltip_position)  # Add this line
                    self.pie_chart.tag_bind(arc, '<Leave>', self.hide_tooltip)
                    
                    start_angle += current_extent
            else:
                # Single item case
                self.pie_chart.create_oval(
                    x - radius * current_progress, 
                    y - radius * current_progress, 
                    x + radius * current_progress, 
                    y + radius * current_progress,
                    fill=colors[0],
                    outline="",
                    width=2
                )
            
            # Animate legend with fade-in effect
            legend_x = x + radius + 10
            legend_y = y - radius - 100
            
            for i, (subject, credits) in enumerate(subject_weights.items()):
                # Calculate alpha for fade-in effect
                
                # Draw legend items with current opacity
                self.pie_chart.create_rectangle(
                    legend_x, legend_y + i * 30,
                    legend_x - 20, legend_y + i * 30 + 20,
                    fill=colors[i % len(colors)],
                    outline="white"
                )
                
                # Add percentage to legend
                percentage = (credits / total_credits) * 100
                self.pie_chart.create_text(
                    legend_x - 110 - (3 * len(subject)), 
                    legend_y + i * 30 + 10,
                    text=f"{subject} ({percentage:.1f}%)", 
                    fill=self.COLOR_THEMES[self.current_color_theme][21],
                    font=("Arial", 12, "bold")
                )
        
        # Animation loop
        def run_animation(step=0):
            if step <= 80:  # 20 animation frames
                progress = self.ease_out_cubic(step / 80)
                animate(progress)
                # Store the after ID so we can cancel it if needed
                self._animation_after_id = self.after(20, lambda: run_animation(step + 1))
        
        # Start animation
        run_animation()

    def ease_out_cubic(self, x):
        """Cubic easing function for smooth animation"""
        return 1 - pow(1 - x, 3)

    def show_tooltip(self, event, text):
        """Show tooltip with smooth following"""
        self._target_x = event.x + 15
        self._target_y = event.y - 15
        
        # Initialize tooltip if it doesn't exist
        if not self._tooltip_id:
            self._tooltip_x = self._target_x
            self._tooltip_y = self._target_y
            self._tooltip_id = self.pie_chart.create_text(
                self._tooltip_x, self._tooltip_y,
                text=text,
                fill=self.COLOR_THEMES[self.current_color_theme][21],
                font=("Arial", 15, "bold"),
                anchor="w"
            )
        else:
            self.pie_chart.itemconfig(self._tooltip_id, text=text)
        
        if not self._animation_active:
            self._animation_active = True
            self.animate_tooltip()

    def animate_tooltip(self):
        """Animate tooltip position with easing"""
        if self._tooltip_id:
            # Easing factor (0.1 = smooth, 0.5 = faster)
            easing = 0.15
            
            # Calculate new position with easing
            dx = self._target_x - self._tooltip_x
            dy = self._target_y - self._tooltip_y
            self._tooltip_x += dx * easing
            self._tooltip_y += dy * easing
            
            # Update tooltip position
            self.pie_chart.coords(self._tooltip_id, self._tooltip_x, self._tooltip_y)
            
            # Continue animation if mouse is still over segment
            if self._animation_active:
                self.after(16, self.animate_tooltip)  # ~60fps

    def update_tooltip_position(self, event):
        """Update target position when mouse moves"""
        if self._tooltip_id:
            self._target_x = event.x + 15
            self._target_y = event.y - 15

    def hide_tooltip(self, event):
        """Hide tooltip and stop animation"""
        if self._tooltip_id:
            self.pie_chart.delete(self._tooltip_id)
            self._tooltip_id = None
            self._animation_active = False

    # GPA CALCULATOR
    # Replace these methods in your SOLARIS class

    def load_subjects_from_json(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                return data.get("semesters", {})  # Return semesters dictionary
        except FileNotFoundError:
            return {}  # Return empty dict if file doesn't exist

    def save_subjects_to_json(self, file_path, semesters):
        data = {"semesters": semesters}
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    
    def show_add_new_subject_btn(self):
        # Add Subject Button at the top of left frame
        self.add_new_subject_btn = ctk.CTkButton(
            self.subjects_scrollable, ###
            text="+ Add New Subject", 
            command=self.show_add_subject_window,
            height=40,
            font=("Roboto", 14, "bold"),
            fg_color=self.COLOR_THEMES[self.current_color_theme][18],
            hover_color=self.COLOR_THEMES[self.current_color_theme][20]
        )
        self.add_new_subject_btn.pack(padx=20, pady=15)

    def show_add_subject_window(self):
        # Create new window
        self.input_window = ctk.CTkToplevel(self)
        self.input_window.title("Add New Subject")
        self.input_window.geometry("400x500")
        self.input_window.resizable(False, False)
        self.input_window.grab_set()  # Make window modal

        # Create main frame with padding
        main_frame = ctk.CTkFrame(self.input_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Subject input
        ctk.CTkLabel(main_frame, text="Subject:", font=("Roboto", 14)).pack(anchor="w", pady=(10, 5))
        self.subject_entry = ctk.CTkEntry(main_frame, width=300, height=35)
        self.subject_entry.pack(pady=(0, 15))
        
        # Grade input
        ctk.CTkLabel(main_frame, text="Grade:", font=("Roboto", 14)).pack(anchor="w", pady=(10, 5))
        self.grade_var = ctk.StringVar(value="Select Grade")
        self.grade_dropdown = ctk.CTkOptionMenu(
            main_frame,
            variable=self.grade_var,
            values=["A+", "A", "A-", "B+", "B", "C", "D", "F"],
            width=300,
            height=35
        )
        self.grade_dropdown.pack(pady=(0, 15))
        
        # Credits input
        ctk.CTkLabel(main_frame, text="Credits:", font=("Roboto", 14), text_color="white").pack(anchor="w", pady=(10, 5))
        self.credits_entry = ctk.CTkEntry(main_frame, width=300, height=35)
        self.credits_entry.pack(pady=(0, 15))
        
        # Buttons frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=(20, 0), fill="x")
        
        # Cancel button
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=140,
            height=40,
            fg_color=self.COLORS["red"]["main"],
            hover_color=self.COLORS["red"]["hover"],
            command=self.input_window.destroy
        ).pack(side="left", padx=5)
        
        # Add button
        ctk.CTkButton(
            button_frame,
            text="Add Subject",
            width=140,
            height=40,
            fg_color=self.COLORS["green"]["main"],
            hover_color=self.COLORS["green"]["hover"],
            command=self.add_subject
        ).pack(side="right", padx=5)













    # POMODORO TIMER
    def setup_pomodoro_timer(self):
        tab = self.tabview.tab("Pomodoro Timer")
        
        # Initialize pomodoro variables
        self.pomodoro_time_left = 25 * 60  # 25 minutes in seconds
        self.pomodoro_timer_running = False
        self.pomodoro_session_type = "work"
        self.pomodoro_count = 0
        
        self.pomodoro_settings = {
            "work_duration": 25,
            "short_break": 5,
            "long_break": 15
        }
        
        # Animation variables
        self.animation_circles = []
        self.animation_angle = 0
        self.animation_running = False
        
        # Create main container with split view
        self.pomodoro_container = ctk.CTkFrame(tab)
        self.pomodoro_container.pack(expand=True, fill="both", padx=100, pady=10)
        self.pomodoro_container.grid_rowconfigure(0, weight=1)
        self.pomodoro_container.grid_columnconfigure(0, weight=2)  # Left side larger
        self.pomodoro_container.grid_columnconfigure(1, weight=1)  # Right side smaller

        # circles color setup (POMODORO TIMER)
        self.current_color = {"r": 128, "g": 128, "b": 128}  # Start with gray
        self.target_color = {"r": 128, "g": 128, "b": 128}   # Target color (will change on start)
        self.color_transition_progress = 1.0  # Progress of color transition (0.0 to 1.0)
        
        # Setup left frame (timer and animation)
        self.setup_pomodoro_left_frame()
        
        # Setup right frame (history)
        self.setup_pomodoro_right_frame()
        
        # Start animation loop
        self.start_pomodoro_animation()
        
        # Load session history
        self.load_pomodoro_history()
    
    def setup_pomodoro_left_frame(self):
        # Left frame for timer and controls
        self.pomodoro_left_frame = ctk.CTkFrame(self.pomodoro_container)
        self.pomodoro_left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Canvas for animation
        self.pomodoro_canvas = ctk.CTkCanvas(self.pomodoro_left_frame, 
                                    bg="#363636", 
                                    highlightthickness=0)
        self.pomodoro_canvas.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Timer display
        self.timer_label = ctk.CTkLabel(
            self.pomodoro_canvas, 
            text="25:00",
            font=ctk.CTkFont(size=48, weight="bold"),
            bg_color="transparent",
            fg_color="transparent"
        )
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Session status
        self.pomodoro_status_label = ctk.CTkLabel(
            self.pomodoro_canvas,
            text="Work Session 1 of 4",
            font=ctk.CTkFont(size=16)
        )
        self.pomodoro_status_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Control buttons
        controls_frame = ctk.CTkFrame(self.pomodoro_left_frame, fg_color="transparent")
        controls_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            controls_frame, 
            text="Start",
            fg_color=self.COLORS["purple"]["main"],
            hover_color=self.COLORS["purple"]["hover"],
            command=self.toggle_pomodoro_timer
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.finish_btn = ctk.CTkButton(
            controls_frame, 
            text="Finish",
            fg_color=self.COLORS["blue"]["main"],
            hover_color=self.COLORS["blue"]["hover"],
            command=self.finish_pomodoro_session
        )
        self.finish_btn.pack(side="left", padx=5)
        
        self.settings_btn = ctk.CTkButton(
            controls_frame,
            text="Settings",
            fg_color=self.COLORS["blue"]["main"],
            hover_color=self.COLORS["blue"]["hover"],
            command=self.show_pomodoro_settings
        )
        self.settings_btn.pack(side="left", padx=5)
        
        # Bind resize event
        self.pomodoro_canvas.bind('<Configure>', self.on_pomodoro_resize)

    def start_pomodoro_animation(self):
        if not hasattr(self, 'pomodoro_canvas'):
            return
            
        center_x = self.pomodoro_canvas.winfo_width() / 2
        center_y = self.pomodoro_canvas.winfo_height() / 2 * 0.88
        radius = 200

        # Update color transition
        if self.color_transition_progress < 1.0:
            self.color_transition_progress = min(1.0, self.color_transition_progress + 0.02)
            
            # Interpolate between current and target colors
            for channel in ['r', 'g', 'b']:
                self.current_color[channel] = int(
                    self.current_color[channel] * (1 - self.color_transition_progress) +
                    self.target_color[channel] * self.color_transition_progress
                )
        
        # Clear previous circles
        self.pomodoro_canvas.delete("circle")
        
        # Draw circles with cubic speed variation
        num_circles = 8
        phase_delay = 0.2  # Controls spacing between circles
        # Adjust animation speed based on timer state
        speed_multiplier = 1.0 if self.pomodoro_timer_running else 0.1
        
        for i in range(num_circles):
            # Calculate base angle with phase delay
            delayed_angle = self.animation_angle - (i * phase_delay)
            
            # Apply cubic speed variation (t³ - t)
            t = (math.sin(delayed_angle) + 1) / 2  # Normalize to 0-1
            speed_variation = t * t * t - t  # Cubic function
            current_angle = delayed_angle * 2 + speed_variation * 2
            
            # Calculate position with cubic influence
            x = center_x + radius * math.cos(current_angle)
            y = center_y + radius * math.sin(current_angle)
            
            # Calculate opacity using cubic function with minimum 35%
            t_opacity = (math.sin(delayed_angle * 2) + 1) / 2
            opacity = int(255 * max(0.4, 0.3 + 0.7 * (t_opacity * t_opacity * t_opacity))) if self.pomodoro_timer_running else int(255 * max(0.4, 0.2 + 0.65 * (t_opacity * t_opacity * t_opacity)))
            
            # Create color with current RGB values and opacity
            color = "#{:02x}{:02x}{:02x}".format(
                int(self.current_color['r'] * opacity / 255),
                int(self.current_color['g'] * opacity / 255),
                int(self.current_color['b'] * opacity / 255)
            )
            
            # Calculate size using cubic function
            base_size = 10 * (1.2 - 0.1 * i)
            size_factor = t * t * t
            size = base_size * (0.8 + 0.4 * size_factor)
            
            # Draw circle
            self.pomodoro_canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=color,
                outline="",
                tags="circle"
            )
        
        # Update animation angle with cubic speed variation
        t = (math.sin(self.animation_angle * 2) + 1) / 2
        speed = (0.03 + 0.04 * (t * t * t)) * speed_multiplier  # Base speed plus cubic variation
        self.animation_angle += speed
        
        # Continue animation
        self.animation_running = True
        self.pomodoro_canvas.after(16, self.start_pomodoro_animation)

    def on_pomodoro_resize(self, event):
        # Get current canvas center
        center_x = event.width / 2
        center_y = event.height / 2
        
        # Adjust position history to new center
        if hasattr(self, 'position_history'):
            old_center_x = self.pomodoro_canvas.winfo_width() / 2
            old_center_y = self.pomodoro_canvas.winfo_height() / 2
            
            # Calculate offset
            offset_x = center_x - old_center_x
            offset_y = center_y - old_center_y
            
            # Update all positions in history
            self.position_history = [
                (x + offset_x, y + offset_y)
                for x, y in self.position_history
            ]
        
        # Update timer label positions
        self.timer_label.place(relx=0.5, rely=0.4, anchor="center")
        self.pomodoro_status_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def setup_pomodoro_right_frame(self):
        # Right frame for session history
        self.pomodoro_right_frame = ctk.CTkFrame(self.pomodoro_container)
        self.pomodoro_right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # History label
        history_label = ctk.CTkLabel(
            self.pomodoro_right_frame, 
            text="Session History",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        history_label.pack(pady=10)
        
        # Scrollable frame for history
        self.history_frame = ctk.CTkScrollableFrame(self.pomodoro_right_frame)
        self.history_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    def toggle_pomodoro_timer(self):
        self.pomodoro_timer_running = not self.pomodoro_timer_running
        if self.pomodoro_timer_running:
            self.target_color = {"r": 191, "g": 242, "b": 245}  # Dodger blue
            self.color_transition_progress = 0.0  # Start transition
            self.start_btn.configure(text="Pause")
            if self.pomodoro_session_type == "work":
                self.add_pomodoro_session_to_history()
            self.update_pomodoro_timer()
        else:
            # if not runnningre
            self.target_color = {"r": 128, "g": 128, "b": 128}  # Dodger blue
            self.color_transition_progress = 0.0  # Start transition
            # Set target color to blue when starting
            self.start_btn.configure(text="Resume")

    def update_pomodoro_timer(self):
        if self.pomodoro_timer_running and self.pomodoro_time_left > 0:
            mins, secs = divmod(self.pomodoro_time_left, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            self.pomodoro_time_left -= 1
            self.after(1000, self.update_pomodoro_timer)
        elif self.pomodoro_time_left <= 0:
            self.handle_pomodoro_complete()

    def handle_pomodoro_complete(self):
        self.pomodoro_timer_running = False
        self.start_btn.configure(text="Start")
        
        if self.pomodoro_session_type == "work":
            self.pomodoro_count += 1
            if self.pomodoro_count % 4 == 0:
                self.pomodoro_session_type = "long_break"
                self.pomodoro_time_left = self.pomodoro_settings["long_break"] * 60
                mins, secs = divmod(self.pomodoro_time_left, 60)
                self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
                messagebox.showinfo("Break Time", "Time for a long break!")
            else:
                self.pomodoro_session_type = "short_break"
                self.pomodoro_time_left = self.pomodoro_settings["short_break"] * 60
                mins, secs = divmod(self.pomodoro_time_left, 60)
                self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
                messagebox.showinfo("Break Time", "Time for a short break!")
        else:
            self.pomodoro_session_type = "work"
            self.pomodoro_time_left = self.pomodoro_settings["work_duration"] * 60
            mins, secs = divmod(self.pomodoro_time_left, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            messagebox.showinfo("Work Time", "Break's over! Time to focus!")
        
        self.update_pomodoro_status()

    def finish_pomodoro_session(self):
        if messagebox.askyesno("Finish Session", 
                             "Are you sure you want to finish this session?"):
            self.pomodoro_time_left = 0
            self.handle_pomodoro_complete()

    def show_pomodoro_settings(self):
        
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Timer Settings")
        settings_window.geometry("400x400")  # Made window slightly larger
        settings_window.resizable(False, False)
        settings_window.grab_set()  # Make window modal
        
        # Work duration setting
        work_label = ctk.CTkLabel(settings_window, text=f"Work Duration: {self.pomodoro_settings['work_duration']} minutes")
        work_label.pack(pady=(20,5))
        work_slider = ctk.CTkSlider(settings_window,
                                from_=1,
                                to=60,
                                number_of_steps=59,
                                width=300,
                                command=lambda value: work_label.configure(
                                    text=f"Work Duration: {int(value)} minutes"))
        work_slider.set(self.pomodoro_settings["work_duration"])
        work_slider.pack(padx=20)
        
        # Short break setting
        short_break_label = ctk.CTkLabel(settings_window, text=f"Short Break: {self.pomodoro_settings['short_break']} minutes")
        short_break_label.pack(pady=(20,5))
        short_break_slider = ctk.CTkSlider(settings_window,
                                        from_=1,
                                        to=30,
                                        number_of_steps=29,
                                        width=300,
                                        command=lambda value: short_break_label.configure(
                                            text=f"Short Break: {int(value)} minutes"))
        short_break_slider.set(self.pomodoro_settings["short_break"])
        short_break_slider.pack(padx=20)
        
        # Long break setting
        long_break_label = ctk.CTkLabel(settings_window, text=f"Long Break: {self.pomodoro_settings['long_break']} minutes")
        long_break_label.pack(pady=(20,5))
        long_break_slider = ctk.CTkSlider(settings_window,
                                        from_=5,
                                        to=60,
                                        number_of_steps=55,
                                        width=300,
                                        command=lambda value: long_break_label.configure(
                                            text=f"Long Break: {int(value)} minutes"))
        long_break_slider.set(self.pomodoro_settings["long_break"])
        long_break_slider.pack(padx=20)
        
        def save_settings():
            # Update settings dictionary
            self.pomodoro_settings["work_duration"] = int(work_slider.get())
            self.pomodoro_settings["short_break"] = int(short_break_slider.get())
            self.pomodoro_settings["long_break"] = int(long_break_slider.get())
            
            # Save to file
            with open("pomodoro_settings.json", "w") as f:
                json.dump(self.pomodoro_settings, f, indent=4)
            
            # If timer is running, stop it and reset with new duration
            if self.pomodoro_timer_running:
                self.pomodoro_timer_running = False
                self.start_btn.configure(text="Start")
            
            # Reset time based on current session type
            if self.pomodoro_session_type == "work":
                self.pomodoro_time_left = self.pomodoro_settings["work_duration"] * 60
            elif self.pomodoro_session_type == "short_break":
                self.pomodoro_time_left = self.pomodoro_settings["short_break"] * 60
            else:  # Long Break
                self.pomodoro_time_left = self.pomodoro_settings["long_break"] * 60
            
            # Update timer display
            minutes = self.pomodoro_time_left // 60
            seconds = self.pomodoro_time_left % 60
            self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            
            messagebox.showinfo("Settings Updated", 
                            "Settings have been updated. Timer has been reset with the new duration.")
            
            settings_window.destroy()
        
        save_btn = ctk.CTkButton(settings_window, 
                                text="Save",
                                width=200,
                                command=save_settings)
        save_btn.pack(pady=30)

        

    def update_pomodoro_status(self):
        self.target_color = {"r": 128, "g": 128, "b": 128}
        self.color_transition_progress = 0
        if self.pomodoro_session_type == "work":
            current_session = (self.pomodoro_count % 4) + 1
            self.pomodoro_status_label.configure(
                text=f"Work Session {current_session} of 4")
        elif self.pomodoro_session_type == "short_break":
            self.pomodoro_status_label.configure(text="Short Break")
        else:
            self.pomodoro_status_label.configure(text="Long Break")

    def add_pomodoro_session_to_history(self):
        session = {
            "start_time": datetime.now().strftime("%I:%M %p"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": self.pomodoro_session_type
        }
        
        # Create session display
        self.display_pomodoro_session(session)
        self.save_pomodoro_session(session)

    def load_pomodoro_history(self):
        try:
            with open("pomodoro_history.json", "r") as f:
                sessions = json.load(f)
                for session in sessions[-10:]:  # Show only last 10 sessions
                    self.display_pomodoro_session(session)
        except FileNotFoundError:
            pass

    def save_pomodoro_session(self, session):
        try:
            with open("pomodoro_history.json", "r") as f:
                sessions = json.load(f)
        except FileNotFoundError:
            sessions = []
        
        sessions.append(session)
        
        with open("pomodoro_history.json", "w") as f:
            json.dump(sessions, f, indent=4)

    def display_pomodoro_session(self, session):
        session_frame = ctk.CTkFrame(self.history_frame)
        session_frame.pack(fill="x", pady=5, padx=5)
        
        # Session info with icons
        time_label = ctk.CTkLabel(
            session_frame,
            text=f"🕒 {session['date']} - {session['start_time']}",
            font=ctk.CTkFont(size=14)
        )
        time_label.pack(anchor="w", padx=10, pady=(5,0))
        
        type_label = ctk.CTkLabel(
            session_frame,
            text=f"📌 {session['type'].replace('_', ' ').title()}",
            font=ctk.CTkFont(size=12)
        )
        type_label.pack(anchor="w", padx=10, pady=(0,5))
        
        # Add separator line
        separator = ctk.CTkFrame(session_frame, height=1)
        separator.pack(fill="x", padx=5)





    # TO-DO LIST
     # TO-DO LIST
    def setup_todo_list(self):
        tab = self.tabview.tab("To-Do List")
        
        # Create task button
        create_task_btn = ctk.CTkButton(tab, text="Create New Task", 
                                    command=self.show_create_task_window)
        create_task_btn.pack(padx=10, pady=10)
        
        # Tasks display frame
        tasks_container = ctk.CTkFrame(tab)
        tasks_container.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Left container for active tasks
        left_container = ctk.CTkFrame(tasks_container)
        left_container.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        
        # Active tasks label
        incomplete_label = ctk.CTkLabel(left_container, text="Active Tasks", 
                                    font=("Arial", 16, "bold"))
        incomplete_label.pack(padx=5, pady=5)
        
        # Active tasks scrollable frame
        self.incomplete_tasks_frame = ctk.CTkScrollableFrame(left_container)
        self.incomplete_tasks_frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Right container for completed tasks
        right_container = ctk.CTkFrame(tasks_container)
        right_container.pack(side="right", padx=5, pady=5, fill="both", expand=True)
        
        # Completed tasks label
        completed_label = ctk.CTkLabel(right_container, text="Completed Tasks", 
                                    font=("Arial", 16, "bold"))
        completed_label.pack(padx=5, pady=5)
        
        # Completed tasks scrollable frame
        self.completed_tasks_frame = ctk.CTkScrollableFrame(right_container)
        self.completed_tasks_frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Initialize tasks dictionary
        self.tasks = {}
        
        # Load existing tasks
        self.load_tasks()
    
    def show_create_task_window(self):
        # Create new window
        self.task_window = ctk.CTkToplevel(self)
        self.task_window.title("Create New Task")
        self.task_window.geometry("400x675")
        self.task_window.resizable(False, False)
        self.task_window.grab_set()  # Make window modal
        
        # Task name
        name_label = ctk.CTkLabel(self.task_window, text="Task Name:")
        name_label.pack(padx=10, pady=5)
        self.task_name_entry = ctk.CTkEntry(self.task_window, width=300)
        self.task_name_entry.pack(padx=10, pady=5)
        
        # Deadline (Calendar)
        deadline_label = ctk.CTkLabel(self.task_window, text="Deadline:")
        deadline_label.pack(padx=10, pady=5)
        self.calendar = Calendar(self.task_window, selectmode='day', 
                            date_pattern='y-mm-dd')
        self.calendar.pack(padx=10, pady=5)
        
        # Remarks
        remarks_label = ctk.CTkLabel(self.task_window, text="Remarks:")
        remarks_label.pack(padx=10, pady=5)
        self.remarks_text = ctk.CTkTextbox(self.task_window, width=300, height=100)
        self.remarks_text.pack(padx=10, pady=5)

        # Category label
        category_btn = ctk.CTkLabel(self.task_window, text="Category:" )
        category_btn.pack(padx=10, pady=5)

        # Initialise category dropdown button
        self.category_var = ctk.StringVar(value="Select Category")
        self.category_type = ctk.CTkOptionMenu(self.task_window, variable=self.category_var,
                                               values=["Work","Home","Errands","Online"])
        self.category_type.pack(padx=10, pady=5)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.task_window)
        buttons_frame.pack(padx=10, pady=10, fill="x")
        
        # Cancel button
        cancel_btn = ctk.CTkButton(buttons_frame, text="Cancel", 
                                command=self.task_window.destroy)
        cancel_btn.pack(side="left", padx=5, expand=True)
        
        # Create button
        create_btn = ctk.CTkButton(buttons_frame, text="Create Task", 
                                command=self.create_task)
        create_btn.pack(side="right", padx=5, expand=True)

    def create_task(self):
        name = self.task_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Task name cannot be empty!")
            return
        
        if name in self.tasks:
            messagebox.showerror("Error", "Task name already exists!")
            return
            
        task = {
            "name": name,
            "date_created": datetime.now().strftime("%Y-%m-%d"),
            "deadline": self.calendar.get_date(),
            "remarks": self.remarks_text.get("1.0", "end-1c").strip(),
            "category": self.category_type.get(),
            "complete": False
        }
        
        self.tasks[name] = task
        self.save_tasks()
        self.refresh_display()
        self.task_window.destroy()

    def display_task(self, task, frame):
        # Create card frame with padding and border
        card_frame = ctk.CTkFrame(frame, corner_radius=10)
        card_frame.pack(padx=10, pady=5, fill="x")

        # Content frame inside card for padding
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(padx=15, pady=10, fill="x")

        # Header frame for task name
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))

        # Task name - title
        name_label = ctk.CTkLabel(
            header_frame, 
            text=task["name"],
            font=("Arial", 16, "bold")
        )
        name_label.pack(side="left", anchor="w")

        # Status indicator
        status_frame = ctk.CTkFrame(
            header_frame,
            width=12,
            height=12,
            corner_radius=6,
            fg_color="green" if task["complete"] else "orange"
        )
        status_frame.pack(side="right", padx=5)

        # Separator line
        separator = ctk.CTkFrame(content_frame, height=1, fg_color="gray70")
        separator.pack(fill="x", pady=(0, 10))

        # Dates frame
        dates_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        dates_frame.pack(fill="x", pady=(0, 5))

        # Created date
        created_label = ctk.CTkLabel(
            dates_frame,
            text=f"📅 Created: {task['date_created']}",
            font=("Arial", 12)
        )
        created_label.pack(side="left")

        # Deadline date
        deadline_label = ctk.CTkLabel(
            dates_frame,
            text=f"⏰ Due: {task['deadline']}",
            font=("Arial", 12)
        )
        deadline_label.pack(side="right")

        # Completion date if task is complete
        if task["complete"] and "completion_date" in task:
            completion_label = ctk.CTkLabel(
                content_frame,
                text=f"✅ Completed: {task['completion_date']}",
                font=("Arial", 12)
            )
            completion_label.pack(anchor="w", pady=(0, 5))

        # Remarks section if there are remarks
        if task["remarks"]:
            remarks_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            remarks_frame.pack(fill="x", pady=(5, 0))
            
            remarks_header = ctk.CTkLabel(
                remarks_frame,
                text="📝 Remarks:",
                font=("Arial", 12, "bold")
            )
            remarks_header.pack(anchor="w")
            
            remarks_text = ctk.CTkLabel(
                remarks_frame,
                text=task["remarks"],
                font=("Arial", 12),
                wraplength=350  # Adjust based on your needs
            )
            remarks_text.pack(anchor="w", padx=(10, 0))

        # Category section
        if task["category"]:
            category_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            category_frame.pack(fill="x", pady=(0,10))

            category_header = ctk.CTkLabel(
                category_frame,
                text="📋 Category:",
                font=("Arial", 12, "bold")
            )
            category_header.pack(anchor="e")

            category_label = ctk.CTkLabel(
                category_frame,
                text=task['category'],
                font=("Arial", 12)
            )
            category_label.pack(anchor="e",padx=(0,22))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))

        if not task["complete"]:
            # Complete button
            complete_btn = ctk.CTkButton(
                buttons_frame,
                text="✓ Mark Complete",
                command=lambda t=task: self.mark_complete(t),
                height=32,
                fg_color="#2c8a6e",
                hover_color="#26755d"
            )
            complete_btn.pack(side="left", padx=(0, 5))

            # Delete button
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="🗑 Delete",
                command=lambda t=task: self.delete_task(t),
                height=32,
                fg_color="#dc3545",
                hover_color="#a82835"
            )
            delete_btn.pack(side="left")
        else:
            # Recreate button
            recreate_btn = ctk.CTkButton(
                buttons_frame,
                text="↻ Recreate Task",
                command=lambda t=task: self.recreate_task(t),
                height=32,
                fg_color="#5e71a6",
                hover_color="#4d5c87"
            )
            recreate_btn.pack(side="left", padx=(0, 5))

            # Delete button
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="🗑 Delete",
                command=lambda t=task: self.delete_task(t),
                height=32,
                fg_color="#dc3545",
                hover_color="#a82835"
            )
            delete_btn.pack(side="left")

    def mark_complete(self, task):
        task_name = task["name"]
        self.tasks[task_name]["complete"] = True
        self.tasks[task_name]["completion_date"] = datetime.now().strftime("%Y-%m-%d")
        self.save_tasks()
        self.refresh_display() 


    def delete_task(self, task):
        task_name = task["name"]
        if messagebox.askyesno("Confirm Delete", 
                            f"Are you sure you want to delete task: {task_name}?"):
            del self.tasks[task_name]
            self.save_tasks()
            self.refresh_display()

    def recreate_task(self, old_task):
        # Create new task with same details but new dates
        new_name = f"{old_task['name']} (Recreated)"
        
        task = {
            "name": new_name,
            "date_created": datetime.now().strftime("%Y-%m-%d"),
            "deadline": old_task["deadline"],
            "remarks": old_task["remarks"],
            "category": old_task["category"],
            "complete": False
        }
        
        self.tasks[new_name] = task
        self.save_tasks()
        self.refresh_display()

    def refresh_display(self):
        # Clear both frames
        for widget in self.incomplete_tasks_frame.winfo_children():
            widget.destroy()
        for widget in self.completed_tasks_frame.winfo_children():
            widget.destroy()
        
        # Redisplay all tasks
        for task in self.tasks.values():
            if task["complete"]:
                self.display_task(task, self.completed_tasks_frame)
            else:
                self.display_task(task, self.incomplete_tasks_frame)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                self.tasks = {task["name"]: task for task in data["tasks"]}
                self.refresh_display()
        except FileNotFoundError:
            self.tasks = {}

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump({"tasks": list(self.tasks.values())}, file, indent=4)

    def setup_settings(self):
        """Setup the Settings tab with appearance and scaling controls"""
        tab = self.tabview.tab("Settings")
        
        # Main settings container with padding
        settings_container = ctk.CTkFrame(tab)
        settings_container.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Load saved settings
        saved_settings = self.settings_manager.load_settings()
        self.current_theme = saved_settings["theme"]
        self.current_scaling = saved_settings["scaling"]
        self.current_color_theme = saved_settings.get("color_theme", "green")
        
        # === Appearance Settings Section ===
        appearance_frame = ctk.CTkFrame(settings_container)
        appearance_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(appearance_frame, text="Appearance Settings", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(padx=10, pady=10)
        
        # Theme Selection
        theme_frame = ctk.CTkFrame(appearance_frame)
        theme_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(theme_frame, text="Theme Mode:").pack(side="left", padx=10)
        self.theme_var = ctk.StringVar(value="Dark" if self.current_theme == "dark" else "Light")
        theme_switch = ctk.CTkSwitch(theme_frame, text="Dark Mode", 
                                    command=self.toggle_theme,
                                    variable=self.theme_var, onvalue="Dark", offvalue="Light")
        theme_switch.pack(side="left", padx=10)
        
        # Color Theme Selection
        color_theme_frame = ctk.CTkFrame(appearance_frame)
        color_theme_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(color_theme_frame, text="Color Theme:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(padx=10, pady=(10,5))
        
        # Create a frame for color theme options
        options_frame = ctk.CTkFrame(color_theme_frame)
        options_frame.pack(padx=10, pady=5, fill="x")
        
        self.color_theme_var = ctk.StringVar(value=self.current_color_theme)
        
        def change_color_theme():
            """Update the current color theme"""
            self.current_color_theme = self.color_theme_var.get()
            self.COLOR_THEMES[self.current_color_theme] = self.COLOR_THEMES[self.current_color_theme]
            
            # Update preview colors
            for btn, theme_name in theme_buttons:
                btn.configure(fg_color=self.COLOR_THEMES[theme_name][15])
        
        # Create theme buttons with color preview
        theme_buttons = []
        for theme_name in ["green", "blue", "purple", "pink", "red"]:
            btn_frame = ctk.CTkFrame(options_frame)
            btn_frame.pack(side="left", padx=5, pady=5, expand=True)
            
            radio_btn = ctk.CTkRadioButton(
                btn_frame,
                text=theme_name.capitalize(),
                variable=self.color_theme_var,
                value=theme_name,
                command=change_color_theme,
                fg_color=self.COLOR_THEMES[theme_name][15],
                hover_color=self.COLOR_THEMES[theme_name][17]
            )
            radio_btn.pack(padx=5, pady=5)
            theme_buttons.append((radio_btn, theme_name))
        
        # === Scaling Settings Section ===
        scaling_frame = ctk.CTkFrame(settings_container)
        scaling_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(scaling_frame, text="Interface Scaling", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(padx=10, pady=10)
        
        scale_frame = ctk.CTkFrame(scaling_frame)
        scale_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(scale_frame, text="Widget Scale:").pack(side="left", padx=10)
        
        def update_scaling(value):
            """Update the widget scaling"""
            self.current_scaling = float(value)
            ctk.set_widget_scaling(self.current_scaling)
            scale_label.configure(text=f"{self.current_scaling:.1f}x")
        
        self.scale_slider = ctk.CTkSlider(scale_frame, from_=0.8, to=1.6, 
                                        command=update_scaling,
                                        number_of_steps=8)
        self.scale_slider.set(self.current_scaling)
        self.scale_slider.pack(side="left", padx=10, fill="x", expand=True)
        
        scale_label = ctk.CTkLabel(scale_frame, text=f"{self.current_scaling:.1f}x")
        scale_label.pack(side="left", padx=10)
        
        # === Buttons Frame ===
        buttons_frame = ctk.CTkFrame(settings_container)
        buttons_frame.pack(pady=20, fill="x")
        
        def apply_settings():
            """Save settings and reload the application"""
            settings = {
                "theme": self.current_theme,
                "scaling": self.current_scaling,
                "color_theme": self.current_color_theme
            }
            
            if self.settings_manager.save_settings(settings):
                if messagebox.askyesno("Apply Settings", 
                                    "Settings will be applied now. Continue?"):
                    self.reload_application()
        
        def reset_settings():
            """Reset all settings to default values"""
            if messagebox.askyesno("Reset Settings", 
                                "Are you sure you want to reset all settings to default?"):
                # Reset to defaults
                self.current_scaling = 1.3
                self.current_theme = "dark"
                self.current_color_theme = "green"
                self.COLOR_THEMES[self.current_color_theme] = self.COLOR_THEMES["green"]
                
                # Update UI
                ctk.set_widget_scaling(1.3)
                ctk.set_appearance_mode("dark")
                
                # Update controls
                self.theme_var.set("Dark")
                self.scale_slider.set(1.3)
                self.color_theme_var.set("green")
                change_color_theme()  # Update color theme preview
        
        # Apply Button
        apply_button = ctk.CTkButton(buttons_frame, text="Apply Settings",
                                    command=apply_settings,
                                    fg_color=self.COLOR_THEMES[self.current_color_theme][15],
                                    hover_color=self.COLOR_THEMES[self.current_color_theme][17])
        apply_button.pack(side="right", padx=10)
        
        # Reset Button
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Defaults",
                                    command=reset_settings,
                                    fg_color=self.COLOR_THEMES[self.current_color_theme][19],
                                    hover_color=self.COLOR_THEMES[self.current_color_theme][20])
        reset_button.pack(side="right", padx=10)


if __name__ == "__main__":
    app = SOLARIS()
    app.mainloop()
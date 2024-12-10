import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pywinstyles
import time
import math
import json

# importing for todolist
from tkcalendar import Calendar
from datetime import datetime
import json
from tkinter import messagebox


class SOLARIS(ctk.CTk):
    def __init__(self):
        super().__init__()

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
            }
        }

        # Window Configuration        
        self.title("SOLARIS - Study & Productivity Hub")
        width = self.winfo_screenwidth()  
        height = self.winfo_screenheight() 
        self.geometry(f"{width}x{height}")

        ctk.set_default_color_theme("green")
        ctk.set_appearance_mode("dark")
        ctk.set_widget_scaling(1.3)      # Increase the scaling (default is 1.0)
        self.default_font = ctk.CTkFont("Roboto", 14)
        pywinstyles.apply_style(self, "acrylic") # window 11 theme 

        # Show splash screen first
        self.show_splash_screen()
        # Schedule the main UI setup after splash screen
        self.after(2000, self.setup_main_ui)

    def show_splash_screen(self):
        # Create splash screen frame
        self.splash_frame = ctk.CTkFrame(self)
        self.splash_frame.pack(fill="both", expand=True)
            
        # Configure grid for centering
        self.splash_frame.grid_rowconfigure(0, weight=1)
        self.splash_frame.grid_rowconfigure(2, weight=1)
        self.splash_frame.grid_columnconfigure(0, weight=1)
            
        # Add SOLARIS text
        solaris_label = ctk.CTkLabel(
            self.splash_frame,
            text="SOLARIS",
            font=("Roboto", 48, "bold")
        )
        solaris_label.grid(row=1, column=0, pady=(0, 20))
            
        # Add "powered by" text
        powered_by_label = ctk.CTkLabel(
            self.splash_frame,
            text="powered by Wy",
            font=("Roboto", 24)
        )
        powered_by_label.grid(row=2, column=0)
        
    def setup_main_ui(self):
        # Remove splash screen
        self.splash_frame.destroy()
            
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
            
        # Initialize components
        self.setup_gpa_calculator()
        self.setup_pomodoro_timer()
        self.setup_todo_list()

        # GPA CALCULATOR DATA INIT
        self.subject_data = self.load_subjects_from_json("subject_data.json")
        self.gp_and_credits = [(i["gp"],i["credits"],i["subject"]) for i in self.subject_data]
            
        # CHART HOVER VARS
        self._tooltip_id = None
        self._tooltip_x = 0
        self._tooltip_y = 0
        self._target_x = 0
        self._target_y = 0
        self._animation_active = False

        # GPA CALCULATOR DATA INIT
        self.subject_data = self.load_subjects_from_json("subject_data.json")
        self.gp_and_credits = [(i["gp"],i["credits"],i["subject"]) for i in self.subject_data]
        
    

    def load_subjects_from_json(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                return data["subjects"]
        except FileNotFoundError:
            return []
    
    def save_subjects_to_json(self, file_path, subjects):
        data = {"subjects": subjects}
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    
    def draw_pie_chart(self, sub_weight_set):
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
        
        colors = ["#8B5FBF", "#6D70D6", "#4F82ED", "#38A0F2", "#32B7E6", "#4BD3C5", "#6FDFAA", "#8DE68D", "#A3EB6D", "#B6DF56", "#C6D047", "#D0BE42", "#D7A842", "#DE8F47", "#E47250"]
        
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
                    outline="white",
                    width=2
                )
            
            # Animate legend with fade-in effect
            legend_x = x + radius + 50
            legend_y = y - radius
            
            for i, (subject, credits) in enumerate(subject_weights.items()):
                # Calculate alpha for fade-in effect
                alpha = int(255 * current_progress)
                color = self.pie_chart.winfo_rgb(colors[i % len(colors)])
                
                # Draw legend items with current opacity
                self.pie_chart.create_rectangle(
                    legend_x, legend_y + i * 30,
                    legend_x + 20, legend_y + i * 30 + 20,
                    fill=colors[i % len(colors)],
                    outline="white"
                )
                
                # Add percentage to legend
                percentage = (credits / total_credits) * 100
                self.pie_chart.create_text(
                    legend_x - 60 - (3 * len(subject)), 
                    legend_y + i * 30 + 10,
                    text=f"{subject} ({percentage:.1f}%)", 
                    font=("Arial", 12),
                    fill=f"#{alpha:02x}{alpha:02x}{alpha:02x}"
                )
        
        # Animation loop
        def run_animation(step=0):
            if step <= 80:  # 20 animation frames
                progress = self.ease_out_cubic(step / 80)
                animate(progress)
                self.after(20, lambda: run_animation(step + 1))
        
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
                fill="white",
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
    def setup_gpa_calculator(self):
        tab = self.tabview.tab("GPA Calculator")
        
        # Input frame
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(padx=10, pady=10, fill="x")
        self.sub_weight = {}
        
        # Subject input
        ctk.CTkLabel(input_frame, text="Subject:").pack(side="left", padx=5)
        self.subject_entry = ctk.CTkEntry(input_frame, width=150)
        self.subject_entry.pack(side="left", padx=5)
        
        # Grade input
        ctk.CTkLabel(input_frame, text="Grade:").pack(side="left", padx=5)
        self.grade_var = ctk.StringVar(value="Select Grade")
        self.grade_dropdown = ctk.CTkOptionMenu(input_frame, 
                                            variable=self.grade_var,
                                            values=["A+", "A", "A-", "B+", "B", "C", "D", "F"])
        

        self.grade_dropdown.pack(side="left", padx=5)
        
        # Credits input
        ctk.CTkLabel(input_frame, text="Credits:").pack(side="left", padx=5)
        self.credits_entry = ctk.CTkEntry(input_frame, width=70)
        self.credits_entry.pack(side="left", padx=5)
        
        # Add subject button
        self.add_subject_btn = ctk.CTkButton(input_frame, text="Add Subject", 
                                           command=self.add_subject)
        self.add_subject_btn.pack(side="left", padx=10)

        # Frame for subject (left) and chart (right)
        self.main_frame = ctk.CTkFrame(tab)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)  # Fill both directions and expand

        # Configure the columns for dynamic resizing
        self.main_frame.columnconfigure((0, 1), weight=1)  # Two columns
        self.main_frame.rowconfigure(0, weight=1)  # One row

        # Left frame for subjects (scrollable)
        self.subjects_frame = ctk.CTkFrame(self.main_frame)
        self.subjects_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Scrollable frame inside the subjects frame
        self.subjects_scrollable = ctk.CTkScrollableFrame(self.subjects_frame, fg_color="#505050")
        self.subjects_scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # GPA display
        self.gpa_label = ctk.CTkLabel(self.subjects_frame, text="GPA: 0.00", font=("Roboto", 30))
        self.gpa_label.pack(pady=10)

        # Right frame for pie chart
        self.chart_frame = ctk.CTkFrame(self.main_frame)
        self.chart_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.pie_chart = ctk.CTkCanvas(self.chart_frame, background="#363636", highlightthickness=0)
        self.pie_chart.grid(sticky='nsew')
        self.pie_chart.pack(padx=25, pady=25, expand=True, fill="both")

        #use loaded subject data, make rows, then draw
        # GPA CALCULATOR DATA INIT

        # BLOCK OF CODE TO LOAD AND POPULATE THE ARRAYS
        self.subject_data = self.load_subjects_from_json("subject_data.json") # [{'subject': 'Math', 'grade': 'A', 'gp': 4.0, 'credits': 3}, {'subject': 'English', 'grade': 'B+', 'gp': 3.33, 'credits': 4}, {'subject': 'HISTORY', 'grade': 'A+', 'gp': 4.0, 'credits': 3.0}]
        self.gp_and_credits = [(i["gp"],i["credits"],i["subject"]) for i in self.subject_data] # [(4.0, 3), (3.33, 4), (4.0, 3.0)]
        self.sub_weight = {i["subject"]:i["credits"] for i in self.subject_data} # {'Math': 3, 'English': 4, 'HISTORY': 3.0}

        self.calculate_gpa(self.gp_and_credits)
        self.draw_pie_chart(self.sub_weight)

         # Create visual elements for each loaded subject
        for subject_info in self.subject_data:
            row_frame = ctk.CTkFrame(self.subjects_scrollable)
            row_frame.pack(fill="x", pady=5)

            # Create column frames
            column_data = [
                ("Subject", subject_info["subject"][0:15:1]),
                ("Grade", subject_info["grade"]),
                ("GP", f"{subject_info['gp']:.2f}"),
                ("Credits", f"{subject_info['credits']:.1f}")
            ]

            max_width = 0
            # First pass to calculate maximum width
            for col_title, col_value in column_data:
                col_frame = ctk.CTkFrame(row_frame)
                col_label = ctk.CTkLabel(col_frame, text=col_value, anchor="w")
                col_label.pack(pady=2)
                title_label = ctk.CTkLabel(col_frame, text=col_title, font=("Arial", 10))
                title_label.pack(pady=2)
                max_width = max(max_width, col_label.winfo_width(), title_label.winfo_width())
                col_frame.destroy()  # Remove temporary frame used for width calculation

            # Second pass to create actual frames with consistent width
            for col_title, col_value in column_data:
                col_frame = ctk.CTkFrame(row_frame, width=max_width + 20)
                col_frame.pack(side="left", padx=10)
                col_label = ctk.CTkLabel(col_frame, text=col_value, anchor="w")
                col_label.pack(pady=2)
                title_label = ctk.CTkLabel(col_frame, text=col_title, font=("Arial", 10))
                title_label.pack(pady=2)
            
            # Add delete button
            #chek
            delete_btn = ctk.CTkButton(row_frame, text="Delete", width=60,
                        command=lambda row=row_frame, 
                        sub=subject_info["subject"]: self.delete_subject(row, sub), 
                        fg_color="#b34242")
            delete_btn.pack(side="right", padx=20)

        # Update initial calculations
        if self.subject_data:  # Only calculate if there's data
            self.calculate_gpa(self.gp_and_credits)
            self.draw_pie_chart(self.sub_weight)

    
    def add_subject(self):
        grade_to_gpa = {
            "A+": 4.0, "A": 4.0, "A-": 3.75,
            "B+": 3.33, "B": 3.0, "C": 2.0, 
            "D": 1.0, "F": 0.0
        }

        try:
            # Get and validate input values
            subject = self.subject_entry.get().strip()
            selected_grade = self.grade_var.get()
            grade_points = grade_to_gpa[selected_grade]
            credits = float(self.credits_entry.get())

            if not subject or selected_grade == "Select Grade":
                return messagebox.showerror("Error", "Please fill in all fields")

            # Create new subject data
            new_subject = {
                "subject": subject,
                "grade": selected_grade,
                "gp": grade_points,
                "credits": credits
            }

            # Update or add to subject_data
            subject_exists = False
            for i, existing_subject in enumerate(self.subject_data):
                if existing_subject["subject"] == subject:
                    self.subject_data[i] = new_subject
                    subject_exists = True
                    break
            
            if not subject_exists:
                self.subject_data.append(new_subject)

            # Update sub_weight for pie chart
            self.sub_weight[subject] = credits
            self.gp_and_credits = [(i["gp"],i["credits"],i["subject"]) for i in self.subject_data]
            

            # Create visual elements
            row_frame = ctk.CTkFrame(self.subjects_scrollable)
            row_frame.pack(fill="x", pady=5)

            # Create column frames
            column_data = [
                ("Subject", subject[0:15:1]),
                ("Grade", selected_grade),
                ("GP", f"{grade_points:.2f}"),
                ("Credits", f"{credits:.1f}")
            ]

            max_width = 0
            for col_title, col_value in column_data:
                col_frame = ctk.CTkFrame(row_frame)
                col_label = ctk.CTkLabel(col_frame, text=col_value, anchor="w")
                col_label.pack(pady=2)
                title_label = ctk.CTkLabel(col_frame, text=col_title, font=("Arial", 10))
                title_label.pack(pady=2)
                max_width = max(max_width, col_label.winfo_width(), title_label.winfo_width())

            # Set the same width for all column frames
            for col_title, col_value in column_data:
                col_frame = ctk.CTkFrame(row_frame, width=max_width + 20)
                col_frame.pack(side="left", padx=10)
                col_label = ctk.CTkLabel(col_frame, text=col_value, anchor="w")
                col_label.pack(pady=2)
                title_label = ctk.CTkLabel(col_frame, text=col_title, font=("Arial", 10))
                title_label.pack(pady=2)
            
            # Add delete button
            # chek
            delete_btn = ctk.CTkButton(row_frame, text="Delete", width=60,
                        command=lambda row=row_frame, 
                        subject=subject: self.delete_subject(row, subject), 
                        fg_color="#c45151")
            delete_btn.pack(side="right", padx=20)
            
            # Clear entries
            self.subject_entry.delete(0, 'end')
            self.credits_entry.delete(0, 'end')
            self.grade_var.set("Select Grade")
            
            # Update calculations and save
            self.calculate_gpa(self.gp_and_credits)
            self.draw_pie_chart(self.sub_weight)
            self.save_subjects_to_json("subject_data.json", self.subject_data)

        except ValueError:
            messagebox.showerror("Error", "Credits must be a valid number")
        except KeyError:
            messagebox.showerror("Error", "Please select a valid grade")
    
    def delete_subject(self, row, subject):
        # Remove the subject from the sub_weight dictionary
        if subject in self.sub_weight:
            del self.sub_weight[subject]          

        # Remove the subject's grade points and credits from gp_and_credits list
        for pair in self.gp_and_credits:
            if pair[2] == subject:
                self.gp_and_credits.remove(pair)
                break

        # Remove from subject_data list
        self.subject_data = [item for item in self.subject_data if item["subject"] != subject]
        
        # Save updated data to JSON file
        self.save_subjects_to_json("subject_data.json", self.subject_data)

        # Destroy the row frame
        row.destroy()

        # Recalculate GPA
        self.calculate_gpa(self.gp_and_credits)

        # Redraw the pie chart
        self.draw_pie_chart(self.sub_weight)
    
    def calculate_gpa(self, gp_and_credits: list):
        total_points = 0
        total_credits = 0
        
        
        for pair in gp_and_credits:
            total_points += pair[0] * pair[1]
            total_credits += pair[1]
        
        if total_credits > 0:
            gpa = total_points / total_credits
            self.gpa_label.configure(text=f"GPA: {gpa:.2f}")
    
    # POMODORO TIMER
    def setup_pomodoro_timer(self):
        tab = self.tabview.tab("Pomodoro Timer")
        
        # Initialize pomodoro variables
        self.pomodoro_time_left = 25 * 60  # 25 minutes in seconds
        self.pomodoro_timer_running = False
        self.pomodoro_session_type = "Study"
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
            command=self.toggle_pomodoro_timer
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.finish_btn = ctk.CTkButton(
            controls_frame, 
            text="Finish",
            command=self.finish_pomodoro_session
        )
        self.finish_btn.pack(side="left", padx=5)
        
        self.settings_btn = ctk.CTkButton(
            controls_frame,
            text="Settings",
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
        
        # Clear previous circles
        self.pomodoro_canvas.delete("circle")
        
        # Draw circles with cubic speed variation
        num_circles = 8
        phase_delay = 0.2  # Controls spacing between circles
        
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
            
            # Calculate opacity using cubic function
            t_opacity = (math.sin(delayed_angle * 2) + 1) / 2
            opacity = int(255 * (0.4 + 0.6 * (t_opacity * t_opacity * t_opacity)))
            opacity_hex = format(opacity, '02x')
            
            # Calculate size using cubic function
            base_size = 10 * (1.2 - 0.1 * i)
            size_factor = t * t * t
            size = base_size * (0.8 + 0.4 * size_factor)
            
            # Draw circle
            self.pomodoro_canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=f"#{opacity_hex}{opacity_hex}{opacity_hex}",
                outline="",
                tags="circle"
            )
        
        # Update animation angle with cubic speed variation
        t = (math.sin(self.animation_angle * 2) + 1) / 2
        speed = 0.03 + 0.04 * (t * t * t)  # Base speed plus cubic variation
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
            self.start_btn.configure(text="Pause")
            if self.pomodoro_session_type == "work":
                self.add_pomodoro_session_to_history()
            self.update_pomodoro_timer()
        else:
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
                messagebox.showinfo("Break Time", "Time for a long break!")
            else:
                self.pomodoro_session_type = "short_break"
                self.pomodoro_time_left = self.pomodoro_settings["short_break"] * 60
                messagebox.showinfo("Break Time", "Time for a short break!")
        else:
            self.pomodoro_session_type = "work"
            self.pomodoro_time_left = self.pomodoro_settings["work_duration"] * 60
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
        settings_window.geometry("300x200")
        settings_window.grab_set()  # Make window modal
        
        # Work duration setting
        ctk.CTkLabel(settings_window, 
                    text="Work Duration (minutes):").pack(pady=5)
        work_entry = ctk.CTkEntry(settings_window)
        work_entry.insert(0, str(self.pomodoro_settings["work_duration"]))
        work_entry.pack()
        
        # Short break setting
        ctk.CTkLabel(settings_window, 
                    text="Short Break (minutes):").pack(pady=5)
        short_break_entry = ctk.CTkEntry(settings_window)
        short_break_entry.insert(0, str(self.pomodoro_settings["short_break"]))
        short_break_entry.pack()
        
        # Long break setting
        ctk.CTkLabel(settings_window, 
                    text="Long Break (minutes):").pack(pady=5)
        long_break_entry = ctk.CTkEntry(settings_window)
        long_break_entry.insert(0, str(self.pomodoro_settings["long_break"]))
        long_break_entry.pack()
        
        def save_settings():
            try:
                self.pomodoro_settings["work_duration"] = int(work_entry.get())
                self.pomodoro_settings["short_break"] = int(short_break_entry.get())
                self.pomodoro_settings["long_break"] = int(long_break_entry.get())
                self.save_pomodoro_settings()
                settings_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        save_btn = ctk.CTkButton(settings_window, text="Save", 
                                command=save_settings)
        save_btn.pack(pady=20)

    def update_pomodoro_status(self):
        if self.pomodoro_session_type == "work":
            current_session = (self.pomodoro_count % 4) + 1
            self.pomodoro_status_label.configure(
                text=f"Work Session {current_session} of 4")
        elif self.pomodoro_session_type == "short_break":
            self.pomodoro_status_label.configure(text="Short Break")
        else:
            self.pomodoro_status_label.configure(text="Long Break")

    def on_pomodoro_resize(self, event):
        # Update circle positions when canvas is resized
        center_x = event.width / 2
        center_y = event.height / 2
        for i, circle in enumerate(self.animation_circles):
            angle = (i * math.pi / 3)
            circle['x'] = center_x + 120 * math.cos(angle)
            circle['y'] = center_y + 120 * math.sin(angle)
        
        # Update label positions
        self.timer_label.place(relx=0.5, rely=0.4, anchor="center")
        self.pomodoro_status_label.place(relx=0.5, rely=0.5, anchor="center")
    
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

    def save_pomodoro_settings(self):
        with open("pomodoro_settings.json", "w") as f:
            json.dump(self.pomodoro_settings, f, indent=4)

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
        self.task_window.geometry("400x650")
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

if __name__ == "__main__":
    app = SOLARIS()
    app.mainloop()
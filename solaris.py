import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pywinstyles
import time
import math
import json



class SOLARIS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        
        self.title("SOLARIS - Study & Productivity Hub")
        width = self.winfo_screenwidth()  
        height = self.winfo_screenheight() 
        self.geometry(f"{width}x{height}")

        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")
        ctk.set_widget_scaling(1.3)      # Increase the scaling (default is 1.0)
        self.default_font = ctk.CTkFont("Roboto", 14)
        pywinstyles.apply_style(self, "acrylic") # window 11 theme 
        

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

        #key bindings
        self.bind("<Return>", lambda event: self.add_subject_btn.invoke())

        # CHART HOVER VARS
        # Add these as instance variables
        self._tooltip_id = None  # Canvas text item ID
        self._tooltip_x = 0
        self._tooltip_y = 0
        self._target_x = 0
        self._target_y = 0
        self._animation_active = False

        # GPA CALCULATOR DATA INIT
        self.subject_data = self.load_subjects_from_json("subject_data.json")

        self.gp_and_credits = []
        
    

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
                font=("Arial", 10, "bold"),
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
            delete_btn = ctk.CTkButton(row_frame, text="Delete", width=60,
                        command=lambda row=row_frame, sub=subject_info["subject"]: 
                        self.delete_subject(row, sub))
            print(subject_info["subject"])
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

            # Update gp_and_credits for GPA calculation
            # Remove existing entry if subject exists

            # GOAL: MAKE THE DELETE FUNCTION COMPATIBLE TO THE go_and_credits format
            
            self.gp_and_credits = [(i["gp"],i["credits"],i["subject"]) for i in self.subject_data]
            print(self.gp_and_credits)
            

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
            delete_btn = ctk.CTkButton(row_frame, text="Delete", width=60,
                        command=lambda row=row_frame, subject=subject: self.delete_subject(row, subject))
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
        print(total_points, total_credits)
    
    # POMODORO TIMER
    def setup_pomodoro_timer(self):
        tab = self.tabview.tab("Pomodoro Timer")
        
        # Timer display
        self.timer_label = ctk.CTkLabel(tab, text="25:00", 
                                    font=ctk.CTkFont(size=48, weight="bold"))
        self.timer_label
        self.timer_label.pack(pady=20)
        
        # Status display
        self.status_label = ctk.CTkLabel(tab, text="Ready to Start", 
                                    font=ctk.CTkFont(size=16))
        self.status_label.pack(pady=5)
        
        # Pomodoro counter
        self.pomodoro_counter_label = ctk.CTkLabel(tab, 
                                                text="Pomodoros Completed: 0/4",
                                                font=ctk.CTkFont(size=14))
        self.pomodoro_counter_label.pack(pady=5)
        
        # Control buttons
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="Start", 
                                    command=self.start_pomodoro)
        self.start_btn.pack(side="left", padx=10)
        
        self.reset_btn = ctk.CTkButton(btn_frame, text="Reset", 
                                    command=self.reset_pomodoro)
        self.reset_btn.pack(side="left", padx=10)
        
        self.finish_btn = ctk.CTkButton(btn_frame, text="Finish", 
                                    command=self.finish_current_session)
        self.finish_btn.pack(side="left", padx=10)
        
        # Timer variables
        self.pomodoro_count = 0
        self.time_left = 25 * 60  # 25 minutes in seconds
        self.timer_running = False
        self.is_break = False
        self.is_long_break = False
    
    def start_pomodoro(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
            self.start_btn.configure(text="Pause")
        else:
            self.timer_running = False
            self.start_btn.configure(text="Resume")

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.time_left -= 1
            self.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.timer_running = False
            self.start_btn.configure(text="Start")
            self.handle_session_complete()

    def handle_session_complete(self):
        if not self.is_break:
            # Completed a Pomodoro
            self.pomodoro_count += 1
            self.pomodoro_counter_label.configure(
                text=f"Pomodoros Completed: {self.pomodoro_count}/4"
            )
            
            if self.pomodoro_count % 4 == 0:
                # Time for a long break
                self.time_left = 30 * 60  # 30 minutes
                self.is_break = True
                self.is_long_break = True
                self.status_label.configure(text="Long Break - Time to recharge!")
                messagebox.showinfo("Pomodoro", 
                                "Great job! Time for a 30-minute break!")
                self.timer_label.configure(text="30:00")
            else:
                # Time for a short break
                
                self.time_left = 5 * 60  # 5 minutes
                self.is_break = True
                self.is_long_break = False
                self.status_label.configure(text="Short Break - Take 5!")
                messagebox.showinfo("Pomodoro", 
                                "Good work! Time for a 5-minute break!")
                self.timer_label.configure(text="05:00")
        else:
            # Break is over, start new Pomodoro
            self.time_left = 25 * 60
            self.is_break = False
            self.is_long_break = False
            self.status_label.configure(text="Focus Time!")
            messagebox.showinfo("Pomodoro", "Break's over! Ready for the next focus session?")
            self.timer_label.configure(text="25:00")

    def reset_pomodoro(self):
        self.timer_running = False
        self.time_left = 25 * 60
        self.is_break = False
        self.is_long_break = False
        self.pomodoro_count = 0
        self.timer_label.configure(text="25:00")
        self.start_btn.configure(text="Start")
        self.status_label.configure(text="Ready to Start")
        self.pomodoro_counter_label.configure(text="Pomodoros Completed: 0/4")

    def finish_current_session(self):
        if messagebox.askyesno("Finish Session", 
                            "Are you sure you want to finish the current session?"):
            self.time_left = 0
            self.timer_running = False
            self.handle_session_complete()

            # show break time
            self.start_btn.configure(text="Start")
        
    # TO-DO LIST
    def setup_todo_list(self):
        tab = self.tabview.tab("To-Do List")
        
        # Input frame
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(padx=10, pady=10, fill="x")
        
        self.task_entry = ctk.CTkEntry(input_frame, 
                                     placeholder_text="Enter new task...")
        self.task_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        add_task_btn = ctk.CTkButton(input_frame, text="Add Task", 
                                   command=self.add_task)
        add_task_btn.pack(side="right", padx=5)
        
        # Tasks list
        self.tasks_frame = ctk.CTkScrollableFrame(tab)
        self.tasks_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    
    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(fill="x", pady=5, padx=5)
            
            task_label = ctk.CTkLabel(task_frame, text=task_text)
            task_label.pack(side="left", padx=5)
            
            delete_btn = ctk.CTkButton(task_frame, text="✓", width=30,
                                     command=lambda: task_frame.destroy())
            delete_btn.pack(side="right", padx=5)
            
            self.task_entry.delete(0, 'end')

if __name__ == "__main__":
    app = SOLARIS()
    app.mainloop()
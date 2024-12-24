import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
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
            "scaling": 1.3
        }
    
    def load_settings(self):
        """Load settings from file or create with defaults if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            return self.default_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings
    
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


        # Window Configuration        
        self.title("SOLARIS - Study & Productivity Hub")
        width = self.winfo_screenwidth()  
        height = self.winfo_screenheight() 
        self.geometry(f"{width}x{height}")

   
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_widget_scaling(self.current_scaling)        

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
        self.tabview.add("To-Do List")
        self.tabview.add("Settings")

        # Initialize components
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
                "scaling": self.current_scaling
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
                
                # Update UI
                ctk.set_widget_scaling(1.3)
                ctk.set_appearance_mode("dark")
                
                # Update controls
                self.theme_var.set("Dark")
                self.scale_slider.set(1.3)
        
        # Apply Button
        apply_button = ctk.CTkButton(buttons_frame, text="Apply Settings",
                                    command=apply_settings,
                                    fg_color=self.COLORS["green"]["main"],
                                    hover_color=self.COLORS["green"]["hover"])
        apply_button.pack(side="right", padx=10)
        
        # Reset Button
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Defaults",
                                    command=reset_settings,
                                    fg_color=self.COLORS["red"]["main"],
                                    hover_color=self.COLORS["red"]["hover"])
        reset_button.pack(side="right", padx=10)


if __name__ == "__main__":
    app = SOLARIS()
    app.mainloop()
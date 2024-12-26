SOLARIS - Study & Productivity Hub


-------------------------Installation-----------------------------
1. Ensure you have Python 3.8 or newer installed on your system
2. Open a terminal/command prompt in the project directory by entering cmd on the address bar in the app directory(main.py)
3. Install the required dependencies by typing:
   pip install -r requirements.txt

*** IMPORTANT: open cmd in project directory NOT in pc user directory (reason: could not locate requirements.txt)***
***Alternative: use cd and paste the directory path to locate the requirements file***




Running the Application:
1. Navigate to the project directory in terminal/command prompt
2. Run the main application by typing:
   python main.py OR double clicking on the main.py file





App Description:


SOLARIS is a comprehensive study and productivity application that combines a GPA Calculator, Pomodoro Timer, and To-Do List manager in one convenient interface.

Features:
- GPA Calculator: Track and calculate your semester GPA and cumulative GPA
- Pomodoro Timer: Stay focused with customizable work/break intervals
- To-Do List: Manage your tasks with deadlines and status tracking
- Modern UI: Clean, customizable interface with light/dark mode support


Usage Guide:

GPA Calculator:
1. Select or create a new semester
2. Click "Add New Subject" to enter course details:
   - Enter subject name
   - Select grade from dropdown
   - Enter credit hours
3. View your GPA calculation and credit distribution in the pie chart
4. Edit or delete subjects as needed

Pomodoro Timer:
1. Click "Start" to begin a work session (default 25 minutes)
2. Take breaks when timer completes:
   - Short breaks (5 minutes) after each session
   - Long breaks (15 minutes) after 4 sessions
3. Customize timer settings:
   - Click "Settings" to adjust work/break durations
   - Track your session history on the right panel

To-Do List:
1. Click "Create New Task" to add a new item
2. Enter task details:
   - Task name
   - Deadline using calendar
   - Optional remarks
3. Mark tasks as complete when finished
4. View active and completed tasks in separate columns
5. Recreate or delete tasks as needed


Settings:
1. Access settings tab to customize:
   - Theme (Light/Dark mode)
   - Color scheme
   - Interface scaling
2. Click "Apply Settings" to save changes
3. Use "Reset to Defaults" to restore original settings



Troubleshooting:
If you encounter any issues:
1. Ensure all dependencies are correctly installed
2. Check you have proper permissions in the application directory
3. Verify Python version compatibility
4. Make sure no required files are missing:
   - main.py
   - solaris.py
   - tasks.json (created automatically)
   - subject_data.json (created automatically)




Support Files:
The application automatically creates and manages several JSON files:
- tasks.json: Stores to-do list data
- subject_data.json: Stores GPA calculator data
- pomodoro_history.json: Stores timer session history
- app_settings.json: Stores application preferences

These files are created automatically and should not be modified manually.



Notes:
- The application saves all data automatically
- Closing the application preserves all settings and data
- First-time startup creates necessary data files
- Windows 11 users get additional visual enhancements

For additional help or feature requests, please contact the developer. 011-10578676(TAN WY HANG)
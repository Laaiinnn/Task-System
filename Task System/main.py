import mysql.connector
from mysql.connector import Error

# Connect to MySQL Server
def connect():
    try:
        conn = mysql.connector.connect(
            host="yourlocalhostname",
            user="yourusername",
            password="yourpassword",
            database="yourdatabase"
        )
        if conn.is_connected():
            print("Connected to MySQL Server")
            return conn
    except Error as e:
        print(e)
        return None

# Initialize MySQL database
def init_database(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS projects 
                          (id INT AUTO_INCREMENT PRIMARY KEY,
                           name VARCHAR(255),
                           description TEXT,
                           status VARCHAR(50),
                           deadline DATE)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                          (id INT AUTO_INCREMENT PRIMARY KEY,
                           project_id INT,
                           description TEXT,
                           status VARCHAR(50),
                           assigned_to VARCHAR(255),
                           deadline DATE,
                           FOREIGN KEY(project_id) REFERENCES projects(id))''')
        print("MySQL database initialized")
    except Error as e:
        print(e)

# Function to submit a project request
def submit_project(conn, name, description, deadline):
    try:
        cursor = conn.cursor()
        status = 'Pending'
        cursor.execute('''INSERT INTO projects (name, description, status, deadline)
                          VALUES (%s, %s, %s, %s)''', (name, description, status, deadline))
        conn.commit()
        print("Project request submitted successfully!")
    except Error as e:
        print(e)

# Function to assign a task
def assign_task(conn, project_id, description, assigned_to, deadline):
    try:
        cursor = conn.cursor()
        status = 'Pending'
        cursor.execute('''INSERT INTO tasks (project_id, description, status, assigned_to, deadline)
                          VALUES (%s, %s, %s, %s, %s)''', (project_id, description, status, assigned_to, deadline))
        conn.commit()
        print("Task assigned successfully!")
    except Error as e:
        print(e)

# Function to update task progress
def update_task_progress(conn, task_id, status):
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE tasks SET status = %s WHERE id = %s''', (status, task_id))
        conn.commit()
        print("Task progress updated successfully!")
    except Error as e:
        print(e)

# Function to generate project report
def generate_project_report(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM projects''')
        projects = cursor.fetchall()
        for project in projects:
            print(f'Project ID: {project[0]}')
            print(f'Project Name: {project[1]}')
            print(f'Description: {project[2]}')
            print(f'Status: {project[3]}')
            print(f'Deadline: {project[4]}')
            print('\nTasks:')
            cursor.execute('''SELECT * FROM tasks WHERE project_id = %s''', (project[0],))
            tasks = cursor.fetchall()
            for task in tasks:
                print(f'Task ID: {task[0]}')
                print(f'Description: {task[2]}')
                print(f'Status: {task[3]}')
                print(f'Assigned to: {task[4]}')
                print(f'Deadline: {task[5]}')
                print('-----------------------------')
            print('=============================')
    except Error as e:
        print(e)

def main():
    conn = connect()
    if conn:
        init_database(conn)

        while True:
            print("\nTask System")
            print("1. Submit Project Request")
            print("2. Assign Task")
            print("3. Update Task Progress")
            print("4. Generate Project Report")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter project name: ")
                description = input("Enter project description: ")
                deadline = input("Enter project deadline (YYYY-MM-DD): ")
                submit_project(conn, name, description, deadline)

            elif choice == '2':
                project_id = int(input("Enter project ID: "))
                description = input("Enter task description: ")
                assigned_to = input("Enter assigned team member: ")
                deadline = input("Enter task deadline (YYYY-MM-DD): ")
                assign_task(conn, project_id, description, assigned_to, deadline)

            elif choice == '3':
                task_id = int(input("Enter task ID: "))
                status = input("Enter task status (In Progress/Completed): ")
                update_task_progress(conn, task_id, status)

            elif choice == '4':
                generate_project_report(conn)

            elif choice == '5':
                print("Exiting the system...")
                break

            else:
                print("Invalid choice. Please try again.")

        conn.close()

if __name__ == "__main__":
    main()
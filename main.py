import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar, Frame
import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Connection App")
        self.connection_details = {}
        self.create_connection_frame()
        self.create_screenshot_button()

    def create_connection_frame(self):
        self.connection_frame = tk.Frame(self.root)
        self.connection_frame.pack(padx=10, pady=10)

        tk.Label(self.connection_frame, text="Host:").grid(row=0, column=0, sticky="w")
        self.host_entry = tk.Entry(self.connection_frame)
        self.host_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.connection_frame, text="User:").grid(row=1, column=0, sticky="w")
        self.user_entry = tk.Entry(self.connection_frame)
        self.user_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.connection_frame, text="Password:").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self.connection_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.connection_frame, text="Database:").grid(row=3, column=0, sticky="w")
        self.database_entry = tk.Entry(self.connection_frame)
        self.database_entry.grid(row=3, column=1, pady=5)

        tk.Button(self.connection_frame, text="Connect", command=self.connect_to_database).grid(row=4, columnspan=2,
                                                                                                pady=10)

    def create_screenshot_button(self):
        self.screenshot_button = tk.Button(self.root, text="Take Screenshots", command=self.take_screenshots)
        self.screenshot_button.pack(pady=10)

    def create_scrollable_frame(self):
        canvas = Canvas(self.root)
        scrollbar = Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def connect_to_database(self):
        self.connection_details = {
            # 'host': self.host_entry.get(),
            # 'user': self.user_entry.get(),
            # 'password': self.password_entry.get(),
            # 'database': self.database_entry.get()

            'host': 'localhost',
            'user': 'kbtonmoy',
            'password': '6677',
            'database': 'forclient'
        }
        try:
            connection = mysql.connector.connect(**self.connection_details)
            if connection.is_connected():
                self.connection_frame.destroy()
                self.show_success_frame(connection)
        except Error as e:
            messagebox.showerror("Error", f"Error connecting to MySQL Database: {e}")

    def show_success_frame(self, connection):
        self.create_scrollable_frame()
        query = "SELECT id, root_domain FROM ecom_platform1"
        cursor = connection.cursor()
        cursor.execute(query)
        self.records = cursor.fetchall()

        self.checkboxes = []
        for i, (id, root_domain) in enumerate(self.records, start=1):
            tk.Label(self.scrollable_frame, text=f"{id}: {root_domain}").grid(row=i, column=0)
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.scrollable_frame, variable=var)
            chk.grid(row=i, column=1)
            self.checkboxes.append((var, root_domain))

        cursor.close()
        connection.close()

    def take_screenshots(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
        chrome_options.add_argument("--start-maximized")  # Start maximized
        chrome_options.add_argument("--window-size=1920,1080")  # Set window size
        chrome_options.add_argument("--hide-scrollbars")  # Set window size
        driver = webdriver.Chrome(options=chrome_options)

        os.makedirs('screenshots', exist_ok=True)  # Ensure the screenshot directory exists

        for var, url in self.checkboxes:
            if var.get():
                try:
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url  # Add http:// if not present
                    driver.get(url)
                    # Adjust the timeout as needed
                    driver.implicitly_wait(3)  # Wait for the page to load
                    screenshot_path = os.path.join('screenshots',
                                                   f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}.png")
                    driver.save_screenshot(screenshot_path)
                except Exception as e:
                    print(f"Error taking screenshot of {url}: {e}")

        driver.quit()
        messagebox.showinfo("Info", "Screenshots taken")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

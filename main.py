import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import os
from threading import Thread
import queue

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Connection App")
        self.connection_details = {}
        self.connection = None  # Database connection instance variable
        self.create_connection_frame()

# All Frames are here

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

    def prepare_videos_frame(self):
        # Placeholder method for "Prepare Videos" functionality
        messagebox.showinfo("Info", "Prepare Videos functionality not implemented yet")

    def upload_youtube_frame(self):
        # Placeholder method for "Upload on YouTube" functionality
        messagebox.showinfo("Info", "Upload on YouTube functionality not implemented yet")

    def show_success_frame(self):
        self.create_option_buttons()

    def take_screenshots_frame(self):
        self.clear_all_widgets()
        self.create_upload_csv_button()


# All Buttons are here

    def create_option_buttons(self):
        # New method to create buttons for "Take Screenshots", "Prepare Videos", "Upload on YouTube"
        tk.Button(self.root, text="Take Screenshots", command=self.take_screenshots_frame).pack()
        tk.Button(self.root, text="Prepare Videos", command=self.prepare_videos_frame).pack()
        tk.Button(self.root, text="Upload on YouTube", command=self.upload_youtube_frame).pack()

    def create_screenshot_button(self):
        self.screenshot_button = tk.Button(self.root, text="Start Capturing", command=self.take_screenshots)
        self.screenshot_button.pack(pady=10)

    def create_upload_csv_button(self):
        tk.Button(self.root, text="Upload CSV", command=self.upload_csv).pack()


# ALl logical Functions are here
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
            self.connection = mysql.connector.connect(**self.connection_details)
            if self.connection.is_connected():
                self.connection_frame.destroy()
                self.show_success_frame()
        except Error as e:
            messagebox.showerror("Error", f"Error connecting to MySQL Database: {e}")

    def upload_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.process_csv(filename)

    def process_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            urls = [row['url'] for row in reader]
            self.start_screenshot_process(urls)

    def start_screenshot_process(self, urls):
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=len(urls))
        self.progress_bar.pack()

        self.queue = queue.Queue()
        for url in urls:
            thread = Thread(target=self.take_screenshots, args=(url, self.queue))
            thread.start()

        self.root.after(100, self.check_queue)

    def check_queue(self):
        try:
            while True:
                message = self.queue.get_nowait()
                if message == "done":
                    self.progress_var.set(self.progress_var.get() + 1)
        except queue.Empty:
            pass

        if self.progress_var.get() == self.progress_bar['maximum']:
            self.progress_bar.destroy()
            messagebox.showinfo("Info", "Screenshots taken for all URLs and database updated")
        else:
            self.root.after(100, self.check_queue)

    def take_screenshots(self, url, queue):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--hide-scrollbars")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)  # Setting a timeout for page load

        os.makedirs('screenshots', exist_ok=True)


        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            driver.get(url)
            driver.implicitly_wait(3)  # Adjust the timeout as needed
            screenshot_filename = f"{url.replace('http://', '').replace('https://', '').replace('/', '_')}.png"
            screenshot_path = os.path.join('screenshots', screenshot_filename)
            driver.save_screenshot(screenshot_path)
            self.update_database(url, screenshot_path)
            driver.quit()
            self.queue.put("done")
        except Exception as e:
            print(f"Error taking screenshot of {url}: {e}")
        return True

    def update_database(self, url, screenshot_path):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO url_screenshots (root_domain, location) VALUES (%s, %s) ON DUPLICATE KEY UPDATE location = VALUES(location)"
            cursor.execute(query, (url, screenshot_path))
            self.connection.commit()
            cursor.close()
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating the database: {e}")


# Global Functions are here

    def clear_all_widgets(self):

        for widget in root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()


 # def create_scrollable_frame(self):
    #     canvas = Canvas(self.root)
    #     scrollbar = Scrollbar(self.root, orient="vertical", command=canvas.yview)
    #     self.scrollable_frame = Frame(canvas)
    #
    #     self.scrollable_frame.bind(
    #         "<Configure>",
    #         lambda e: canvas.configure(
    #             scrollregion=canvas.bbox("all")
    #         )
    #     )
    #     canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
    #     canvas.configure(yscrollcommand=scrollbar.set)
    #
    #     canvas.pack(side="left", fill="both", expand=True)
    #     scrollbar.pack(side="right", fill="y")
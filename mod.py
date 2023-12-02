import tkinter as tk
from tkinter import filedialog, messagebox

class YourClass:
    # ... other methods of your class ...

    def create_option_buttons(self):
        # ... your existing button creation code ...
        tk.Button(self.root, text="Prepare Videos", command=self.open_video_preparation_frame).pack()
        # ... rest of your button creation code ...

    def open_video_preparation_frame(self):
        # New window (or frame) for video preparation settings
        self.prep_window = tk.Toplevel(self.root)
        self.prep_window.title("Video Preparation Settings")

        # Input field for video file
        tk.Label(self.prep_window, text="Select a video file:").pack()
        self.video_path_var = tk.StringVar()
        tk.Entry(self.prep_window, textvariable=self.video_path_var, state='readonly').pack()
        tk.Button(self.prep_window, text="Browse", command=self.select_video_file).pack()

        # Input field for export directory
        tk.Label(self.prep_window, text="Select export directory:").pack()
        self.export_dir_var = tk.StringVar()
        tk.Entry(self.prep_window, textvariable=self.export_dir_var, state='readonly').pack()
        tk.Button(self.prep_window, text="Browse", command=self.select_export_directory).pack()

        # Submit button
        tk.Button(self.prep_window, text="Submit", command=self.save_video_settings).pack()

    def select_video_file(self):
        # Open file dialog to select a video file
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if file_path:
            self.video_path_var.set(file_path)

    def select_export_directory(self):
        # Open directory dialog to select an export directory
        directory = filedialog.askdirectory()
        if directory:
            self.export_dir_var.set(directory)

    def save_video_settings(self):
        # Save the video path and export directory
        self.video_path = self.video_path_var.get()
        self.export_dir = self.export_dir_var.get()
        self.prep_window.destroy()
        messagebox.showinfo("Info", "Video settings saved")

# ... rest of your class ...

# Example usage
# app = YourClass()
# app.root.mainloop()

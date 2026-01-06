import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime
import os
import cv2
import qrcode
from PIL import Image, ImageTk

# -----------------------------
# Configuration
# -----------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"
FILE_NAME = "attendance.txt"
QR_FOLDER = "QR_Codes"

if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

# -----------------------------
# Attendance Utility Functions
# -----------------------------
def get_next_id():
    if not os.path.exists(FILE_NAME):
        return 1
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()
    if not lines:
        return 1
    try:
        last_id = int(lines[-1].split(" - ")[0])
        return last_id + 1
    except:
        return 1

def save_attendance(name):
    student_id = get_next_id()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_NAME, "a") as file:
        file.write(f"{student_id} - {name} - {now}\n")
    # use a messagebox to inform
    messagebox.showinfo("Attendance Marked", f"{name} (ID: {student_id})")

# -----------------------------
# Admin Panel (same as before)
# -----------------------------
def open_admin_panel():
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("520x550")
    root.configure(bg="#eaf2f8")

    header = tk.Frame(root, bg="#2e86c1", height=80)
    header.pack(fill="x")

    tk.Label(header, text="🎓 Admin Control Panel", bg="#2e86c1",
             fg="white", font=("Helvetica", 20, "bold")).pack(pady=20)

    btn_frame = tk.Frame(root, bg="#eaf2f8")
    btn_frame.pack(pady=30)

    style = {
        "width": 30,
        "height": 2,
        "font": ("Arial", 11, "bold"),
        "relief": "ridge",
        "bd": 3,
        "cursor": "hand2"
    }

    tk.Button(btn_frame, text="📝 Mark Attendance (Manual)",
              command=lambda: mark_manual(), bg="#aed6f1", **style).pack(pady=8)

    tk.Button(btn_frame, text="📱 Generate QR Code",
              command=lambda: generate_qr(), bg="#85c1e9", **style).pack(pady=8)

    tk.Button(btn_frame, text="📋 View Attendance Records",
              command=view_attendance, bg="#f7dc6f", **style).pack(pady=8)

    tk.Button(btn_frame, text="❌ Delete Attendance (by ID)",
              command=delete_attendance, bg="#f1948a", **style).pack(pady=8)

    tk.Button(btn_frame, text="🔄 Back to Scanner",
              command=lambda: [root.destroy(), open_scanner_window()],
              bg="#82e0aa", **style).pack(pady=8)

    root.mainloop()

# -----------------------------
# Admin Utilities
# -----------------------------
def mark_manual():
    name = simpledialog.askstring("Manual Attendance", "Enter student name:")
    if name:
        save_attendance(name)

def generate_qr():
    roll = simpledialog.askstring("Generate QR", "Enter Roll Number:")
    name = simpledialog.askstring("Generate QR", "Enter Student Name:")
    course = simpledialog.askstring("Generate QR", "Enter Course (e.g., BCA/BBA):")
    semester = simpledialog.askstring("Generate QR", "Enter Semester (e.g., 1st, 2nd):")

    if not (roll and name and course and semester):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    # Ordered timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✔ Ordered QR data format
    qr_data = f"{roll}, {name}, {course}, {semester}, {now}"

    # Create QR
    qr_img = qrcode.make(qr_data)

    # File name
    file_name = f"{roll}_{name.replace(' ', '_')}_QR.png"
    file_path = os.path.join(QR_FOLDER, file_name)

    qr_img.save(file_path)

    messagebox.showinfo("QR Generated", f"QR Code saved as:\n{file_path}")

    roll = simpledialog.askstring("Generate QR", "Enter Roll Number:")
    name = simpledialog.askstring("Generate QR", "Enter Student Name:")
    course = simpledialog.askstring("Generate QR", "Enter Course (e.g., BCA/BBA):")
    semester = simpledialog.askstring("Generate QR", "Enter Semester (e.g., 1st, 2nd):")

    if not (roll and name and course and semester):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    # Ordered timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✔ Updated ordered QR data format
    qr_data = f"{roll}, {name}, {course}, {semester}, {now}"

    # Create QR
    qr_img = qrcode.make(qr_data)

    # Build filename
    file_name = f"{roll}_{name.replace(' ', '_')}_QR.png"
    file_path = os.path.join(QR_FOLDER, file_name)

    qr_img.save(file_path)

    messagebox.showinfo("QR Generated", f"QR Code saved as:\n{file_path}")

    roll = simpledialog.askstring("Generate QR", "Enter Roll Number:")
    name = simpledialog.askstring("Generate QR", "Enter Student Name:")
    course = simpledialog.askstring("Generate QR", "Enter Course (e.g., BCA/BBA):")
    semester = simpledialog.askstring("Generate QR", "Enter Semester (e.g., 1st, 2nd):")

    if not (roll and name and course and semester):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    # Generate timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create formatted QR data
    qr_data = f"{roll}, {name}, {course}, {semester}, {now}"

    # Create QR
    qr = qrcode.make(qr_data)

    # Save QR image
    file_name = f"{roll}_{name.replace(' ', '_')}_QR.png"
    file_path = os.path.join(QR_FOLDER, file_name)

    qr.save(file_path)

    messagebox.showinfo("QR Generated", f"QR Code saved as:\n{file_path}")

def view_attendance():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            data = file.read()
        if data.strip():
            # if too long, you may want to show in a scrolled Text widget; for now a messagebox
            messagebox.showinfo("Attendance Records", data)
        else:
            messagebox.showinfo("Attendance Records", "No records found.")
    else:
        messagebox.showinfo("Attendance Records", "File not found.")

def delete_attendance():
    id_to_delete = simpledialog.askstring("Delete Attendance", "Enter ID to delete:")
    if not id_to_delete:
        return
    if not os.path.exists(FILE_NAME):
        messagebox.showinfo("Delete Attendance", "Attendance file not found.")
        return
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()
    new_lines = [line for line in lines if not line.startswith(id_to_delete + " - ")]
    if len(new_lines) == len(lines):
        messagebox.showinfo("Delete Attendance", f"No record found with ID {id_to_delete}.")
        return
    with open(FILE_NAME, "w") as file:
        file.writelines(new_lines)
    messagebox.showinfo("Delete Attendance", f"Record ID {id_to_delete} deleted.")

# -----------------------------
# Scanner Window using Tkinter label (PIL ImageTk)
# -----------------------------
def open_scanner_window():
    # Create main scanner window
    scanner_window = tk.Tk()
    scanner_window.title("QR Attendance Scanner")
    scanner_window.geometry("900x620")
    scanner_window.configure(bg="#eaf2f8")

    # Title / Header
    header = tk.Frame(scanner_window, bg="#2e86c1", height=70)
    header.pack(fill="x")
    tk.Label(header, text="📷 QR Attendance Scanner", bg="#2e86c1",
             fg="white", font=("Helvetica", 18, "bold")).pack(pady=10)

    # Video display label
    video_label = tk.Label(scanner_window)
    video_label.pack(pady=10)

    # Admin button top-right
    admin_btn = tk.Button(
        scanner_window, text="Admin Panel", bg="#c39bd3",
        fg="white", font=("Arial", 11, "bold"),
        command=lambda: admin_login(scanner_window, cap)
    )
    # we'll place relative to window after a short delay to ensure geometry exists
    admin_btn.place(x=780, y=20)

    # Info label
    info = tk.Label(scanner_window, text="Point camera to a student's QR code. (Press window close to stop.)",
                    bg="#eaf2f8", font=("Arial", 10))
    info.pack()

    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot access camera. Check connection or camera index.")
        scanner_window.destroy()
        return

    detector = cv2.QRCodeDetector()

    def on_close():
        # release camera and close windows cleanly
        try:
            if cap and cap.isOpened():
                cap.release()
        except:
            pass
        scanner_window.destroy()

    scanner_window.protocol("WM_DELETE_WINDOW", on_close)

    # Keep track of last-decoded content to avoid double-marking same QR continuously
    last_data = {"value": None, "time": None}

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            video_label.config(text="Failed to read from camera.")
            return

        frame_display = cv2.resize(frame, (780, 480))

        # Detect QR
        data, bbox, _ = detector.detectAndDecode(frame)

        # Draw green bounding box
        if bbox is not None:
            pts = bbox[0].astype(int)
            for i in range(len(pts)):
                cv2.line(frame_display, tuple(pts[i]), tuple(pts[(i+1) % len(pts)]),
                         (0, 255, 0), 3)

        # ✔ If QR found
        if data:
            text = data.strip()

            # Avoid double scan
            if text and text != last_data["value"]:
                last_data["value"] = text

                # Extract ordered QR data
                parts = text.split(",")

                if len(parts) >= 4:
                    roll = parts[0].strip()
                    name = parts[1].strip()
                    course = parts[2].strip()
                    semester = parts[3].strip()

                    formatted = f"{roll} - {name} - {course} - {semester}"
                    save_attendance(formatted)
                else:
                    # fallback
                    save_attendance(text)

        # Convert to Tkinter display
        frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        video_label.after(15, update_frame)

    # start loop
    update_frame()
    scanner_window.mainloop()

# -----------------------------
# Admin Login (single dialog, not two sequential simpledialogs)
# -----------------------------
def admin_login(scanner_window, cap):
    # custom modal dialog (Toplevel) for username+password
    dialog = tk.Toplevel(scanner_window)
    dialog.transient(scanner_window)
    dialog.grab_set()
    dialog.title("Admin Login")
    dialog.geometry("320x180")
    dialog.resizable(False, False)

    tk.Label(dialog, text="Enter admin credentials", font=("Arial", 12, "bold")).pack(pady=8)

    tk.Label(dialog, text="Username:", anchor="w").pack(fill="x", padx=12)
    user_entry = tk.Entry(dialog)
    user_entry.pack(fill="x", padx=12, pady=(0,8))

    tk.Label(dialog, text="Password:", anchor="w").pack(fill="x", padx=12)
    pass_entry = tk.Entry(dialog, show="*")
    pass_entry.pack(fill="x", padx=12, pady=(0,12))

    result = {"ok": False}

    def on_ok():
        u = user_entry.get()
        p = pass_entry.get()
        if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
            result["ok"] = True
            dialog.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            # keep dialog open for retry

    def on_cancel():
        dialog.destroy()

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=6)
    tk.Button(btn_frame, text="Login", width=10, command=on_ok).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel).pack(side="left", padx=6)

    # focus username entry
    user_entry.focus_set()
    dialog.wait_window()

    if result["ok"]:
        # stop camera and close scanner window before opening admin panel
        try:
            if cap and cap.isOpened():
                cap.release()
        except:
            pass
        # destroy scanner window (its parent)
        try:
            scanner_window.destroy()
        except:
            pass
        open_admin_panel()

# -----------------------------
# Start app
# -----------------------------
if __name__ == "__main__":
    open_scanner_window()

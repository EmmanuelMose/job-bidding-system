import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import re
import phonenumbers
import locale




# Function to clear the right frame
def clear_frame():
    for widget in right_frame.winfo_children():
        widget.destroy()

def get_country_code():
    try:
        country_code = locale.getdefaultlocale()[0].split('_')[1]
        example_number = phonenumbers.example_number_for_region(country_code)
        if example_number:
            return f"+{example_number.country_code}"
        else:
            return "+1"  # Default to US if detection fails
    except Exception:
        return "+1"
# ==================== COMPLAIN ====================
def submit_complaint():
    complaint = complaint_text.get("1.0", "end-1c")
    if not complaint.strip():
        messagebox.showerror("Error", "Complaint cannot be empty!")
        return
    messagebox.showinfo("Success", "Complaint submitted successfully!")
    complaint_text.delete("1.0", "end")

def show_complain():
    clear_frame()

    tk.Label(right_frame, text="Type your Complaint:", font=("Arial", 14)).pack(anchor="w", pady=5, padx=10)

    global complaint_text
    complaint_text = tk.Text(right_frame, height=10, width=70, wrap="word", bd=2, relief="groove")
    complaint_text.pack(padx=10, pady=5)

    tk.Button(right_frame, text="Submit Complaint", command=submit_complaint, bg="green", fg="white", padx=20, pady=5).pack(pady=10)

# ==================== PROFILE ====================
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        load_image(file_path)

def modify_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        load_image(file_path)

def load_image(file_path):
    global profile_img
    img = Image.open(file_path)
    img = img.resize((20, 20), Image.LANCZOS)  # Keep size unchanged
    profile_img = ImageTk.PhotoImage(img)
    image_label.config(image=profile_img)
    image_label.image = profile_img

# ==================== PROFILE ====================
def validate_phone():
    global entry_phone, country_code_var  # Declare globals here
    phone = entry_phone.get()
    full_phone = f"{country_code_var.get()}{phone}"  # Use country_code_var here

    try:
        parsed_number = phonenumbers.parse(full_phone, None)
        if phonenumbers.is_valid_number(parsed_number):
            messagebox.showinfo("Success", "Phone number is valid!")
        else:
            messagebox.showerror("Error", "Invalid phone number format!")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid phone number: {e}")

def save_profile():
    global entry_phone, country_code_var  # Declare globals here
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    id_no = entry_id.get()
    location = entry_location.get()
    phone = entry_phone.get()

    if not (first_name and last_name and id_no and location and phone):
        messagebox.showerror("Error", "All fields are required!")
        return

    full_phone = f"{country_code_var.get()}{phone}"  # Use country_code_var here

    try:
        parsed_number = phonenumbers.parse(full_phone, None)
        if not phonenumbers.is_valid_number(parsed_number):
            messagebox.showerror("Error", "Invalid phone number format!")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Invalid phone number: {e}")
        return

    messagebox.showinfo("Success", f"Profile for {first_name} {last_name} saved successfully!")

# ... (rest of your code remains the same)

def show_profile():
    clear_frame()

    form_frame = tk.Frame(right_frame)
    form_frame.pack(pady=20, padx=30, fill="both", expand=True)

    left_frame = tk.Frame(form_frame)
    left_frame.grid(row=0, column=0, sticky="nw", padx=(0, 20))

    # First Name
    tk.Label(left_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=5)
    global entry_first_name
    entry_first_name = tk.Entry(left_frame, width=40)
    entry_first_name.grid(row=0, column=1, pady=5)

    # Last Name
    tk.Label(left_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=5)
    global entry_last_name
    entry_last_name = tk.Entry(left_frame, width=40)
    entry_last_name.grid(row=1, column=1, pady=5)

    # ID Number
    tk.Label(left_frame, text="ID No:").grid(row=2, column=0, sticky="w", pady=5)
    global entry_id
    entry_id = tk.Entry(left_frame, width=40)
    entry_id.grid(row=2, column=1, pady=5)

    # Location
    tk.Label(left_frame, text="Location:").grid(row=3, column=0, sticky="w", pady=5)
    global entry_location
    entry_location = tk.Entry(left_frame, width=40)
    entry_location.grid(row=3, column=1, pady=5)

    # Phone Number
    tk.Label(left_frame, text="Phone Number:").grid(row=4, column=0, sticky="w", pady=5)

    # Country Code Dropdown
    global country_code_var
    country_code = tk.StringVar()
    country_code.set(get_country_code())

    country_code_dropdown = ttk.Combobox(left_frame, textvariable=country_code, width=5)
    country_code_dropdown.grid(row=4, column=1, sticky="w", pady=5)

    # Phone Number Entry
    global entry_phone
    entry_phone = tk.Entry(left_frame, width=30)
    entry_phone.grid(row=4, column=1, pady=5, padx=(60, 0), sticky="w")

    # Validate Button
    validate_button = tk.Button(left_frame, text="Validate", command=validate_phone, bg="#555555", fg="white", padx=10,
                                pady=5)
    validate_button.grid(row=4, column=2, padx=5, sticky="w")

    # Profile picture section
    right_frame_inner = tk.Frame(form_frame)
    right_frame_inner.grid(row=0, column=1, sticky="ne", padx=(20, 0))

    tk.Label(right_frame_inner, text="Profile Image:").pack(anchor="center")
    global image_label
    image_label = tk.Label(right_frame_inner, width=20, height=20, relief="ridge", bg="#ddd")
    image_label.pack(pady=5)

    button_frame = tk.Frame(right_frame_inner)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="Upload", command=upload_image, bg="#555555", fg="white").pack(side="left", padx=5)
    tk.Button(button_frame, text="Modify", command=modify_image, bg="#555555", fg="white").pack(side="left", padx=5)

    tk.Button(form_frame, text="Save", command=save_profile, bg="#4CAF50", fg="white", padx=20, pady=5).grid(row=1, column=0, columnspan=2, pady=10)

# ==================== POST JOB ====================
def show_post_job():
    clear_frame()
    tk.Label(right_frame, text="Post Job Feature Coming Soon!", font=("Arial", 14)).pack(pady=20)

# ==================== JOB STATUS ====================
# ==================== POST JOB ====================
def show_post_job():
    clear_frame()

    form_frame = tk.Frame(right_frame)
    form_frame.pack(pady=20, padx=30, fill="both", expand=True)

    field_width = 40

    # Category
    tk.Label(form_frame, text="Category:").grid(row=0, column=0, sticky="w", pady=5)
    category = ttk.Combobox(form_frame, values=["Software", "Design", "Writing", "Marketing"], width=field_width)
    category.grid(row=0, column=1, pady=5)

    # Price and Pay Button
    tk.Label(form_frame, text="Price:").grid(row=1, column=0, sticky="w", pady=5)
    price = tk.Entry(form_frame, width=field_width - 5)
    price.grid(row=1, column=1, pady=5)
    tk.Button(form_frame, text="Pay", bg="#555555", fg="white").grid(row=1, column=2, padx=5)

    # Workload
    tk.Label(form_frame, text="Workload:").grid(row=2, column=0, sticky="w", pady=5)
    workload = tk.Entry(form_frame, width=field_width)
    workload.grid(row=2, column=1, pady=5)

    # Location
    tk.Label(form_frame, text="Location:").grid(row=3, column=0, sticky="w", pady=5)
    location = ttk.Combobox(form_frame, values=["Remote", "On-Site"], width=field_width)
    location.grid(row=3, column=1, pady=5)

    # Urgency
    tk.Label(form_frame, text="Urgency:").grid(row=4, column=0, sticky="w", pady=5)
    urgency = ttk.Combobox(form_frame, values=["Low", "Medium", "High"], width=field_width)
    urgency.grid(row=4, column=1, pady=5)

    # Post Button
    tk.Button(form_frame, text="Post", bg="#4CAF50", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

# ==================== JOB STATUS ====================
def show_job_status():
    clear_frame()

    tk.Label(right_frame, text="Select Job Status:", font=("Arial", 14)).pack(anchor="w", pady=5, padx=10)

    # Dropdown for job status
    status_options = ["Pending", "In Progress", "Completed", "Cancelled"]
    status_combobox = ttk.Combobox(right_frame, values=status_options, width=30)
    status_combobox.pack(pady=5, padx=10)

    def display_status():
        selected_status = status_combobox.get()
        if selected_status:
            messagebox.showinfo("Job Status", f"Selected Job Status: {selected_status}")
        else:
            messagebox.showwarning("Warning", "Please select a job status.")

    tk.Button(right_frame, text="Check Status", command=display_status, bg="#4CAF50", fg="white", padx=20, pady=5).pack(pady=10)

# ==================== MAIN WINDOW ====================
root = tk.Tk()
root.title("Admin Dashboard")
root.geometry("1000x600")

# Left navigation panel
nav_frame = tk.Frame(root, bg="#333333", width=250, height=600)
nav_frame.pack(side="left", fill="y")

# Right content area
right_frame = tk.Frame(root, bg="#ffffff", width=750, height=600)
right_frame.pack(side="right", fill="both", expand=True)

# Navigation buttons
nav_buttons = [
    ("Profile", show_profile),
    ("Post Job", show_post_job),
    ("Complain", show_complain),
    ("Job Status", show_job_status) # Fixed to call the correct function
]

for text, command in nav_buttons:
    tk.Button(nav_frame, text=text, command=command, bg="#555555", fg="white", width=20, height=2).pack(pady=5)

# Load Profile page by default
show_profile()

# Run the app
root.mainloop()
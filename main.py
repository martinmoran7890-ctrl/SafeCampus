import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
from database import get_connection

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SafeCampusApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SafeCampus — Campus Emergency Information System")
        self.geometry("1400x850")
        self.resizable(True, True)
        self.current_user = None
        self.all_reports = []
        self.filtered_reports = []

        self.sidebar_frame = None
        self.main_content_frame = ctk.CTkFrame(self, fg_color="#0f172a")
        self.main_content_frame.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_main_content(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

    # ========== LOGIN SCREEN ==========
    def show_login_screen(self):
        if self.sidebar_frame:
            self.sidebar_frame.pack_forget()
            self.sidebar_frame = None
        self.clear_main_content()
        self.main_content_frame.pack(fill="both", expand=True)

        frame = ctk.CTkFrame(self.main_content_frame, fg_color="#1e293b", corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="SafeCampus", font=("Arial", 28, "bold"), text_color="#3b82f6").pack(pady=(30, 5))
        ctk.CTkLabel(frame, text="Campus Emergency Information System", font=("Arial", 14), text_color="#cbd5e1").pack(pady=(0, 30))

        ctk.CTkLabel(frame, text="Username:", font=("Arial", 12), text_color="#f8fafc").pack(anchor="w", padx=40)
        username_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter username")
        username_entry.pack(padx=40, pady=(5, 15))

        ctk.CTkLabel(frame, text="Password:", font=("Arial", 12), text_color="#f8fafc").pack(anchor="w", padx=40)
        password_entry = ctk.CTkEntry(frame, width=300, show="*", placeholder_text="Enter password")
        password_entry.pack(padx=40, pady=(5, 25))

        def do_login():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            if not u or not p:
                messagebox.showwarning("Incomplete", "Fill in username and password")
                return
            conn = get_connection()
            if not conn:
                messagebox.showerror("Error", "Cannot connect to database\nCheck if MySQL is running")
                return
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
                user = cur.fetchone()
                cur.close()
                conn.close()
                if user:
                    self.current_user = user
                    self.build_sidebar()
                    self.show_dashboard()
                else:
                    messagebox.showerror("Login Failed", "Invalid Username or Password")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(frame, text="Login", command=do_login,
                      fg_color="#3b82f6", hover_color="#2563eb",
                      font=("Arial", 12, "bold"), width=300).pack(pady=(0, 10))
        ctk.CTkButton(frame, text="Create New Account", command=self.show_register_screen,
                      fg_color="#10b981", hover_color="#059669",
                      font=("Arial", 11, "bold"), width=300).pack(pady=(0, 30))

    # ========== REGISTER SCREEN ==========
    def show_register_screen(self):
        self.clear_main_content()
        frame = ctk.CTkFrame(self.main_content_frame, fg_color="#1e293b", corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Create New Account", font=("Arial", 22, "bold"), text_color="#10b981").pack(pady=(30, 25))

        ctk.CTkLabel(frame, text="Full Name:", font=("Arial", 11), text_color="#f8fafc").pack(anchor="w", padx=40)
        fullname_entry = ctk.CTkEntry(frame, width=300)
        fullname_entry.pack(padx=40, pady=(5, 12))

        ctk.CTkLabel(frame, text="Username:", font=("Arial", 11), text_color="#f8fafc").pack(anchor="w", padx=40)
        user_entry = ctk.CTkEntry(frame, width=300)
        user_entry.pack(padx=40, pady=(5, 12))

        ctk.CTkLabel(frame, text="Password:", font=("Arial", 11), text_color="#f8fafc").pack(anchor="w", padx=40)
        pass_entry = ctk.CTkEntry(frame, width=300, show="*")
        pass_entry.pack(padx=40, pady=(5, 12))

        ctk.CTkLabel(frame, text="Role:", font=("Arial", 11), text_color="#f8fafc").pack(anchor="w", padx=40)
        role_menu = ctk.CTkOptionMenu(frame, values=["student", "staff", "admin"])
        role_menu.set("student")
        role_menu.pack(padx=40, pady=(5, 25))

        def do_register():
            full = fullname_entry.get().strip()
            user = user_entry.get().strip()
            pwd = pass_entry.get().strip()
            role = role_menu.get()
            if not full or not user or not pwd:
                messagebox.showwarning("Incomplete", "Fill in all fields")
                return
            conn = get_connection()
            if not conn:
                messagebox.showerror("Error", "Cannot connect to database")
                return
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, password, full_name, role) VALUES (%s, %s, %s, %s)",
                            (user, pwd, full, role))
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Success", "Account created!")
                self.show_login_screen()
            except Exception as e:
                if "Duplicate" in str(e):
                    messagebox.showerror("Exists", "Username already taken")
                else:
                    messagebox.showerror("Error", str(e))

        ctk.CTkButton(frame, text="Create Account", command=do_register,
                      fg_color="#10b981", hover_color="#059669", width=300).pack(pady=(0, 10))
        ctk.CTkButton(frame, text="Back to Login", command=self.show_login_screen,
                      fg_color="#64748b", width=300).pack(pady=(0, 30))

    # ========== SIDEBAR ==========
    def build_sidebar(self):
        self.clear_main_content()
        self.main_content_frame.pack_forget()
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1e293b")
        self.sidebar_frame.pack(side="left", fill="y")
        self.main_content_frame = ctk.CTkFrame(self, fg_color="#0f172a")
        self.main_content_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.sidebar_frame, text="SafeCampus", font=("Arial", 18, "bold"), text_color="#3b82f6").pack(pady=(30, 5))
        ctk.CTkLabel(self.sidebar_frame, text=f"Welcome, {self.current_user['full_name']}",
                     font=("Arial", 10), text_color="#cbd5e1").pack(pady=(0, 30))
        ctk.CTkLabel(self.sidebar_frame, text=f"Role: {self.current_user['role'].upper()}",
                     font=("Arial", 9, "bold"), text_color="#94a3b8").pack(pady=(0, 20))

        pages = [
            ("Dashboard", self.show_dashboard),
            ("Campus Information", self.show_campus_info),
            ("Submit Report", self.show_submit_report),
            ("Emergency Alerts", self.show_emergency_alerts),
            ("Incident Logs", self.show_incident_logs),
            ("User Management", self.show_user_management)
        ]
        if self.current_user["role"] not in ["admin", "staff"]:
            pages = [p for p in pages if p[0] != "User Management"]
        for name, cmd in pages:
            ctk.CTkButton(self.sidebar_frame, text=name, command=cmd,
                          fg_color="transparent", hover_color="#334155",
                          anchor="w", font=("Arial", 11)).pack(fill="x", padx=15, pady=3)
        ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.show_login_screen,
                      fg_color="#ef4444", hover_color="#dc2626").pack(side="bottom", pady=30)

    # ========== DASHBOARD ==========
    def show_dashboard(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content_frame, text="Main Dashboard", font=("Arial", 22, "bold")).pack(anchor="w", padx=30, pady=(30, 20))
        conn = get_connection()
        stats = {}
        if conn:
            try:
                cur = conn.cursor()
                for table, label in [
                    ("emergency_contacts", "Contacts"),
                    ("safety_information", "Safety Info"),
                    ("emergency_reports", "Reports"),
                    ("emergency_alerts", "Alerts")
                ]:
                    cur.execute(f"SELECT COUNT(*) FROM {table}")
                    stats[label] = cur.fetchone()[0]
                cur.close()
                conn.close()
            except:
                stats = {"Contacts": 0, "Safety Info": 0, "Reports": 0, "Alerts": 0}
        cards_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30)
        for idx, (title, val) in enumerate(stats.items()):
            card = ctk.CTkFrame(cards_frame, fg_color="#1e293b", corner_radius=8)
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")
            cards_frame.grid_columnconfigure(idx, weight=1)
            ctk.CTkLabel(card, text=str(val), font=("Arial", 28, "bold"), text_color="#3b82f6").pack(pady=(20, 5))
            ctk.CTkLabel(card, text=title, font=("Arial", 12), text_color="#cbd5e1").pack(pady=(0, 20))

    # ========== CAMPUS INFORMATION ==========
    def show_campus_info(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content_frame, text="Campus Information", font=("Arial", 22, "bold")).pack(anchor="w", padx=30, pady=(30, 10))
        conn = get_connection()
        info_list = []
        if conn:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM safety_information ORDER BY id")
                info_list = cur.fetchall()
                cur.close()
                conn.close()
            except:
                pass
        scroll_frame = ctk.CTkScrollableFrame(self.main_content_frame)
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        if not info_list:
            ctk.CTkLabel(scroll_frame, text="No information available.", text_color="#94a3b8").pack(pady=20)
            return
        for info in info_list:
            card = ctk.CTkFrame(scroll_frame, fg_color="#1e293b", corner_radius=8)
            card.pack(fill="x", pady=8)
            ctk.CTkLabel(card, text=info["title"], font=("Arial", 14, "bold"), text_color="#3b82f6").pack(anchor="w", padx=20, pady=(15, 5))
            ctk.CTkLabel(card, text=f"Category: {info['category']}", text_color="#94a3b8").pack(anchor="w", padx=20)
            ctk.CTkLabel(card, text=info["details"], wraplength=1100, text_color="#e2e8f0").pack(anchor="w", padx=20, pady=(5, 15))

    # ========== SUBMIT REPORT ==========
    def show_submit_report(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content_frame, text="Submit Emergency Report", font=("Arial", 22, "bold")).pack(anchor="w", padx=30, pady=(30, 10))

        def submit():
            loc = loc_entry.get().strip()
            typ = type_menu.get()
            desc = desc_text.get("1.0", "end").strip()
            if not loc or not typ:
                messagebox.showwarning("Incomplete", "Fill location and type")
                return
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO emergency_reports (reporter_name, location, incident_type, description, status) VALUES (%s, %s, %s, %s, %s)",
                                (self.current_user["full_name"], loc, typ, desc, "Pending"))
                    conn.commit()
                    cur.close()
                    conn.close()
                    messagebox.showinfo("Submitted", "Report saved successfully!")
                    loc_entry.delete(0, "end")
                    desc_text.delete("1.0", "end")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        form = ctk.CTkFrame(self.main_content_frame, fg_color="#1e293b", corner_radius=8)
        form.pack(fill="x", padx=30)
        ctk.CTkLabel(form, text="Incident Type:", font=("Arial", 11, "bold")).pack(anchor="w", padx=25, pady=(20, 5))
        type_menu = ctk.CTkOptionMenu(form, values=["Accident", "Fire", "Medical", "Security", "Other"])
        type_menu.set("Accident")
        type_menu.pack(padx=25, pady=(0, 15))
        ctk.CTkLabel(form, text="Location:", font=("Arial", 11, "bold")).pack(anchor="w", padx=25, pady=(5, 5))
        loc_entry = ctk.CTkEntry(form, width=600)
        loc_entry.pack(padx=25, pady=(0, 15))
        ctk.CTkLabel(form, text="Description:", font=("Arial", 11, "bold")).pack(anchor="w", padx=25, pady=(5, 5))
        desc_text = ctk.CTkTextbox(form, width=600, height=120)
        desc_text.pack(padx=25, pady=(0, 20))
        ctk.CTkButton(form, text="Submit Report", command=submit, fg_color="#10b981").pack(pady=(0, 25))

    # ========== INCIDENT LOGS — FILTER FIXED ==========
    def show_incident_logs(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content_frame, text="Incident Logs", font=("Arial", 22, "bold")).pack(anchor="w", padx=30, pady=(30, 10))

        conn = get_connection()
        self.all_reports = []
        if conn:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM emergency_reports ORDER BY created_at DESC")
                self.all_reports = cur.fetchall()
                cur.close()
                conn.close()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))
                self.all_reports = []
        self.filtered_reports = self.all_reports.copy()

        filter_frame = ctk.CTkFrame(self.main_content_frame, fg_color="#1e293b", corner_radius=8)
        filter_frame.pack(fill="x", padx=30, pady=(0, 10))
        ctk.CTkLabel(filter_frame, text="Filter by Status:", font=("Arial", 11)).pack(side="left", padx=20, pady=15)
        status_filter = ctk.CTkOptionMenu(filter_frame, values=["All", "Pending", "In Progress", "Resolved"])
        status_filter.set("All")
        status_filter.pack(side="left", padx=(0, 15))

        container = ctk.CTkFrame(self.main_content_frame)
        container.pack(fill="both", expand=True, padx=30)
        cols = ("ID", "Reporter", "Location", "Type", "Status", "Date")
        tree = ttk.Treeview(container, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
        tree.column("ID", width=50)
        tree.column("Reporter", width=150)
        tree.column("Location", width=200)
        tree.column("Type", width=120)
        tree.column("Status", width=120)
        tree.column("Date", width=180)
        tree.pack(fill="both", expand=True)

        def refresh_table():
            for item in tree.get_children():
                tree.delete(item)
            for r in self.filtered_reports:
                tree.insert("", "end", values=(
                    r["id"], r.get("reporter_name", "N/A"), r["location"],
                    r["incident_type"], r["status"], str(r["created_at"])[:19]
                ))

        def apply_filter():
            sel = status_filter.get()
            if sel == "All":
                self.filtered_reports = self.all_reports.copy()
            else:
                self.filtered_reports = [r for r in self.all_reports if r["status"] == sel]
            refresh_table()
            messagebox.showinfo("Filter Applied ✅", f"Showing {len(self.filtered_reports)} report(s)")

        ctk.CTkButton(filter_frame, text="Apply Filter", command=apply_filter, fg_color="#3b82f6").pack(side="left", padx=5)

        def mark_resolved():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Notice", "Select a report first")
                return
            rid = tree.item(sel[0])["values"][0]
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE emergency_reports SET status=%s WHERE id=%s", ("Resolved", rid))
                    conn.commit()
                    cur.close()
                    conn.close()
                    messagebox.showinfo("Updated ✅", "Status changed to Resolved")
                    self.show_incident_logs()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        def export_reports():
            if not self.filtered_reports:
                messagebox.showinfo("Notice", "No data to export")
                return
            path = filedialog.asksaveasfilename(defaultextension=".csv",
                initialfile=f"Incident_Logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            if not path:
                return
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["ID", "Reporter", "Location", "Type", "Status", "Description", "Date"])
                for r in self.filtered_reports:
                    w.writerow([r["id"], r.get("reporter_name", ""), r["location"], r["incident_type"],
                                r["status"], r.get("description", ""), str(r["created_at"])[:19]])
            messagebox.showinfo("Exported ✅", f"Saved to:\n{path}")

        def print_preview():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Notice", "Select a report first")
                return
            rid = tree.item(sel[0])["values"][0]
            r = next((x for x in self.filtered_reports if x["id"] == rid), None)
            if not r:
                return
            txt = f"""
INCIDENT REPORT DETAILS
ID: {r['id']}
Reporter: {r.get('reporter_name', 'N/A')}
Location: {r['location']}
Type: {r['incident_type']}
Status: {r['status']}
Date: {str(r['created_at'])[:19]}

Description:
{r.get('description', '')}
"""
            win = ctk.CTkToplevel(self)
            win.title("Report Preview")
            win.geometry("600x450")
            txt_box = ctk.CTkTextbox(win)
            txt_box.pack(fill="both", expand=True, padx=10, pady=10)
            txt_box.insert("1.0", txt)
            txt_box.configure(state="disabled")

        btn_frame = ctk.CTkFrame(self.main_content_frame)
        btn_frame.pack(fill="x", padx=30, pady=10)
        if self.current_user["role"] in ["admin", "staff"]:
            ctk.CTkButton(btn_frame, text="Mark as Resolved", command=mark_resolved, fg_color="#10b981").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Export CSV", command=export_reports, fg_color="#3b82f6").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="View Details", command=print_preview, fg_color="#f59e0b").pack(side="left", padx=5)

        refresh_table()

    # ========== EMERGENCY ALERTS — WALANG PUTOL! ==========
    def show_emergency_alerts(self):
        self.clear_main_content()
        ctk.CTkLabel(self.main_content_frame, text="Emergency Alerts", font=("Arial", 22, "bold")).pack(anchor="w", padx=30, pady=(30, 10))

        if self.current_user["role"] in ["admin", "staff"]:
            def post_alert():
                t = title_entry.get().strip()
                lvl = level_menu.get()
                msg = msg_text.get("1.0", "end").strip()
                if not t or not msg:
                    messagebox.showwarning("Incomplete", "Fill in title and message")
                    return
                conn = get_connection()
                if conn:
                    try:
                        cur = conn.cursor()
                        cur.execute("INSERT INTO emergency_alerts (alert_title, alert_level, message) VALUES (%s, %s, %s)", (t, lvl, msg))
                        conn.commit()
                        cur.close()
                        conn.close()
                        messagebox.showinfo("Posted ✅", "Alert has been sent!")
                        title_entry.delete(0, "end")
                        msg_text.delete("1.0", "end")
                        self.show_emergency_alerts()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            post_frame = ctk.CTkFrame(self.main_content_frame, fg_color="#1e293b", corner_radius=8)
            post_frame.pack(fill="x", padx=30, pady=(0, 20))
            ctk.CTkLabel(post_frame, text="Post New Alert", font=("Arial", 13, "bold")).pack(anchor="w", padx=20, pady=(15, 10))
            row = ctk.CTkFrame(post_frame)
            row.pack(fill="x", padx=20, pady=(0, 10))
            ctk.CTkLabel(row, text="Title:").grid(row=0, column=0, sticky="w")
            title_entry = ctk.CTkEntry(row)
            title_entry.grid(row=0, column=1, padx=5, sticky="ew")
            ctk.CTkLabel(row, text="Level:").grid(row=0, column=2, sticky="w", padx=(15, 0))
            level_menu = ctk.CTkOptionMenu(row, values=["Critical", "Warning", "Info"])
            level_menu.set("Warning")
            level_menu.grid(row=0, column=3)
            row.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(post_frame, text="Message:").pack(anchor="w", padx=20)
            msg_text = ctk.CTkTextbox(post_frame, height=80)
            msg_text.pack(fill="x", padx=20, pady=(5, 10))
            ctk.CTkButton(post_frame, text="Send Alert", command=post_alert, fg_color="#f59e0b").pack(pady=(0, 15))

        conn = get_connection()
        alerts = []
        if conn:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM emergency_alerts ORDER BY posted_at DESC")
                alerts = cur.fetchall()
                cur.close()
                conn.close()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

        list_frame = ctk.CTkFrame(self.main_content_frame)
        list_frame.pack(fill="both", expand=True, padx=30)
        cols = ("ID", "Title", "Level", "Message", "Posted")
        tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)

        # ✅ Sobrang lapad — kasya lahat ng mensahe, WALANG PUTOL!
        tree.column("ID", width=50)
        tree.column("Title", width=250)
        tree.column("Level", width=100)
        tree.column("Message", width=900)
        tree.column("Posted", width=180)
        tree.pack(fill="both", expand=True)

        def dismiss_alert():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Notice", "Select an alert first")
                return
            aid = tree.item(sel[0])["values"][0]
            if not messagebox.askyesno("Confirm", "Dismiss this alert?"):
                return
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM emergency_alerts WHERE id=%s", (aid,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    self.show_emergency_alerts()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        if self.current_user["role"] in ["admin", "staff"]:
            ctk.CTkButton(list_frame, text="Dismiss Selected", command=dismiss_alert, fg_color="#ef4444").pack(pady=(5, 10))

        # ✅ BUONG MENSAHE — WALANG PINUTOL!
        for a in alerts:
            tree.insert("", "end", values=(
                a["id"],
                a["alert_title"],
                a["alert_level"],
                a["message"],
                str(a["posted_at"])[:19]
            ))

        # ✅ View Full Message button
        def view_full_message():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Notice", "Select an alert to view")
                return
            aid = tree.item(sel[0])["values"][0]
            alert = next((x for x in alerts if x["id"] == aid), None)
            if not alert:
                return
            win = ctk.CTkToplevel(self)
            win.title("Full Alert Message")
            win.geometry("700x500")
            ctk.CTkLabel(win, text=alert["alert_title"], font=("Arial", 16, "bold"),
                         text_color="#3b82f6").pack(pady=(20, 10))
            ctk.CTkLabel(win, text=f"Level: {alert['alert_level']}", font=("Arial", 12)).pack(pady=2)
            ctk.CTkLabel(win, text=f"Posted: {str(alert['posted_at'])[:19]}", font=("Arial", 10), text_color="#94a3b8").pack(pady=2)
            ctk.CTkLabel(win, text="Message:", font=("Arial", 11, "bold")).pack(anchor="w", padx=30, pady=(15, 5))
            txt = ctk.CTkTextbox(win, height=250)
            txt.pack(fill="both", expand=True, padx=30, pady=(0, 20))
            txt.insert("1.0", alert["message"])
            txt.configure(state="disabled")

        ctk.CTkButton(list_frame, text="View Full Message", command=view_full_message,
                      fg_color="#3b82f6").pack(pady=5)

    # ========== USER MANAGEMENT ==========
    def show_user_management(self):
        if self.current_user["role"] not in ["admin", "staff"]:
            messagebox.showwarning("Access Denied", "Admin or Staff only")
            return
        self.clear_main_content()
        ctk.CTkLabel(self.main_content_frame, text="User Management", font=("Arial", 22, "bold")).pack(anchor="w", padx=30, pady=(30, 10))

        form = ctk.CTkFrame(self.main_content_frame, fg_color="#1e293b", corner_radius=8)
        form.pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkLabel(form, text="Add New User", font=("Arial", 13, "bold"), text_color="#10b981").pack(anchor="w", padx=20, pady=(15, 10))

        row = ctk.CTkFrame(form)
        row.pack(fill="x", padx=20, pady=(0, 15))
        ctk.CTkLabel(row, text="Full Name:").grid(row=0, column=0, sticky="w")
        fm_name = ctk.CTkEntry(row)
        fm_name.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(row, text="Username:").grid(row=0, column=2, sticky="w", padx=(15, 0))
        fm_user = ctk.CTkEntry(row)
        fm_user.grid(row=0, column=3, padx=5)
        ctk.CTkLabel(row, text="Password:").grid(row=0, column=4, sticky="w", padx=(15, 0))
        fm_pass = ctk.CTkEntry(row, show="*")
        fm_pass.grid(row=0, column=5, padx=5)
        ctk.CTkLabel(row, text="Role:").grid(row=0, column=6, sticky="w", padx=(15, 0))
        fm_role = ctk.CTkOptionMenu(row, values=["student", "staff", "admin"])
        fm_role.set("student")
        fm_role.grid(row=0, column=7, padx=5)

        def add_user():
            n, u, p, r = fm_name.get().strip(), fm_user.get().strip(), fm_pass.get().strip(), fm_role.get()
            if not n or not u or not p:
                messagebox.showwarning("Incomplete", "Fill all fields")
                return
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO users (username, password, full_name, role) VALUES (%s, %s, %s, %s)", (u, p, n, r))
                    conn.commit()
                    cur.close()
                    conn.close()
                    messagebox.showinfo("Saved ✅", "User added successfully")
                    self.show_user_management()
                except Exception as e:
                    if "Duplicate" in str(e):
                        messagebox.showerror("Exists", "Username already taken")
                    else:
                        messagebox.showerror("Error", str(e))

        ctk.CTkButton(form, text="Add / Save User", command=add_user, fg_color="#10b981").pack(pady=(0, 15))

        conn = get_connection()
        users = []
        if conn:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM users ORDER BY id")
                users = cur.fetchall()
                cur.close()
                conn.close()
            except:
                pass

        list_frame = ctk.CTkFrame(self.main_content_frame)
        list_frame.pack(fill="both", expand=True, padx=30)
        cols = ("ID", "Username", "Full Name", "Role")
        tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)
        for c in cols:
            tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)

        def delete_user():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Notice", "Select a user first")
                return
            uid = tree.item(sel[0])["values"][0]
            uname = tree.item(sel[0])["values"][1]
            if uname == self.current_user["username"]:
                messagebox.showwarning("Cannot Delete", "You cannot delete your own account")
                return
            if not messagebox.askyesno("Confirm", f"Delete user '{uname}'?"):
                return
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM users WHERE id=%s", (uid,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    messagebox.showinfo("Deleted ✅", "User removed")
                    self.show_user_management()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        ctk.CTkButton(list_frame, text="Delete Selected User", command=delete_user, fg_color="#ef4444").pack(pady=10)
        for u in users:
            tree.insert("", "end", values=(u["id"], u["username"], u["full_name"], u["role"]))

if __name__ == "__main__":
    app = SafeCampusApp()
    app.mainloop()

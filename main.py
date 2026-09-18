import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from models import Auth, ContactManager, SafetyManager, IncidentManager

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SafeCampusApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔷 SafeCampus: Emergency Information System")
        self.geometry("1050x680")
        
        self.auth = Auth()
        self.contact_mgr = ContactManager()
        self.safety_mgr = SafetyManager()
        self.incident_mgr = IncidentManager()
        
        self.current_user = None
        self.current_frame = None
        
        self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.clear_frame()
        self.current_frame = DashboardFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_contacts(self):
        self.clear_frame()
        self.current_frame = ContactsFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_safety(self):
        self.clear_frame()
        self.current_frame = SafetyFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_incidents(self):
        self.clear_frame()
        self.current_frame = IncidentsFrame(self)
        self.current_frame.pack(fill="both", expand=True)


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#e6f0fa")
        self.parent = parent
        
        ctk.CTkLabel(self, text="🏫 SafeCampus", 
                     font=("Arial", 32, "bold"), text_color="#1a5276").pack(pady=(80,10))
        ctk.CTkLabel(self, text="Campus Emergency Information System", 
                     font=("Arial", 16), text_color="#283747").pack(pady=(0,40))
        
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        card.pack(pady=10, padx=350, fill="both", expand=True)
        
        ctk.CTkLabel(card, text="🔐 Sign In", 
                     font=("Arial", 20, "bold")).pack(pady=(30,20))
        
        self.user_entry = ctk.CTkEntry(card, placeholder_text="Username", width=280, height=40)
        self.user_entry.pack(pady=8)
        
        self.pass_entry = ctk.CTkEntry(card, placeholder_text="Password", 
                                       show="*", width=280, height=40)
        self.pass_entry.pack(pady=8)
        
        ctk.CTkButton(card, text="Login", command=self.do_login, 
                      fg_color="#2980b9", hover_color="#1f6195",
                      width=280, height=45, font=("Arial", 14, "bold")).pack(pady=25)
        
        ctk.CTkLabel(card, text="Demo: admin / admin123", 
                     text_color="#7f8c8d", font=("Arial", 11)).pack(pady=(0,30))

    def do_login(self):
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()
        
        result = self.parent.auth.login(user, pw)
        if result:
            self.parent.current_user = result
            self.parent.show_dashboard()
        else:
            messagebox.showerror("❌ Login Failed", "Invalid username or password!")


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f0f4f8")
        self.parent = parent
        
        top = ctk.CTkFrame(self, fg_color="#2980b9", height=80)
        top.pack(fill="x")
        top.pack_propagate(False)
        
        ctk.CTkLabel(top, text="🏠 Dashboard", font=("Arial", 22, "bold"), 
                     text_color="white").pack(side="left", padx=30, pady=20)
        ctk.CTkButton(top, text="🚪 Logout", fg_color="#e74c3c", hover_color="#c0392b",
                      command=parent.show_login, width=100).pack(side="right", padx=20, pady=20)
        
        contacts = len(parent.contact_mgr.get_all())
        safety = len(parent.safety_mgr.get_all())
        incidents = len(parent.incident_mgr.get_all())
        
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(pady=30, padx=40, fill="x")
        
        self.stat_card(stats_container, "📞 Emergency Contacts", contacts, "#3498db", 0)
        self.stat_card(stats_container, "🛡️ Safety Information", safety, "#27ae60", 1)
        self.stat_card(stats_container, "📋 Incident Reports", incidents, "#f39c12", 2)
        
        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.nav_card(btn_container, "📞 View Contacts", "Emergency contact numbers", 
                      "#3498db", parent.show_contacts, 0)
        self.nav_card(btn_container, "🛡️ Safety Guides", "Procedures & protocols", 
                      "#27ae60", parent.show_safety, 1)
        self.nav_card(btn_container, "📋 Incident Logs", "Reported incidents", 
                      "#f39c12", parent.show_incidents, 2)

    def stat_card(self, parent, title, count, color, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, border_color=color, border_width=2)
        card.grid(row=0, column=col, padx=15, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(card, text=title, font=("Arial", 13), text_color="#555").pack(pady=(20,5))
        ctk.CTkLabel(card, text=str(count), font=("Arial", 36, "bold"), 
                     text_color=color).pack(pady=(0,20))

    def nav_card(self, parent, title, desc, color, cmd, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, border_color="#ddd", border_width=1)
        card.grid(row=0, column=col, padx=15, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(card, text=title, font=("Arial", 15, "bold"), 
                     text_color=color).pack(pady=(25,8))
        ctk.CTkLabel(card, text=desc, font=("Arial", 11), text_color="#777").pack(pady=(0,20))
        ctk.CTkButton(card, text="Open →", fg_color=color, hover_color="#333",
                      command=cmd, width=140).pack(pady=(0,25))


class ContactsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f0f4f8")
        self.parent = parent
        
        top = ctk.CTkFrame(self, fg_color="#3498db", height=70)
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkButton(top, text="← Back", fg_color="#2980b9", hover_color="#1f6195",
                      command=parent.show_dashboard).pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(top, text="📞 Emergency Contacts", font=("Arial", 20, "bold"), 
                     text_color="white").pack(side="left", padx=10, pady=15)
        
        self.tree = ttk.Treeview(self, columns=("name", "number", "category", "desc"), show="headings", height=18)
        self.tree.heading("name", text="Name")
        self.tree.heading("number", text="Contact Number")
        self.tree.heading("category", text="Category")
        self.tree.heading("desc", text="Description")
        self.tree.column("name", width=250)
        self.tree.column("number", width=180)
        self.tree.column("category", width=130)
        self.tree.column("desc", width=350)
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = self.parent.contact_mgr.get_all()
        for row in data:
            self.tree.insert("", "end", values=(row[1], row[2], row[3], row[4]))


class SafetyFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f0f4f8")
        self.parent = parent
        
        top = ctk.CTkFrame(self, fg_color="#27ae60", height=70)
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkButton(top, text="← Back", fg_color="#219653", hover_color="#1e8449",
                      command=parent.show_dashboard).pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(top, text="🛡️ Safety Information", font=("Arial", 20, "bold"), 
                     text_color="white").pack(side="left", padx=10, pady=15)
        
        # --- Mas malawak na talahanayan, hindi pinuputol ang teksto ---
        self.tree = ttk.Treeview(self, columns=("title", "category", "content"), show="headings", height=18)
        self.tree.heading("title", text="Title")
        self.tree.heading("category", text="Category")
        self.tree.heading("content", text="Full Details")
        self.tree.column("title", width=280)       # Mas malawak
        self.tree.column("category", width=150)
        self.tree.column("content", width=650)     # Pinakamalawak — buong teksto
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Ipakita ang buong laman — WALANG pinuputol
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = self.parent.safety_mgr.get_all()
        # Ipinapakita ang BUONG teksto — walang "..."
        for row in data:
            self.tree.insert("", "end", values=(row[1], row[3], row[2]))

class IncidentsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f0f4f8")
        self.parent = parent
        
        
        top = ctk.CTkFrame(self, fg_color="#f39c12", height=70)
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkButton(top, text="← Back", fg_color="#e67e22", hover_color="#d35400",
                      command=parent.show_dashboard).pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(top, text="📋 Incident Reports", font=("Arial", 20, "bold"), 
                     text_color="white").pack(side="left", padx=10, pady=15)
        
        self.tree = ttk.Treeview(self, columns=("title", "location", "status", "date"), show="headings", height=18)
        self.tree.heading("title", text="Title")
        self.tree.heading("location", text="Location")
        self.tree.heading("status", text="Status")
        self.tree.heading("date", text="Date Reported")
        self.tree.column("title", width=300)
        self.tree.column("location", width=250)
        self.tree.column("status", width=120)
        self.tree.column("date", width=200)
        self.tree.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = self.parent.incident_mgr.get_all()
        for row in data:
            self.tree.insert("", "end", values=(row[1], row[3], row[5], row[4]))


if __name__ == "__main__":
    app = SafeCampusApp()
    app.mainloop()
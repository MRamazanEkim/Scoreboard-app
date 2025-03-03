import tkinter as tk
from tkinter import filedialog, colorchooser, Toplevel, messagebox, simpledialog, font, ttk
from PIL import Image, ImageTk, ImageGrab
import os
import sys


class ScoreboardApp:
    MAX_PLAYERS = 12  

    def __init__(self, root):
        self.root = root
        self.root.title("M3 Scoreboard")
        
        # Fix icon path handling for PyInstaller
        if getattr(sys, 'frozen', False):
            # Running from PyInstaller-built EXE
            icon_path = os.path.join(sys._MEIPASS, "app_icon.ico")
        else:
            # Running from a normal Python script
            icon_path = os.path.abspath("app_icon.ico")

        # Ensure the icon exists before setting it
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print(f"Warning: Icon file not found at {icon_path}")
        
        self.fullscreen = False
        self.root.attributes('-fullscreen', self.fullscreen)
        self.root.bind("<Escape>", self.toggle_fullscreen)

        self.bg_image = None
        self.bg_label = tk.Label(root)
        self.bg_label.place(relwidth=1, relheight=1)
        
        # Default Fonts
        self.title_font = ("Arial", 45, "bold")
        self.team_font = ("Arial", 40)
        self.player_font = ("Arial", 20)

        # SCOREBOARD Title
        self.title_var = tk.StringVar(value="SCOREBOARD")
        self.title_entry = tk.Entry(root, textvariable=self.title_var, font=self.title_font, width=20, justify="center", bg="black", fg="white")
        self.title_entry.place(relx=0.5, rely=0.05, anchor="center")
        
        self.available_fonts = list(font.families())

        # Team Data
        self.team1_players = []

        # Scoreboard Frame (Wider)
        self.scoreboard_frame = tk.Frame(root, bg="black", bd=10, padx=60, pady=10)  
        self.scoreboard_frame.place(relx=0.5, rely=0.5, anchor="center")
    

        # Delete & Add Buttons (Side by Side with Team Name)
        self.delete_team1_button = tk.Button(self.scoreboard_frame, text="−", font=("Arial", 24), width=3, command=self.delete_team1_player, bg="red", fg="white", relief="raised", bd=5)
        self.delete_team1_button.grid(row=0, column=0, padx=10, pady=10)

        self.team_name_var = tk.StringVar(value="Team Name")
        self.team_name_entry = tk.Entry(self.scoreboard_frame, textvariable=self.team_name_var, font=self.team_font, width=14, justify="center")
        self.team_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_team1_button = tk.Button(self.scoreboard_frame, text="+", font=("Arial", 24), width=3, command=self.add_team1_player, bg="green", fg="white", relief="raised", bd=5)
        self.add_team1_button.grid(row=0, column=2, padx=10, pady=10)

        # Change Background Button (Small, Bottom Right Corner)
        self.change_bg_button = tk.Button(self.root, text="🌄", font=("Arial", 20), command=self.change_background, width=3, height=1, bg="blue", fg="white", relief="raised", bd=5)
        self.change_bg_button.place(relx=0.98, rely=0.98, anchor="se")

        # Adding Color Pickers to Upper Right Corner with Distinct Style (Icons without text)
        self.frame_color_button = tk.Button(root, text="🎨", command=self.change_frame_color, bg="yellow", fg="black", relief="raised", bd=5, font=("Arial", 12))
        self.frame_color_button.place(relx=0.98, rely=0.02, anchor="ne")

        self.team_name_color_button = tk.Button(root, text="🎨", command=self.change_team_name_color, bg="purple", fg="white", relief="raised", bd=5, font=("Arial", 12))
        self.team_name_color_button.place(relx=0.94, rely=0.02, anchor="ne")

        self.player_name_color_button = tk.Button(root, text="🎨", command=self.change_player_names_color, bg="orange", fg="black", relief="raised", bd=5, font=("Arial", 12))
        self.player_name_color_button.place(relx=0.90, rely=0.02, anchor="ne")
        
        # Update Screenshot Button (Smaller and changed to "#")
        self.update_button = tk.Button(self.root, text="#", font=("Arial", 14), command=self.capture_screenshot, width=3, height=1, bg="gray", fg="white", relief="raised", bd=5)
        self.update_button.place(relx=0.02, rely=0.98, anchor="sw")
        
        # Font Selection Buttons
        self.title_font_button = tk.Button(self.root, text="Title Font", command=self.pick_title_font)
        self.title_font_button.place(relx=0.06, rely=0.02, anchor="ne")

        self.team_font_button = tk.Button(self.root, text="Team Font", command=self.pick_team_font)
        self.team_font_button.place(relx=0.06, rely=0.06, anchor="ne")

        self.player_font_button = tk.Button(self.root, text="Player Font", command=self.pick_player_font)
        self.player_font_button.place(relx=0.06, rely=0.10, anchor="ne")
        
        # Create second window at startup
        self.create_second_window()

    def add_team1_player(self):
        if len(self.team1_players) < self.MAX_PLAYERS:
            self.add_player(self.team1_players)

    def delete_team1_player(self):
        if self.team1_players:
            player = self.team1_players.pop()
            for widget in player["widgets"]:
                widget.destroy()
            self.update_ranks(self.team1_players)

    def add_player(self, team):
        row = len(team) + 1

        player = {
            "name": tk.StringVar(value=f"Player {row}"),
            "score": tk.IntVar(value=0),
            "rank": tk.StringVar(value=str(row))
        }

        entry_rank = tk.Label(self.scoreboard_frame, textvariable=player["rank"], font=("Arial", 20), width=3, bg="black", fg="white")
        entry_rank.grid(row=row, column=0, pady=5, padx=10)

        entry_name = tk.Entry(self.scoreboard_frame, textvariable=player["name"], font=self.player_font, width=12, justify="center")
        entry_name.grid(row=row, column=1, pady=5, padx=10)

        entry_score = tk.Entry(self.scoreboard_frame, textvariable=player["score"], font=self.player_font, width=6, justify="center")
        entry_score.grid(row=row, column=2, pady=5, padx=10)

        player["score"].trace_add("write", lambda *args, p=team: self.update_ranks(p))
        player["widgets"] = [entry_rank, entry_name, entry_score]
        team.append(player)

    def update_ranks(self, players):
        if not players:
            return  # Avoid errors if no players exist

        # Sort players by score (highest first)
        players.sort(key=lambda p: p["score"].get(), reverse=True)

        # Update ranks and reorder widgets
        for rank, player in enumerate(players, start=1):
            player["rank"].set(str(rank))

            # Reposition widgets dynamically
            player["widgets"][0].grid(row=rank, column=0, pady=10, padx=10)  # Rank
            player["widgets"][1].grid(row=rank, column=1, pady=10, padx=10)  # Name
            player["widgets"][2].grid(row=rank, column=2, pady=10, padx=10)  # Score

    def create_second_window(self):
        self.second_window = Toplevel(self.root)
        self.second_window.title("Preview")
        self.second_window.geometry("1280x720")
        self.second_window.attributes('-fullscreen', False)
        self.second_window.bind("<Escape>", lambda event: self.toggle_second_window_fullscreen(self.second_window))
        
        # Get correct icon path
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "app_icon.ico")
        else:
            icon_path = os.path.abspath("app_icon.ico")

        # Set icon if the file exists
        if os.path.exists(icon_path):
            self.second_window.iconbitmap(icon_path)
        else:
            print(f"Warning: Icon file not found at {icon_path}")
        
        self.screenshot_label = tk.Label(self.second_window)
        self.screenshot_label.pack()
    
    def capture_screenshot(self):
        # Ensure fullscreen before taking the screenshot
        self.fullscreen = True
        self.root.attributes('-fullscreen', True)
        self.root.update()
        
        # Hide buttons before taking the screenshot
        self.add_team1_button.grid_remove()
        self.delete_team1_button.grid_remove()
        
        self.update_button.focus_set()  # Remove focus from text fields
        self.root.update()
    
        x1, y1 = 200, 0
        x2, y2 = 1680, 1080
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        
        self.delete_team1_button = tk.Button(self.scoreboard_frame, text="−", font=("Arial", 24), width=3, command=self.delete_team1_player, bg="red", fg="white", relief="raised", bd=5)
        self.delete_team1_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.add_team1_button = tk.Button(self.scoreboard_frame, text="+", font=("Arial", 24), width=3, command=self.add_team1_player, bg="green", fg="white", relief="raised", bd=5)
        self.add_team1_button.grid(row=0, column=2, padx=10, pady=10)

        self.second_window.geometry(f'{self.root.winfo_width()}x{self.root.winfo_height()}')
        screenshot = screenshot.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
        screenshot_img = ImageTk.PhotoImage(screenshot)

        self.screenshot_label.config(image=screenshot_img)
        self.screenshot_label.image = screenshot_img

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        if not self.fullscreen:
            self.root.geometry("1280x720")

    def toggle_second_window_fullscreen(self, window):
        is_fullscreen = window.attributes('-fullscreen')
        window.attributes('-fullscreen', not is_fullscreen)
        if not is_fullscreen:
            window.geometry("1280x720")
    
    def change_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.bg_label.config(image=self.bg_image)

    # Function to change Scoreboard Frame color
    def change_frame_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.scoreboard_frame.config(bg=color)
        else:
            self.scoreboard_frame.config(bg="SystemTransparent")  # Set transparent
    
    # Function to change Team Name color
    def change_team_name_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.team_name_entry.config(fg=color)

    # Function to change Player Names color
    def change_player_names_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            for player in self.team1_players:
                player["widgets"][1].config(fg=color)  # Name Label
                
    def pick_title_font(self):
        self.open_font_picker("title")
    
    def pick_team_font(self):
        self.open_font_picker("team")
    
    def pick_player_font(self):
        self.open_font_picker("player")
    
    def open_font_picker(self, target):
        font_window = Toplevel(self.root)
        font_window.title("Select Font")
        font_window.geometry("300x300")
        
        font_var = tk.StringVar(value=self.title_font[0] if target == "title" else self.team_font[0] if target == "team" else self.player_font[0])
        font_listbox = tk.Listbox(font_window, listvariable=tk.StringVar(value=self.available_fonts), height=15)
        font_listbox.pack(fill=tk.BOTH, expand=True)
        
        def apply_font():
            selected_index = font_listbox.curselection()
            if selected_index:
                selected_font = self.available_fonts[selected_index[0]]
                if target == "title":
                    self.title_font = (selected_font, 45, "bold")
                    self.title_entry.config(font=self.title_font)
                elif target == "team":
                    self.team_font = (selected_font, 40)
                    self.team_name_entry.config(font=self.team_font)
                elif target == "player":
                    self.player_font = (selected_font, 20)
                    for player in self.team1_players:
                        player["widgets"][1].config(font=self.player_font)
            font_window.destroy()
        
        apply_button = tk.Button(font_window, text="Apply Font", command=apply_font)
        apply_button.pack()

root = tk.Tk()
root.geometry("1280x720")
app = ScoreboardApp(root)
root.mainloop()

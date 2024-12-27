import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkinter import ttk

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notepad")
        self.root.geometry("800x600")
        
        # Configure colors and default font
        self.bg_color = "black"
        self.fg_color = "orange"
        self.root.configure(bg=self.bg_color)
        self.current_font = ("Arial", 12)
        
        # Create main text area with styling
        self.text_area = tk.Text(
            self.root,
            undo=True,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            selectbackground="#333333",
            selectforeground=self.fg_color,
            font=self.current_font
        )
        self.text_area.pack(expand=True, fill='both')
        
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        
        # Format menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        
        # Font submenu
        self.font_menu = tk.Menu(self.format_menu, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        self.format_menu.add_cascade(label="Font", menu=self.font_menu)
        
        # Get available fonts
        self.available_fonts = sorted(font.families())
        
        # Add fonts to menu
        for font_name in self.available_fonts:
            self.font_menu.add_radiobutton(
                label=font_name,
                command=lambda fn=font_name: self.change_font(fn),
                variable=tk.StringVar(value=self.current_font[0])
            )
        
        # Font size menu
        self.size_menu = tk.Menu(self.format_menu, tearoff=0, bg=self.bg_color, fg=self.fg_color)
        self.format_menu.add_cascade(label="Size", menu=self.size_menu)
        
        # Add common font sizes
        for size in [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]:
            self.size_menu.add_radiobutton(
                label=str(size),
                command=lambda s=size: self.change_size(s),
                variable=tk.IntVar(value=self.current_font[1])
            )
        
        # Font style options
        self.format_menu.add_checkbutton(label="Bold", command=self.toggle_bold)
        self.format_menu.add_checkbutton(label="Italic", command=self.toggle_italic)
        self.format_menu.add_checkbutton(label="Underline", command=self.toggle_underline)
        
        # Add scrollbar
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar", 
                       background=self.bg_color, 
                       troughcolor=self.bg_color,
                       arrowcolor=self.fg_color)
        
        self.scrollbar = ttk.Scrollbar(self.text_area, style="Custom.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        
        # Current file
        self.current_file = None
        
        # Font state
        self.bold = False
        self.italic = False
        self.underline = False
    
    def change_font(self, font_name):
        self.current_font = (font_name, self.current_font[1])
        self.update_font()
    
    def change_size(self, size):
        self.current_font = (self.current_font[0], size)
        self.update_font()
    
    def toggle_bold(self):
        self.bold = not self.bold
        self.update_font()
    
    def toggle_italic(self):
        self.italic = not self.italic
        self.update_font()
    
    def toggle_underline(self):
        self.underline = not self.underline
        self.update_font()
    
    def update_font(self):
        # Build font description
        weight = "bold" if self.bold else "normal"
        slant = "italic" if self.italic else "roman"
        
        # Create new font configuration
        current_font = font.Font(
            family=self.current_font[0],
            size=self.current_font[1],
            weight=weight,
            slant=slant,
            underline=self.underline
        )
        
        # Apply to text area
        self.text_area.configure(font=current_font)
    
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Simple Notepad")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
                self.current_file = file_path
                self.root.title(f"Simple Notepad - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't open file: {str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, 'w') as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't save file: {str(e)}")
        else:
            self.save_as()
    
    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(file_path, 'w') as file:
                    file.write(content)
                self.current_file = file_path
                self.root.title(f"Simple Notepad - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't save file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
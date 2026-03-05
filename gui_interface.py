import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class GuiApplication(tk.Tk):
    def __init__(self, model=None, *args, **kwargs):
        super().__init__()
        self.model = model
        self.title("GUI Chat")
        self.minsize(800, 600)
        self.configure(background="white")
        self.menubar = None
        self.chat_window = None
        self.user_entry = None
        self.send_button = None

        self.setup_menubar()
        self.setup_chat_window()
        self.setup_user_input_area()

    def setup_menubar(self):
        self.menubar = tk.Menu(self)
        self.menubar.configure(background='white', foreground='black')
        file_menu = tk.Menu(self.menubar)
        file_menu.add_command(label="Exit", command=self.destroy, background='white', foreground='black')
        file_menu.add_separator()

        self.menubar.add_cascade(label="File", menu=file_menu, background='white', foreground='black')
        self.configure(menu=self.menubar)


    def setup_chat_window(self):
        self.chat_window = tk.scrolledtext.ScrolledText(self, height=15, width=75, wrap='word',
                                                        background='white', foreground='black',
                                                        takefocus=False, relief='sunken'
                                                        )
        # Model will output garbage when user isn't the first to speak, could be fixed on the back end.
        #if self.model is not None:
        #    self.chat_window.insert(tk.END, self.model.send_to_model() + '\n\n')
        self.chat_window.configure(state='disabled')
        self.chat_window.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    def setup_user_input_area(self):
        self.user_entry = tk.scrolledtext.ScrolledText(self, height=10, width=75, wrap='word',
                                                       background='white', foreground='black',
                                                       takefocus=True, relief="sunken")
        self.user_entry.grid(row=1, column=0, columnspan=3, padx=5, pady=(0,5))
        self.send_button = ttk.Button(self, text="Send", command=self.send_input)
        self.send_button.grid(row=1, column=3)

    def send_input(self):
        user_input = self.user_entry.get('1.0', tk.END)
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, f'User: {user_input}\n')
        self.chat_window.yview(tk.END)
        self.user_entry.delete('1.0', tk.END)
        self.chat_window.config(state='disabled')
        if self.model is not None:
            self.add_chat_text(self.model.send_to_model(user_input))

    def add_chat_text(self, message):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, message + '\n\n')
        self.chat_window.yview(tk.END)
        self.chat_window.config(state='disabled')


if __name__ == "__main__":
    try:
        app = GuiApplication()
        print("GUI starting...")
        app.mainloop()
    except Exception as e:
        print(f"Display error: {e}")
        print("No display available. Are you running this in WSL, SSH, or a headless environment?")
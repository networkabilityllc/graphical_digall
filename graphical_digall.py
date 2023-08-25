import subprocess
import tkinter as tk
from tkinter import scrolledtext, filedialog

# Define tag names
TAG_RED = 'red'
TAG_LIGHT_GREEN = 'light_green'
TAG_LIGHT_BLUE = 'light_blue'
TAG_LIGHT_CYAN = 'light_cyan'
TAG_RESTORE = 'restore'

def run_dig(domain, text_widget):
    # Clear the text_widget content
    text_widget.delete(1.0, tk.END)
    
    text_widget.insert(tk.END, "Queries: (dig +noall +answer '{0}' '<type>')...\n".format(domain), TAG_LIGHT_BLUE)
    
    for t in ["SOA", "NS", "SPF", "TXT", "MX", "AAAA", "A"]:
        text_widget.insert(tk.END, "Querying for {0} records...\n".format(t), TAG_LIGHT_GREEN)
        
        # Run the dig command using subprocess
        try:
            result = subprocess.run(["dig", "+noall", "+answer", domain, t], capture_output=True, text=True)
            text_widget.insert(tk.END, result.stdout + '\n')
        except Exception as e:
            text_widget.insert(tk.END, "Error running dig command: {0}\n".format(e), TAG_RED)


def save_data(text_widget):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_widget.get(1.0, tk.END))

def main():
    # Basic tkinter setup
    root = tk.Tk()
    root.title("DigAll GUI")
    
    # Set background color for main window
    root.configure(bg='#333333')

    frame = tk.Frame(root, bg='#333333')
    frame.pack(padx=10, pady=10)

    # Scrolled text widget with dark theme
    text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=20, bg='#2E2E2E', fg='#E0E0E0', insertbackground='white')
    text_widget.pack(padx=10, pady=10)
    text_widget.tag_config(TAG_RED, foreground='red')
    text_widget.tag_config(TAG_LIGHT_GREEN, foreground='light green')
    text_widget.tag_config(TAG_LIGHT_BLUE, foreground='light blue')
    text_widget.tag_config(TAG_LIGHT_CYAN, foreground='light cyan')

    # Label widget with the instruction
    domain_label = tk.Label(frame, text="Type in Domain Name Here:", bg='#333333', fg='#E0E0E0')
    domain_label.pack(pady=(10, 0))

    # Entry widget with dark theme
    domain_entry = tk.Entry(frame, width=40, bg='#2E2E2E', fg='#E0E0E0', insertbackground='white')
    domain_entry.pack(pady=10)
    domain_entry.focus_set()

    # Dig button with dark theme
    dig_button = tk.Button(frame, text="Run DigAll", command=lambda: run_dig(domain_entry.get(), text_widget), bg='#444444', fg='#E0E0E0', activebackground='#555555', activeforeground='#E0E0E0')
    dig_button.pack(pady=(0, 5))

    # Save Data button with dark theme
    save_button = tk.Button(frame, text="Save Data", command=lambda: save_data(text_widget), bg='#444444', fg='#E0E0E0', activebackground='#555555', activeforeground='#E0E0E0')
    save_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()

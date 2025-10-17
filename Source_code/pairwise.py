import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import sys

class PairwiseRankerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pairwise Ranking Tool")
        self.root.geometry("600x400")

        # Handle safe exit
        self.root.protocol("WM_DELETE_WINDOW", self.safe_exit)

        self.items = []
        self.final_ranking = []
        self.choice_var = None

        self.create_widgets()

    def create_widgets(self):
        """Build the GUI layout."""
        self.title_label = tk.Label(self.root, text="Pairwise Ranking Tool", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load items from .txt file", command=self.load_file)
        self.load_button.pack(pady=10)

        self.compare_frame = tk.Frame(self.root)
        self.compare_frame.pack(pady=20)

        self.label1 = tk.Label(self.compare_frame, text="", font=("Arial", 14))
        self.label1.grid(row=0, column=0, padx=10)

        self.label2 = tk.Label(self.compare_frame, text="", font=("Arial", 14))
        self.label2.grid(row=0, column=2, padx=10)

        self.button1 = tk.Button(self.compare_frame, text="Choose 1", width=15, command=lambda: self.choose(1))
        self.button1.grid(row=1, column=0, pady=10)

        self.button2 = tk.Button(self.compare_frame, text="Choose 2", width=15, command=lambda: self.choose(2))
        self.button2.grid(row=1, column=2, pady=10)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def safe_exit(self):
        """Gracefully exit the program if the user closes the window."""
        if messagebox.askokcancel("Exit", "Do you want to quit? Unsaved progress will be lost."):
            try:
                self.root.destroy()
                sys.exit(0)
            except Exception:
                pass

    def load_file(self):
        """Load items from a text file."""
        path = filedialog.askopenfilename(
            title="Select a .txt file",
            filetypes=[("Text Files", "*.txt")]
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            self.items = [line.strip() for line in f if line.strip()]

        if len(self.items) < 2:
            messagebox.showerror("Error", "Please provide at least 2 items in your file.")
            return

        messagebox.showinfo("Loaded", f"Loaded {len(self.items)} items.")
        self.start_ranking()

    def start_ranking(self):
        """Start the pairwise comparison process."""
        self.final_ranking = self.merge_sort(self.items)
        self.save_results()

        result_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(self.final_ranking)])
        messagebox.showinfo("Ranking Complete", f"Your ranking:\n\n{result_text}")
        self.safe_exit()

    def choose(self, choice_num):
        """Handle button click (1 or 2)."""
        self.choice_var.set(choice_num)

    def merge_sort(self, items):
        """Recursive merge sort with user input for comparisons."""
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left = self.merge_sort(items[:mid])
        right = self.merge_sort(items[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            self.choice_var = tk.IntVar()
            self.label1.config(text=left[i])
            self.label2.config(text=right[j])
            self.status_label.config(
                text=f"Comparing: {left[i]} vs {right[j]}  ({len(result)+1} of ~{len(self.items)*2})"
            )

            # Wait for user choice
            try:
                self.root.wait_variable(self.choice_var)
            except tk.TclError:
                self.safe_exit()
                return []

            if self.choice_var.get() == 1:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def save_results(self):
        """Save the final ranking to a text file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = "ranking_results.txt"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n--- Ranking Session ({timestamp}) ---\n")
            for i, item in enumerate(self.final_ranking, start=1):
                f.write(f"{i}. {item}\n")
            f.write("\n")
        print(f"✅ Results saved to {filename}")

# Run the app safely
if __name__ == "__main__":
    root = tk.Tk()
    app = PairwiseRankerApp(root)
    root.mainloop()

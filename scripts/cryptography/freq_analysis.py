from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
import string
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from io import StringIO

# Custom console theme for better clarity
custom_theme = Theme({
    "warning": "bold yellow",
    "danger": "bold red",
    "info": "cyan",
    "success": "green"
})

console = Console(theme=custom_theme)

# Standard English frequencies (%)
english_freq = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23,
    'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03,
    'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99,
    's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
    'y': 1.97, 'z': 0.07
}

def frequency_analysis(text, threshold=5.0, sort_by_difference=False):
    # Clean input
    cleaned = ''.join(filter(str.isalpha, text)).lower()
    freq = Counter(cleaned)
    total = sum(freq.values())

    # Results container
    results = []
    for letter in string.ascii_lowercase:
        your_pct = (freq.get(letter, 0) / total) * 100 if total > 0 else 0
        expected_pct = english_freq.get(letter, 0)
        diff = your_pct - expected_pct
        abs_diff = abs(diff)
        results.append((letter.upper(), your_pct, expected_pct, abs_diff, diff))

    # Sort
    #results.sort(key=lambda x: x[3], reverse=True if sort_by_difference else False)

    # Table with emojis and highlights
    table = Table(title="🔐 Ciphertext Frequency vs Standard English", show_lines=True)
    table.add_column("Letter", justify="center", style="info")
    table.add_column("Your Text %", justify="right", style="magenta")
    table.add_column("Expected %", justify="right", style="success")
    table.add_column("Δ Difference", justify="right")

    similarity_check = 0
    for letter, your_pct, expected_pct, abs_diff, diff in results:
        emoji = "🔺" if diff > 0 else "🔻"
        diff_str = f"{emoji} {abs_diff:.2f}%"
        margin = abs(expected_pct - your_pct) / abs(expected_pct)
        if margin < 0.2:
            similarity_check +=1
        if abs_diff >= threshold:
            color = "danger" if diff > 0 else "warning"
            diff_str = f"[{color}]{diff_str}[/{color}]"
        else:
            diff_str = f"{emoji} {abs_diff:.2f}%"
        table.add_row(letter, f"{your_pct:.2f}%", f"{expected_pct:.2f}%", diff_str)
    table.add_row("~", f"{similarity_check/26*100:.2f}%", "-", "Similarity")
    console.print(table)
    # Capture output and display in tkinter
    output_buffer = StringIO()
    temp_console = Console(file=output_buffer, theme=custom_theme, width=80)
    temp_console.print(table)
    return output_buffer.getvalue()


def frequency_analysis_graph(text, max_bar_len=20):
    cleaned = ''.join(filter(str.isalpha, text)).lower()
    freq = Counter(cleaned)
    total = sum(freq.values())

    if total == 0:
        return "No alphabetic content to analyze."

    output_lines = []
    output_lines.append(" LETTER | Ciphertext                 | English Average")
    output_lines.append(" -------+------------------------+------------------------")

    # Prepare frequencies
    letters = string.ascii_lowercase
    your_freqs = [(freq.get(ch, 0) / total) * 100 for ch in letters]
    english_vals = [english_freq[ch] for ch in letters]

    # Scaling based on highest frequency in either set
    scale_base = max(max(your_freqs), max(english_vals))
    similarity_check = 0
    for ch, actual_pct, expected_pct in zip(letters, your_freqs, english_vals):        
        margin = abs(expected_pct - actual_pct) / abs(expected_pct)
        if margin < 0.2:
            similarity_check +=1
        bar_your = "█" * int((actual_pct / scale_base) * max_bar_len)
        bar_english = "█" * int((expected_pct / scale_base) * max_bar_len)
        output_lines.append(
            f"    {ch.upper():<3} | {bar_your:<20} {actual_pct:>4.1f}% | {bar_english:<20} {expected_pct:>4.1f}%"
        )
    output_lines.append(f"Similarity: {similarity_check/26*100:>4.1f}%")
    return "\n".join(output_lines)

def show_freq_output(text_output):
    root = tk.Tk()
    root.title("Letter Frequency Comparison (Side-by-Side)")
    root.geometry("900x600")
    text_widget = ScrolledText(root, font=("Courier", 12), bg="#1e1e1e", fg="#d4d4d4")
    text_widget.pack(expand=True, fill="both")
    text_widget.insert("1.0", text_output)
    text_widget.config(state="disabled")
    root.mainloop()


    # output_text = frequency_analysis(ciphertext, threshold=5.0, sort_by_difference=True)
    # output = frequency_analysis_graph(ciphertext)
    # show_freq_output(output)

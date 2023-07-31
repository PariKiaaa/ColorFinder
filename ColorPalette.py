import tkinter as tk
import pyperclip
import random

class ColorPaletteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color palette")
        self.colors = [self.random_color() for _ in range(54)]
        self.row_num = 0
        self.col_num = 0

        self.create_palette()

    def random_color(self):
        return "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

    def on_color_click(self, HEX_code):
        # Get the RGB code from the HEX code
        rgb_code = self.hex_to_rgb(HEX_code)
        # Update the RGB label text
        self.rgb_info_label.config(text=f"RGB: {rgb_code}")

        # Update the HEX label text and open the copy dialog after a short delay
        self.color_info_label.config(text=f"HEX: {HEX_code}")
        self.after(100, lambda: self.open_copy_dialog(HEX_code, rgb_code))

    def open_copy_dialog(self, HEX_code, rgb_code):
        # Open a dialog for copying the color information (HEX or RGB)
        dialog = ColorCopyDialog(self, HEX_code, rgb_code)
        self.wait_window(dialog)

    def create_palette(self):
        for color in self.colors:
            # Create colored frames as the color palette
            frame = tk.Frame(self, width=50, height=50, bg=color)
            frame.grid(row=self.row_num, column=self.col_num, padx=5, pady=5)
            frame.bind("<Button-1>", lambda event, HEX=color: self.on_color_click(HEX))
            
            self.col_num += 1
            if self.col_num > 5:
                self.col_num = 0
                self.row_num += 1

        # Create labels to show the HEX and RGB information
        self.color_info_label = tk.Label(self, text="HEX: ", font=("Arial", 14))
        self.color_info_label.grid(row=self.row_num+1, column=0, columnspan=3)

        self.rgb_info_label = tk.Label(self, text="RGB: ", font=("Arial", 14))
        self.rgb_info_label.grid(row=self.row_num+1, column=3, columnspan=3)

    @staticmethod
    def hex_to_rgb(hex_code):
        # Convert HEX code to RGB code
        hex_code = hex_code.lstrip("#")
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


class ColorCopyDialog(tk.Toplevel):
    def __init__(self, parent, HEX_code, RGB_code):
        super().__init__(parent)
        self.title("Copy Color")
        self.HEX_code = HEX_code
        self.RGB_code = RGB_code

        self.create_widgets()

    def create_widgets(self):
        # Buttons to copy HEX or RGB code to clipboard
        hex_button = tk.Button(self, text="Copy HEX", command=self.copy_hex)
        hex_button.pack(padx=20, pady=10, side=tk.LEFT)

        rgb_button = tk.Button(self, text="Copy RGB", command=self.copy_rgb)
        rgb_button.pack(padx=20, pady=10, side=tk.RIGHT)

    def copy_hex(self):
        # Copy HEX code to clipboard and close the dialog
        pyperclip.copy(self.HEX_code)
        self.destroy()

    def copy_rgb(self):
        # Convert RGB code to a comma-separated string and copy to clipboard
        rgb_str = ", ".join(str(val) for val in self.RGB_code)
        pyperclip.copy(rgb_str)
        self.destroy()


if __name__ == "__main__":
    app = ColorPaletteApp()
    app.mainloop()

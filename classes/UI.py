from tkinter import TOP, Frame, StringVar, Tk, Label, Entry, Button, Text, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

class UI:
    def show_gcode_input(self) -> str | None:
        window = TkinterDnD.Tk()
        window.title("GCode Input")
        window.geometry("500x500")

        headline_label = Label(window, text="GCode Input", font=("Arial", 24), pady=20)
        headline_label.pack()

        file_path_var = StringVar()
        entry_widget = Entry(window, textvariable=file_path_var, width=300, font=("Arial", 12))
        label = Label(window, text="Enter File Path or Drop File Here:", font=("Arial", 12))
        label.pack(side=TOP, padx=20, pady=5)
        entry_widget.pack(side=TOP, padx=5, pady=5)
        def __on_drop(event: TkinterDnD.DnDEvent):
            files: str = event.data
            files = files[1:]
            files_list = files.split("}")
            file:str = files_list[0]
            file_path_var.set(file)
        entry_widget.drop_target_register(DND_FILES)
        entry_widget.dnd_bind('<<Drop>>', __on_drop)

        is_ok: list[bool] = []
        def __on_click():
            is_ok.append(True)
            window.quit()
        button = Button(window, text="Convert", command=__on_click)
        button.pack(side=TOP, padx=5, pady=5)

        window.mainloop()
        window.quit()
        window.destroy()
        if True in is_ok:
            return file_path_var.get()
        return None

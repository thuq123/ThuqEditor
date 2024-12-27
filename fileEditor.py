import tkinter as tk
from tkinter import colorchooser, filedialog, font

import win32api

global openedFileName
openedFileName = False

global selected
selected = ""

window = tk.Tk()
window.title("ThuqPad")
window.geometry("1366x768")
window.iconphoto(True, tk.PhotoImage(file="Icon.png"))
# Icon created by Pixel Budha Premium from www.flaticon.com

buttonFrame = tk.Frame(window)
buttonFrame.pack(fill="x", side=tk.TOP)

frame = tk.Frame(window)
frame.pack(pady=5, side=tk.TOP, fill="both", expand=True)

textScrollBar = tk.Scrollbar(frame)
textScrollBar.pack(
    side="right",
    fill="y",
)

horizontalScrollBar = tk.Scrollbar(frame, orient="horizontal")
horizontalScrollBar.pack(side="bottom", fill="x")

textBox = tk.Text(
    frame,
    width=97,
    height=25,
    font=("Helvetica", 16),
    selectbackground="lightblue",
    selectforeground="black",
    undo=True,
    yscrollcommand=textScrollBar.set,
    xscrollcommand=horizontalScrollBar.set,
    wrap="none",
)
textBox.pack(expand=True, fill="both", padx=5)

textScrollBar.config(command=textBox.yview)
horizontalScrollBar.config(command=textBox.xview)


def newFile():
    textBox.delete("1.0", tk.END)
    window.title("New File - ThuqPad")
    statusBar.configure(text="New File        ")
    global openedFileName
    openedFileName = False


def openFile():
    textBox.delete("1.0", tk.END)
    filename = filedialog.askopenfilename(
        title="Open File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if filename:
        global openedFileName
        openedFileName = filename

        name = filename
        statusBar.configure(text=f"{name}        ")
        window.title(f"{name} - ThuqPad")

        filename = open(filename, "r")
        content = filename.read()
        textBox.insert(tk.END, content)
        filename.close()


def saveAsFile():
    filename = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=".*",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if filename:
        name = filename
        statusBar.configure(text=f"Saved as {name}        ")
        window.title(f"{name} - ThuqPad")

        filename = open(filename, "w")
        filename.write(textBox.get(1.0, tk.END))
        filename.close()


def saveFile():
    global openedFileName

    if openedFileName:
        filename = openedFileName
        statusBar.configure(text=f"Saved {filename}        ")
        window.title(f"{filename} - ThuqPad")

        filename = open(filename, "w")
        filename.write(textBox.get(1.0, tk.END))

        filename.close()

    else:
        saveAsFile()


def printFile():
    filetoprint = filedialog.askopenfilename(
        title="Print File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if filetoprint:
        win32api.ShellExecute(0, "print", filetoprint, "", ".", 0)


def cutText(e):
    global selected

    if e:
        selected = window.clipboard_get()
    else:
        if textBox.selection_get():
            selected = textBox.selection_get()

            textBox.delete("sel.first", "sel.last")

            window.clipboard_clear()
            window.clipboard_append(selected)


def pasteText(e):
    global selected

    if e:
        selected = window.clipboard_get()

    else:
        if selected:
            position = textBox.index("insert")
            textBox.insert(position, selected)


def copyText(e):
    global selected

    if e:
        selected = window.clipboard_get()
    else:
        if textBox.selection_get():
            selected = textBox.selection_get()

            window.clipboard_clear()
            window.clipboard_append(selected)


def boldText():
    boldFont = font.Font(textBox, textBox.cget("font"))
    boldFont.configure(weight="bold")

    textBox.tag_configure("bold", font=boldFont)

    currentTags = textBox.tag_names("sel.first")

    if "bold" in currentTags:
        textBox.tag_remove("bold", "sel.first", "sel.last")

    else:
        textBox.tag_add("bold", "sel.first", "sel.last")


def italicText():
    italicFont = font.Font(textBox, textBox.cget("font"))
    italicFont.configure(slant="italic")

    textBox.tag_configure("italic", font=italicFont)

    currentTags = textBox.tag_names("sel.first")

    if "italic" in currentTags:
        textBox.tag_remove("italic", "sel.first", "sel.last")

    else:
        textBox.tag_add("italic", "sel.first", "sel.last")


def changeTextColor():
    colorFont = font.Font(textBox, textBox.cget("font"))

    myColor = colorchooser.askcolor()[1]

    if myColor:
        textBox.tag_configure("colored", font=colorFont, foreground=myColor)

        currentTags = textBox.tag_names("sel.first")

        if "colored" in currentTags:
            textBox.tag_remove("colored", "sel.first", "sel.last")

        else:
            textBox.tag_add("colored", "sel.first", "sel.last")


def selectAll():
    textBox.tag_add("sel", "1.0", tk.END)


def clearAll():
    textBox.delete("1.0", tk.END)


menu = tk.Menu(window)
window.config(menu=menu)

boldIcon = tk.PhotoImage(file="Bold.png")
boldIcon = boldIcon.subsample(20, 20)
# Icon created by Dave Gandy from www.flaticon.com
italicIcon = tk.PhotoImage(file="Italic.png")
italicIcon = italicIcon.subsample(20, 20)
# Icon created by Dave Gandy from www.flaticon.com
undoIcon = tk.PhotoImage(file="Undo.png")
undoIcon = undoIcon.subsample(20, 20)
# Icon created by Dave Gandy from www.flaticon.com
redoIcon = tk.PhotoImage(file="Redo.png")
redoIcon = redoIcon.subsample(20, 20)
# Icon created by Md Tanvirul Haque from www.flaticon.com
textColorIcon = tk.PhotoImage(file="TextColor.png")
textColorIcon = textColorIcon.subsample(20, 20)
# Icon created by egorpolyakov from www.flaticon.com

fileMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New", command=newFile, accelerator="(Ctrl + n)")
fileMenu.add_command(label="Open", command=openFile, accelerator="(Ctrl + o)")
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_command(label="Save As", command=saveAsFile, accelerator="(Ctrl + s)")
fileMenu.add_separator()
fileMenu.add_command(label="Print", command=printFile, accelerator="(Ctrl + p)")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=window.quit)

editMenu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(
    label="Copy", command=lambda: copyText(False), accelerator="(Ctrl + c)"
)
editMenu.add_command(
    label="Cut", command=lambda: cutText(False), accelerator="(Ctrl + x)"
)
editMenu.add_command(
    label="Paste", command=lambda: pasteText(False), accelerator="(Ctrl + v)"
)
editMenu.add_separator()
editMenu.add_command(label="Undo", command=textBox.edit_undo, accelerator="(Ctrl + z)")
editMenu.add_command(label="Redo", command=textBox.edit_redo, accelerator="(Ctrl + y)")
editMenu.add_separator()
editMenu.add_command(label="Select All", command=selectAll, accelerator="(Ctrl + a)")
editMenu.add_command(label="Clear", command=clearAll)

statusBar = tk.Label(window, text="Ready        ", anchor="e")
statusBar.pack(fill="x", side="bottom", ipady=5)

window.bind("<Control-Key-c>", lambda x: copyText(True))
window.bind("<Control-Key-x>", lambda x: cutText(True))
window.bind("<Control-Key-v>", lambda x: pasteText(True))
window.bind("<Control-Key-z>", lambda x: textBox.edit_undo())
window.bind("<Control-Key-y>", lambda x: textBox.edit_redo())
window.bind("<Control-Key-a>", lambda x: selectAll())
window.bind("<Control-Key-s>", lambda x: saveAsFile())
window.bind("<Control-Key-o>", lambda x: openFile())
window.bind("<Control-Key-p>", lambda x: printFile())
window.bind("<Control-Key-n>", lambda x: newFile())

boldButton = tk.Button(buttonFrame, image=boldIcon, command=boldText)
boldButton.grid(row=0, column=0, sticky="w", padx=10, pady=5)

italicButton = tk.Button(buttonFrame, image=italicIcon, command=italicText)
italicButton.grid(row=0, column=1, padx=10, pady=5)

undoButton = tk.Button(buttonFrame, image=undoIcon, command=textBox.edit_undo)
undoButton.grid(row=0, column=2, padx=10, pady=5)

redoButton = tk.Button(buttonFrame, image=redoIcon, command=textBox.edit_redo)
redoButton.grid(row=0, column=3, padx=10, pady=5)

textColorButton = tk.Button(buttonFrame, image=textColorIcon, command=changeTextColor)
textColorButton.grid(row=0, column=4, padx=10, pady=5)

window.mainloop()

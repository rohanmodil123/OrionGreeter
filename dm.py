#!/usr/bin/env python3

import tkinter as tk
import time
import sys
import pam
import colour
from functools import partial
import threading
import subprocess
import wx


app = wx.App(False)
screenwidth, screenheight = wx.GetDisplaySize()  # root.winfo_height does not work
print(screenwidth, screenheight)

root = tk.Tk()

root.config(bg='#2E3440')
root.geometry(f'{screenwidth}x{screenheight}')
root.update()

global username
global password
global mode

username = None
password = None

# Mode 0: No user/pass. Mode 1: User, no pass. Mode 3: Authenticated.
mode = 0


def entry_cursor(ph1=None, ph2=None, ph3=None):
    # ph1 = variable, ph2 = None, ph3 = mode.
    # print("\n entry_cursor method called \n")

    if len(entry_widget.get()) == 0:
        entry_widget.config(insertbackground='#2E3440')
    if len(entry_widget.get()) > 0:
        entry_widget.config(insertbackground='#ffffff')


# Fixing Control Backspace and Control Delete


def entry_ctrl_bs(event):
    ent = event.widget
    end_idx = ent.index(tk.INSERT)
    ent.selection_range(0, end_idx)


def entry_ctrl_dl(event):
    ent = event.widget
    start_idx = ent.index(tk.INSERT)
    end_idx = len(ent.get())
    ent.selection_range(start_idx, end_idx)


def entry_enter(widget, bg, fg, event):
    # entry_widget.config(bg='#ffffff')

    fade(entry_widget, smoothness=1, fg=fg, bg=bg)

    global username
    global password

    if mode == 0:
        username = entry_widget.get()
    elif mode == 1:
        password = entry_widget.get()

    entry_widget.delete(0, tk.END)
    entry_widget.config(insertbackground='#C4C6C8')

    if mode == 0:
        timer = threading.Timer(0.1, entry_enter2, [username])
        timer.start()
    if mode == 1:
        timer = threading.Timer(0.1, entry_enter3, [username])
        timer.start()


def entry_enter2(usrname):
    label.config(text=f'Hello, {usrname}.')
    fade(entry_widget, smoothness=3, fg='#ffffff', bg='#2E3440')
    entry_widget.delete(0, tk.END)
    entry_widget.config(insertbackground='#2E3440', show='*')

    global mode
    mode = 1


def entry_enter3(passwd):
    # global password
    global mode

    if not pam.authenticate(username, password):
        mode = 0
        print("Login unsuccessful")

        label.config(text='Failed. Identify.')
        entry_widget.config(bg='#2E3440', insertbackground='#2E3440', show='')

    else:
        mode = 3
        entry_widget.pack_forget()
        label.pack_forget()

        print("Login successful")
        subprocess.run('startx')


def fade(widget, smoothness=3, cnf={}, **kw):
    """This function will show faded effect on widget's different color options.

    Args:
        widget (tk.Widget): Passed by the bind function.
        smoothness (int): Set the smoothness of the fading (1-10).
        background (str): Fade background color to.
        foreground (str): Fade foreground color to."""

    kw = tk._cnfmerge((cnf, kw))
    if not kw: raise ValueError("No option given, -bg, -fg, etc")
    if len(kw) > 1: return [fade(widget, smoothness, {k: v}) for k, v in kw.items()][0]
    if not getattr(widget, '_after_ids', None): widget._after_ids = {}
    widget.after_cancel(widget._after_ids.get(list(kw)[0], ' '))
    c1 = tuple(map(lambda a: a / 65535, widget.winfo_rgb(widget[list(kw)[0]])))
    c2 = tuple(map(lambda a: a / 65535, widget.winfo_rgb(list(kw.values())[0])))
    colors = tuple(colour.rgb2hex(c, force_long=True)
                   for c in colour.color_scale(c1, c2, max(1, smoothness * 15)))

    def worker(count=0):
        if len(colors) - 1 <= count: return
        widget.config({list(kw)[0]: colors[count]})
        widget._after_ids.update({list(kw)[0]: widget.after(
            max(1, int(smoothness / 10)), worker, count + 1)})

    worker()


def tkint_user_prompt():
    entry_var = tk.StringVar()

    font = ('Fira Sans', 20)

    parent = tk.Frame(root, bg='#2E3440')

    global label
    label = tk.Label(parent, text="Identify.", font=font, fg="#ffffff",
                     bg='#2E3440')
    label.pack(pady=(0, 3))

    global entry_widget
    entry_widget = tk.Entry(parent, textvariable=entry_var, bg='#2E3440', highlightthickness=2, relief='flat',
                            fg='#ffffff', highlightcolor='#ffffff', font=font, bd=2,
                            insertbackground='#2E3440', insertwidth=2, justify='center')
    entry_widget.bind('<Control-BackSpace>', entry_ctrl_bs)
    entry_widget.bind('<Control-Delete>', entry_ctrl_dl)
    entry_widget.bind('<Return>', partial(entry_enter, entry_widget, "#CED0D2", "#CED0D2"))

    entry_widget.pack(anchor='center')

    entry_var.trace_add('write', entry_cursor)

    parent.pack(expand=1)
    root.update()

    root.mainloop()

    root.mainloop()


def tkint_password_prompt():
    entry_var = tk.StringVar()

    font = ('Fira Sans', 20)

    parent = tk.Frame(root, bg='#2E3440')

    label = tk.Label(parent, text="Hello, rohan.", font=font, fg="#ffffff",
                     bg='#2E3440')
    label.pack(pady=(0, 3))

    global entry_widget
    entry_widget = tk.Entry(parent, textvariable=entry_var, bg='#2E3440', highlightthickness=2, relief='flat',
                            fg='#ffffff', highlightcolor='#ffffff', font=font, bd=2,
                            insertbackground='#2E3440', insertwidth=2, show="*", justify='center')
    entry_widget.bind('<Control-BackSpace>', entry_ctrl_bs)
    entry_widget.bind('<Control-Delete>', entry_ctrl_dl)

    entry_widget.pack(anchor='center')

    entry_var.trace_add('write', entry_cursor)

    parent.pack(expand=1)
    root.update()

    root.mainloop()


if __name__ == '__main__':
    tkint_user_prompt()
    tkint_password_prompt()

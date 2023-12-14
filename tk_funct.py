# imports all the necessary libraries
from tkinter import *
from login import *
import requests
import datetime

# create global time and format it
tdytime = datetime.datetime.now()
tdy = tdytime.strftime("%x")
timet = tdytime.strftime("%X")
tdy = tdy.replace("/", "-")
timet = timet.replace(":", "-")
datething = f"-{tdy}-{timet}.txt"


# creates the root tkinter window with options to Create Account, #Login, or Quit
def create_root():
    root = Tk()
    root.geometry("800x1000")
    create = Button(root, text='Create Account', command=lambda: create_window(root))
    create.grid(row=0, column=7)
    log = Button(root, text='Login', command=lambda: LoginWindow(root))
    log.grid(row=1, column=7)
    out = Button(root, text='Quit', command=root.destroy)
    out.grid(row=3, column=7)
    root.mainloop()


# returns whatever window is inputted back to the root window
def return_wind(login_wind, root, user):
    login_wind.destroy()
    root.deiconify()

def logout_wind(login_wind, root, user):
    updateLog(user, "logout")
    login_wind.destroy()
    root.deiconify()


# if an account is created successfully, returns to the root window
def check_create_acc(user, pword, fname, lname, create_wind, root):
    if create_acc(user, pword, fname, lname):
        updateLog(user, "create")
        create_wind.destroy()
        root.deiconify()


# creates a window where users can enter all the
# parameters #required to create an account and
# where users can create the account
def create_window(root):
    create_wind = Toplevel(root)
    root.withdraw()
    create_wind.title('Create Account')
    create_wind.geometry('500x500')
    user = Label(create_wind, text='Enter your username: ')
    user.grid(row=0, column=0)
    pword = Label(create_wind, text='Enter your password: ')
    pword.grid(row=1, column=0)
    fname = Label(create_wind, text='Enter your first name: ')
    fname.grid(row=2, column=0)
    lname = Label(create_wind, text='Enter your last name: ')
    lname.grid(row=3, column=0)
    e1 = StringVar()
    e2 = StringVar()
    e3 = StringVar()
    e4 = StringVar()
    userent = Entry(create_wind, textvariable=e1, bg="light gray", fg="black")
    userent.grid(row=0, column=1)
    pwordent = Entry(create_wind, textvariable=e2, bg="light gray", fg="black")
    pwordent.grid(row=1, column=1)
    fnament = Entry(create_wind, textvariable=e3, bg="light gray", fg="black")
    fnament.grid(row=2, column=1)
    lnament = Entry(create_wind, textvariable=e4, bg="light gray", fg="black")
    lnament.grid(row=3, column=1)
    enterbutton = Button(create_wind, text='Create', command=lambda: check_create_acc(userent.get(),
                        pwordent.get(), fnament.get(), lnament.get(), create_wind, root))
    enterbutton.grid(row=7, column=0)
    backbutton = Button(create_wind, text='Back', command=lambda: return_wind(create_wind, root, user))
    backbutton.grid(row=7, column=1)
    create_wind.mainloop()

#update the log file depending on the action given and update the gui's text box
def updateLog(username, action, extra=None):
    username_safe = username.replace(":", "_")
    username_safe = username_safe.replace("/", "_")
    datething_user = str(username_safe + datething)
    writestr = ""
    if action == "move":
        writestr = f"\n{username} moved the robot {extra} on {tdy} at {timet}"
    elif action == "create":
        writestr = f'\n{username} created an account on {tdy} at {timet}'
    elif action == "login":
        writestr = f'\n{username} logged into their account on {tdy} at {timet}'
    elif action == "logout":
        writestr = f'\n{username} logged out of their account on {tdy} at {timet}'
    with open(datething_user, "a") as file:
        file.write(writestr)
    # with open(datething_user, "r") as f:
    #     update_gui_log(f.readlines(), canvas, tank_wind)


# if a user logs in successfully, creates the Tank GUI window with,
# at the moment, a welcome statement and logout button
def check_logged_in(user, password, login_wind, root):
    try:
        valid, name = login(user, password)
    except TypeError:
        valid, name = False, "nope"
    if valid:
        global tank_wind
        tank_wind = Toplevel(login_wind)
        login_wind.withdraw()
        tank_wind.title('Tank Interface')
        tank_wind.geometry('500x500')
        global canvas
        canvas = Canvas(tank_wind, bg='white', height=500, width=500)
        updateLog(user, "login")
        canvas.pack()
        canvas.create_line(250, 0, 250, 500, fill='black')
        canvas.create_line(0, 250, 500, 250, fill='black')
        welcome = Label(tank_wind, text=f'Welcome {name.title()}')
        logout = Button(tank_wind, text='Logout', command=lambda: logout_wind(tank_wind, root, user))
        rev = ""
        username_safe = user.replace(":", "_")
        username_safe = username_safe.replace("/", "_")
        datething_user = str(username_safe + datething)
        with open(datething_user, "rt") as f:
            logtext = f.readlines()
        for line in reversed(logtext):
            rev += f"{line}\n"
        logtextbox = Label(tank_wind, text=rev)
        viewlog = Button(tank_wind, text='View Full Log', command=lambda: LogDataWind(tank_wind, user))
        forward = Button(tank_wind, text=u'\u2191', command=lambda: postData("forward", user))
        backward = Button(tank_wind, text=u'\u2193', command=lambda: postData("backward", user))
        right = Button(tank_wind, text=u'\u2192', command=lambda: postData("right", user))
        left = Button(tank_wind, text=u'\u2190', command=lambda: postData("left", user))
        play = Button(tank_wind, text=u'\u25B6', command=lambda: postData("go", user))
        stop = Button(tank_wind, text=u'\u2587', command=lambda: postData("stop", user))
        canvas.create_window(250, 20, window=welcome)
        canvas.create_window(400, 20, window=logout)
        canvas.create_window(250, 300, window=logtextbox)
        canvas.create_window(370, 100, window=forward)
        canvas.create_window(370, 200, window=backward)
        canvas.create_window(440, 150, window=right)
        canvas.create_window(300, 150, window=left)
        canvas.create_window(350, 150, window=play)
        canvas.create_window(390, 150, window=stop)
        canvas.create_window(400, 400, window=viewlog)
        tank_wind.mainloop()


# creates a window where the user can log into the Tank GUI,
# and the window notifies the user of successful login, incorrect password, or account nonexistence
def LoginWindow(root):
    login_wind = Toplevel(root)
    root.withdraw()
    login_wind.title('Login')
    login_wind.geometry('500x500')
    user = Label(login_wind, text='Enter your username: ')
    user.grid(row=0, column=0)
    pword = Label(login_wind, text='Enter your password: ')
    pword.grid(row=1, column=0)
    e1 = StringVar()
    e2 = StringVar()
    userent = Entry(login_wind, textvariable=e1, bg="light gray", fg="black")
    userent.grid(row=0, column=1)
    pwordent = Entry(login_wind, textvariable=e2, bg="light gray", fg="black")
    pwordent.grid(row=1, column=1)
    print(userent.get(), pwordent.get())
    enterbutton = Button(login_wind, text='Login',
                         command=lambda: check_logged_in(userent.get(), pwordent.get(), login_wind, root))
    enterbutton.grid(row=5, column=0)
    backbutton = Button(login_wind, text='Back', command=lambda: return_wind(login_wind, root, user))
    backbutton.grid(row=5, column=1)
    login_wind.mainloop()

#display full log
def LogDataWind(tank_wind, user):
    rev = ""
    ld_wind = Toplevel(tank_wind)
    ld_wind.title('Log Data')
    ld_wind.geometry('500x500')
    username_safe = user.replace(":", "_").replace("/", "_")
    datething_user = str(username_safe + datething)
    with open(datething_user, "r") as f:
        logtext = f.readlines()
    for line in reversed(logtext):
        rev += f"{line}\n"
    logtextbox = Label(ld_wind, text=rev)
    logtextbox.grid(row=5, column=1)
    ld_wind.mainloop()

# post http request with direction under key called button to a webserver
def postData(direct, user):
    url = "http://192.168.1.42:4200/"
    data = {'button': direct}
    r = requests.post(url, json=data)
    updateLog(user, "move", direct)


# def update_gui_log(logtext, canvas, wind):
#     rev = ""
#     for line in reversed(logtext):
#         rev += f"{line}\n"
#     logtextbox = Label(wind, text=rev)
#     canvas.create_window(250, 300, window=logtextbox)

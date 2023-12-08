# imports all the necessary libraries
from tkinter import *
from login import *
import requests


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
def Aeturn(login_wind, root, username=None):
  login_wind.destroy()
  root.deiconify()


# if an account is created succesfully, returns to the root window
def check_create_acc(user, pword, fname, lname, create_wind, root):
    logging_create(user)
    if create_acc(user, pword, fname, lname):
        Aeturn(create_wind, root)
      

def postDataMove(direct, user):
  
  url = "http://192.168.1.42:4200/moving"
  data = {'button': direct}
  r = requests.post(url, json=data)
  logging_movement(user, direct)


# creates a window where users can enter all of the parameters #required to create an account and where users can create the #account
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
    enterbutton = Button(create_wind, text='Create', command=lambda: check_create_acc(userent.get(), pwordent.get(), fnament.get(), lnament.get(), create_wind, root))
    enterbutton.grid(row=7, column=0)
    backbutton = Button(create_wind, text='Back', command=lambda: Aeturn(create_wind, root))
    backbutton.grid(row=7, column=1)
    create_wind.mainloop()



# if a user logs in successfully, creates the Tank GUI window with,
# #at the moment, a welcome statement and logout button
def check_logged_in(user, password, login_wind, root):
  
  rev = ""
  valid, name = login(user, password)
  if valid:
    tank_wind = Toplevel(login_wind)
    login_wind.withdraw()
    tank_wind.title('Tank Interface')

    tank_wind.geometry('500x500')
    canvas = Canvas(tank_wind, bg='white', height=500, width=500)
    canvas.pack()
    canvas.create_line(250, 0, 250, 500, fill='black')
    canvas.create_line(0, 250, 500, 250, fill='black')
    welcome = Label(tank_wind, text=f'Welcome {name.title()}')
    logout = Button(tank_wind, text='Logout', command=lambda: logging_out(tank_wind, root, user))
    with open("log.txt", "rt") as f:
      logtext = f.readlines()
    for line in reversed(logtext):
      rev += f"{line}\n"
    logtextbox = Label(tank_wind, text=rev)
    viewlog = Button(tank_wind,text = 'View Full Log', command=lambda: LogDataWind(tank_wind))
    forward = Button(tank_wind, text=u'\u2191', command=lambda: postDataMove("forward", user))
    backward = Button(tank_wind, text=u'\u2193', command=lambda: postDataMove("backward", user))
    right = Button(tank_wind, text=u'\u2192', command=lambda: postDataMove("right", user))
    left = Button(tank_wind, text=u'\u2190', command=lambda: postDataMove("left", user))
    play = Button(tank_wind, text=u'\u25B6', command=lambda: postDataMove("go", user))
    stop = Button(tank_wind, text=u'\u2587', command=lambda: postDataMove("stop", user))
    #log_data = Button(tank_wind, text='View Full Log', command=lambda: postData("stop", user))
    tank_wind.bind('<Up>', lambda:postDataMove('forward',user))
    tank_wind.bind('<Down>', lambda:postDataMove('backward',user))
    tank_wind.bind('<Left>',lambda:postDataMove('left',user))
    tank_wind.bind('<Right>',lambda:postDataMove('right',user))
    canvas.create_window(250, 20, window=welcome)
    canvas.create_window(400, 20, window=logout)
    canvas.create_window(370, 300, window=logtextbox)
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
    backbutton = Button(login_wind, text='Back', command=lambda: Aeturn(login_wind, root))
    backbutton.grid(row=5, column=1)
    login_wind.mainloop()


def logging_out(tank_wind, root, username):
  Aeturn(tank_wind, root, username)
  logging_movement (username, 'logout')
                


def LogDataWind(tank_wind):
  rev = ""
  ld_wind = Toplevel(tank_wind)
  ld_wind.title('Log Data')
  ld_wind.geometry('500x500')
  with open("log.txt", "rt") as f:
    logtext = f.readlines()
  for line in reversed(logtext):
    rev += f"{line}\n"
  logtextbox = Label(ld_wind, text=rev)
  logtextbox.grid(row = 5, column=1)
  ld_wind.mainloop()
  # returnbutton = Button(ld_wind, text='Close Log', command=lamda: )
  
def logging_create(username):
  try:
      tdytime = datetime.datetime.now()
      tdy = tdytime.strftime("%x")
      timet = tdytime.strftime("%X")

      # Replace invalid characters in the filename
      username_safe = username.replace(":", "_").replace("/", "_")
      tdy = tdy.replace(":", "_").replace("/", "_")
      timet = timet.replace(":", "_").replace("/", "_")

      fileName = f"{username_safe}-{tdy}-{timet}.txt"

      writestr = f"\n{username} created an account on {tdy} at {timet}"

      with open(fileName, "w") as f:
          f.write(writestr)

  except Exception as e:
    print(f"An error occurred: {e}")

def all_log(username, direction, thingy):
  if thingy == 'loggingin':
    tdytime = datetime.datetime.now()
    tdy = tdytime.strftime("%x")
    timet = tdytime.strftime("%X")
    
    file_time = timet
   
    file_tdy = tdy

    username_safe = username.replace(":", "_").replace("/", "_")
    tdy = tdy.replace(":", "_").replace("/", "_")
    timet = timet.replace(":", "_").replace("/", "_")
    
    f = open(f"{username}-{tdy}-{timet}.txt", "a")
    writestr = f'\n{username} logged into their account'
    f.write(writestr)
  elif thingy == 'movement':
    logging_movement(username, direction)
    

def logging_movement(username, direction):
  tdytime = datetime.datetime.now()
  tdy = tdytime.strftime("%x")
  timet = tdytime.strftime("%X")
  username_safe = username.replace(":", "_").replace("/", "_")
  tdy = tdy.replace(":", "_").replace("/", "_")
  timet = timet.replace(":", "_").replace("/", "_")
  f = open(f"{username}-{tdy}-{timet}.txt", "a")
  if direction == 'forward':
    writestr = f"\n{username} moved the robot {direction} on {tdy} at {timet}"
  elif direction == 'backward':
    writestr = f"\n{username} moved the robot {direction} on {tdy} at {timet}"
  elif direction == 'left':
    writestr = f"\n{username} moved the robot {direction} on {tdy} at {timet}"
  elif direction == 'right':
    writestr = f"\n{username} moved the robot {direction} on {tdy} at {timet}"
  elif direction == 'go':
    writestr = f"\n{username} moved the robot {direction} on {tdy} at {timet}"
  elif direction == 'stop':
    writestr = f"\n{username} stopped the robot on {tdy} at {timet}"
  elif direction == 'logout':
    writestr = f"\n{username} logged out on {tdy} at {timet}"
  f.write(writestr)

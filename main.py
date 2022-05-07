import pygame
import threading as thread
from pathlib import Path
from time import sleep
import requests
from tkinter import *
import datetime as dt
import random
import socket
import sys
import os

global me
global serverUrl
serverUrl = "http://arairon.xyz/"


def strcls(classname):
    return getattr(sys.modules[__name__], classname)


def getPar(s):
    return s[s.find("(") + 1:s.find(")")]


def exit():
    global me
    print("DISCONNECTING")
    try:
        me.send('/disconnect')
    except Exception as e:
        print(e)


global KillListeners
KillListeners = False


def killLis():
    global KillListeners
    KillListeners = True


class ch:
    def __init__(self, host, port, name):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = int(port)
        self.name = name

    def connect(self):
        try:
            self.s.close()
        except:
            pass
        if not self.port: self.port = int(17777)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        thread.Thread(target=self.listen, args=(), daemon=True).start()
        self.s.send(f'{self.name}'.encode('utf-8'))
        dprint("Connecting!")

    def send(self, text):
        msg = text
        if msg == '/start':
            self.s.send(f"%{msg.split('/')[1]}".encode('utf-8'))
        else:
            self.s.send(msg.encode('utf-8'))

    def listen(self):
        s = self.s
        global KillListeners
        while not KillListeners:
            try:
                msg = s.recv(1024)
                try:
                    if msg.decode('utf-8')[0] == "%":
                        try:
                            print(f'Executing remote command {msg.decode("utf-8").split("%")[1]}')
                            exec(msg.decode("utf-8").split("%")[1])
                        except Exception as e:
                            ConMenu.conText.insert(END,
                                                   f"{e}\nWhen executing remote command \n{msg.decode('utf-8').split('%')[1]}\n")
                    else:
                        print('\r\r' + msg.decode('utf-8') + '\n' + f'you: ', end='')
                        ConMenu.conText.insert(END, f"{msg.decode('utf-8')}\n")
                except IndexError:
                    print('\r\r' + msg.decode('utf-8') + '\n' + f'you: ', end='')
                    ConMenu.conText.insert(END, f"{msg.decode('utf-8')}\n")
                ConMenu.conText.see("end")
            except Exception as e:
                ConMenu.conText.insert(END, f"{e}\n")
        KillListeners = False
        print('Killed listener')


def connect():
    global me
    ip = ConMenu.conIP.get()
    port = ConMenu.conPORT.get()
    name = ConMenu.conNAME.get()
    if name:
        if not port:
            port = 17777
            dprint('Using default port (17777)')
        if not ip:
            ip = 'arairon.xyz'
            dprint('Using default ip (arairon.xyz)')
        me = ch(ip, int(port), name)
        me.connect()
    else:
        dprint('Name may not be empty!')


class Connector:
    def __init__(self):
        pass

    def run(self):
        try:

            self.root = Tk()
            self.root.geometry("500x200")
            self.frame = Frame(self.root)
            self.frame.grid(column=0)
            self.cnct = Frame(self.frame)
            self.cnct.grid(row=0, column=0)
            self.conIPlbl = Label(self.cnct, text='IP:')
            self.conIP = Entry(self.cnct)
            self.conIPlbl.grid(row=0, column=0)
            self.conIP.grid(row=0, column=1)
            self.conPORTlbl = Label(self.cnct, text='Port:')
            self.conPORT = Entry(self.cnct)
            self.conPORTlbl.grid(row=1, column=0)
            self.conPORT.grid(row=1, column=1)
            self.conNAMElbl = Label(self.cnct, text='Name:')
            self.conNAME = Entry(self.cnct)
            self.conNAMElbl.grid(row=2, column=0)
            self.conNAME.grid(row=2, column=1)
            self.conBUT = Button(self.cnct, text='Connect', command=connect)
            self.conBUT.grid(row=3, column=0, columnspan=2)
            self.conIDlbl = Label(self.cnct, text='ID(provided by server)')
            self.conID = Entry(self.cnct, width=5)
            self.conIDB = Button(self.cnct, width=5, text='get ID', command=lambda: dexec("getID()"))
            self.conIDlbl.grid(row=4, column=0, columnspan=2)
            self.conID.grid(row=5, column=0, columnspan=2)
            self.conIDB.grid(row=6, column=0, columnspan=2)

            self.conMenu = Frame(self.frame)
            self.conRun = Entry(self.conMenu, width=46)
            self.conRunB = Button(self.conMenu, text="Send", command=lambda: dsend(self.conRun.get()))
            self.conText = Text(self.conMenu, height=10, width=40)
            self.conMenu.grid(row=0, column=1)
            self.conText.grid(columnspan=2)
            self.conRun.grid(row=1, column=0)
            self.conRunB.grid(row=1, column=1)
            self.menubar = Menu(self.root, tearoff=0)
            #self.menubar.add_command(label="Reload")
            self.menubar.add_separator()
            self.settings_menu = Menu(self.menubar)
            #self.settings_menu.add_command(label="Toggle con/chat stuff")
            # settings_menu.add_checkbutton(label="Turn the board on move", onvalue=1, offvalue=0, variable=turnToggle)
            # settings_menu.add_checkbutton(label="Do NOT turn the board", onvalue=0, offvalue=1, variable=turnToggle)
            # settings_menu.add_command(label="Force turn the board", command = turn)
            # command = lambda: pieceSelected.setPiece(pieceColor.get() + "p")
            #self.menubar.add_cascade(label='Settings', menu=self.settings_menu)
            self.menubar.add_separator()

            self.cardType = StringVar()
            self.cardType.set('c')
            self.cardNum = StringVar()
            self.cardNum.set('14')
            self.debugMode = BooleanVar()
            self.debugMode.set(False)
            self.debug_sel = Menu(self.menubar)
            self.debug_sel.add_radiobutton(label="Spades", value='s', variable=self.cardType)
            self.debug_sel.add_radiobutton(label="Hearts", value='h', variable=self.cardType)
            self.debug_sel.add_radiobutton(label="Clubs", value='c', variable=self.cardType)
            self.debug_sel.add_radiobutton(label="Diamonds", value='d', variable=self.cardType)
            self.debug_sel.add_radiobutton(label='2', value='2', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='3', value='3', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='4', value='4', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='5', value='5', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='6', value='6', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='7', value='7', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='8', value='8', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='9', value='9', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='10', value='10', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='11', value='11', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='12', value='12', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='13', value='13', variable=self.cardNum)
            self.debug_sel.add_radiobutton(label='14', value='14', variable=self.cardNum)
            # self.debug_menu.add_command(label="Force turn the board", command = turn)
            # command = lambda: pieceSelected.setPiece(pieceColor.get() + "p")
            self.menubar.add_cascade(label='DebugSel', menu=self.debug_sel)
            self.debug_menu = Menu(self.menubar)
            self.debug_menu.add_checkbutton(label='DebugMode', onvalue=True, offvalue=False, variable=self.debugMode)
            #self.debug_menu.add_command(label="ToggleVis", command=lambda: dexec("dsel().visible = not dsel().visible"))
            # self.debug_menu.add_command(label="ToggleOnTable", command=lambda: dexec("dsel().onTable = not dsel().onTable"))
            # self.debug_menu.add_command(label="ToggleOnHand",command=lambda: dexec("dsel().onHand = not dsel().onHand"))
            #self.debug_menu.add_command(label="AddGOnTable", command=lambda: dexec("game.onTable.append(dsel())"))
           # self.debug_menu.add_command(label="AddPLOnHand", command=lambda: dexec("LocalPlayer.cards.add(dsel())"))
            self.moveOrigin = StringVar()
            self.moveTarget = StringVar()
            self.debug_menu.add_command(label="killLis()", command=lambda: dexec("killLis()"))
            self.debug_menu.add_command(label="Toggle lockID", command=lambda: dexec("lockID()"))
            self.debug_menu.add_command(label="test()", command=lambda: dexec("test()"))
            self.debug_menu.add_command(label="sendSync()", command=lambda: dexec("sendSync()"))
            self.debug_menu.add_command(label="reqSync()", command=lambda: dexec("reqSync()"))
            self.debug_menu.add_command(label="Move dsel()", command=lambda: dexec(f"cardMove(dsel(), {self.moveOrigin})"))
            self.menubar.add_cascade(label='DebugCmd', menu=self.debug_menu)
            self.move_menu = Menu(self.menubar)
            self.move_menu.add_radiobutton(label="LP.cards", value='LocalPlayer.cards', variable=self.moveOrigin)
            self.move_menu.add_radiobutton(label="game.deck", value='game.deck', variable=self.moveOrigin)
            self.move_menu.add_radiobutton(label="game.onTable", value='game.onTable', variable=self.moveOrigin)
            self.move_menu.add_radiobutton(label="game.discarded", value='game.discarded', variable=self.moveOrigin)
            self.move_menu.add_separator()
            self.move_menu.add_radiobutton(label="LP.cards", value='LocalPlayer.cards', variable=self.moveTarget)
            self.move_menu.add_radiobutton(label="game.deck", value='game.deck', variable=self.moveTarget)
            self.move_menu.add_radiobutton(label="game.onTable", value='game.onTable', variable=self.moveTarget)
            self.move_menu.add_radiobutton(label="game.discarded", value='game.discarded', variable=self.moveTarget)
            self.menubar.add_cascade(label='MoveSettings', menu=self.move_menu)
            self.root.config(menu=self.menubar)
            self.root.bind('<Return>', lambda event: dsend(self.conRun.get()))
            self.root.title("Connection menu")
            self.root.mainloop()
        except IndexError as e:
            print(f'Connect is dead > {e}')

    def print(self, text):
        self.conText.insert(END, text)
        self.conText.insert(END, '\n')

    def debExec(self, cmd):
        try:
            exec(cmd)
        except Exception as e:
            print(e)
            self.print(e)

    def stop(self):
        self.root.destroy()


def dsel():
    return strcls(f'card_{ConMenu.cardType.get()}{ConMenu.cardNum.get()}')


def send(text, shown=True):
    if shown: ConMenu.conText.insert(END, f"you: {text}\n")
    me.send(text)
    if shown: ConMenu.conText.see("end")


def gsend(text, target=None):
    try:
        if target is None:
            me.s.send(('%' + text).encode('utf-8'))
        else:
            me.s.send((f'%>{target}>' + text).encode('utf-8'))
        sleep(0.1)
    except NameError:
        dprint('You are not connected to the server')


ConMenu = Connector()
ConMenu.selfID = -1

thread.Thread(target=ConMenu.run, daemon=True).start()

global RUN


# pygame.image.load(path)
# pygame.transform.scale(img, (x,y))

def LifeCheck():
    print('HELL YEAH!')
    print(pygame.mouse.get_pos())
    dprint('HELL NO!')


def dcls():
    try:
        ConMenu.conText.delete(1.0, END)
    except Exception as e:
        print(f'ConMenu error > {e}')


def dprint(txt, debug=False):
    try:
        if not debug:
            ConMenu.print(txt)
            ConMenu.conText.see("end")
        if debug and ConMenu.debugMode.get():
            ConMenu.print(txt)
            ConMenu.conText.see("end")
    except Exception as e:
        print(f'ConMenu error > {e}')


def dexec(cmd):
    try:
        exec(cmd)
    except Exception as e:
        print(e)
        dprint(e)


def dsend(msg):
    if msg[0] == "#":
        dexec(msg.split('#')[1])
    elif ConMenu.debugMode.get():
        dexec(msg)
    else:
        send(msg)
    ConMenu.conText.see("end")


# Game part
global debugMode
debugMode = False
RUN = True

WinWidth, WinHeight = 1080, 720

pygame.init()
root = pygame.display.set_mode((WinWidth, WinHeight))
pygame.display.set_caption("Pain, but in a new way!")

FPS = 60


class Game:
    def __init__(self):
        self.gameType = 'durak'
        self.players = []
        self.cards = []
        self.deck = []
        self.discarded = set()
        self.onTable = set()
        self.trump = 's14'
        self.mover = None
        self.tableClickable = False

    def tableRow(self, row):
        tableSorted = sorted(self.onTable, key=lambda x: x.tableCoords[0])
        toRet = []
        for i in tableSorted:
            if i.tableCoords[1] == row:
                toRet.append(i)
        return toRet

    def getFromCoords(self, coords, row=None):
        if row is not None: coords = [coords, row]
        for i in game.onTable:
            if i.tableCoords == coords: return i
        return None



class Player:
    instances = []

    def __init__(self, name, rect, canMove=False):
        self.name = name
        self.rect = rect
        self.cards = set()
        self.visible = False
        self.canMove = canMove
        self.instances.append(self)

    def id(self):
        return self.name.split('-')[-1]

    def next(self, margin=1):
        try:
            return self.instances[self.instances.index(self) + margin]
        except IndexError:
            return self.instances[self.instances.index(self) + margin - len(self.instances)]

    def __str__(self):
        return str(self.__dict__)


class Card:
    instances = []
    lastClicked = None

    def __init__(self, name, img, rect):
        self.name = name
        self.img = img
        self.scale = 1
        self.rect = rect
        self.instances.append(self)
        self.visible = False
        self.onHand = False
        self.tableCoords = [-1, -1]
        self.HL = False

    def __str__(self):
        return self.name

    def onTable(self):
        if self in game.onTable: return True
        else: return False

    def isTrump(self, true = True):
        if self.name[0] == game.trump[0]: return true
        else: return not true


game = Game()


# def PLRinit(plrs):
#    for num, i in enumerate(plrs):
#        exec(f"plr{num} = Player('{i}', pygame.Rect(len(Player.instances)*100,0, 100, 120))")


def getID():
    try:
        send('/getID', False)
    except NameError:
        dprint('You are not connected to the server!')
        return
    for i in range(1, 11):
        if ConMenu.selfID == -1:
            sleep(0.5)
        else:
            break


def recvID(id):
    ConMenu.selfID = id
    ConMenu.conID.delete(0, END)
    ConMenu.conID.insert(0, id)
    sleep(0.05)
    lockID()


def plrID(id):
    for i in Player.instances:
        if i.name.split('-')[-1] == str(id):
            return i

    print(f'plrID failed on {id}')
    for i in Player.instances:
        print(i.__dict__)
    return f'plrID({id}) failed!'


def gmEncode(type='full'):
    if type.lower() == 'full':
        fullStr = 'FullState:::'
        for i in Player.instances:
            aplist = ''
            fullStr += i.name + '¡' + str(int(i.canMove)) + '|'
        fullStr = fullStr[:-1] + ':::'
        fullStr += game.trump + '|' + game.mover.name.split('-')[-1] + ':::'
        aplist = ''

        for i in game.deck:
            aplist += i.name + '/'
        fullStr += aplist[:-1] + '|'
        aplist = ''
        for i in game.discarded:
            aplist += i.name + '/'
        fullStr += aplist[:-1] + '|'
        aplist = ''
        for i in game.onTable:
            aplist += i.name + f'({i.tableCoords[0]},{i.tableCoords[1]})' + '/'
        fullStr += aplist[:-1] + '>>>'

        for i in Player.instances:
            aplist = ''
            fullStr += i.name.split('-')[-1] + '>'
            if len(i.cards) == 0: aplist += 'None/'
            for i in i.cards:
                aplist += i.name + '/'
            fullStr += aplist[:-1] + '~'
        fullStr = fullStr[:-1]
        print(fullStr)
        return fullStr
    elif type.lower() == 'plrs':
        fullStr = 'Players:::'
        for i in Player.instances:
            aplist = ''
            fullStr += i.name + '|'
        fullStr = fullStr[:-1] + '>>>'
        for i in Player.instances:
            aplist = ''
            fullStr += i.name.split('-')[-1] + '>'
            for i in i.cards:
                aplist += i.name + '/'
            fullStr += aplist[:-1] + '~'
        fullStr = fullStr[:-1]
        print(fullStr)
        return fullStr
    if type.lower() == 'game':
        fullStr = 'gameState:::'
        fullStr += game.trump + '|' + game.mover.name.split('-')[-1] + ':::'
        aplist = ''
        for i in game.deck:
            aplist += i.name + '/'
        fullStr += aplist[:-1] + '|'
        aplist = ''
        for i in game.discarded:
            aplist += i.name + '/'
        fullStr += aplist[:-1]
        print(fullStr)
        return fullStr


def getCard(name):
    if name[1] == 'a':
        return strcls(name)
    else:
        return strcls(f'card_{name}')


def gmDecode(msg):
    global LocalPlayer
    try:
        print(msg)
        msg1 = msg.split(':::')
        tag = msg1[0]
        msg1.remove(msg1[0])
        if tag == 'FullState':
            plrs = msg1[0].split('|')
            Player.instances = []
            for num, i in enumerate(plrs):
                name = i.split('¡')[0]
                exec(f"plr{num} = Player('{name}', pygame.Rect(len(Player.instances)*105 + 3,0, 100, 120))")
                plrID(name.split('-')[-1]).canMove = bool(int(i.split('¡')[-1]))
                if i.split("-")[-1] == ConMenu.selfID:
                    LocalPlayer = plrID(ConMenu.selfID)
            game.trump = msg1[1].split('|')[0]
            game.mover = plrID(msg1[1].split('|')[1])
            gLsts = msg1[2].split('>>>')[0]
            plrLsts = msg1[2].split('>>>')[1]
            apList = []
            for i in gLsts.split('|')[0].split('/'):
                if i:
                    try:
                        apList.append(getCard(i))
                    except:
                        print('Error when decoding gLsts1 ' + i)
            game.deck = list(apList)
            apList = []
            for i in gLsts.split('|')[1].split('/'):
                if i:
                    try:
                        apList.append(getCard(i))
                    except:
                        print('Error when decoding gLsts2 ' + i)
            game.discarded = list(apList)
            apList = []
            for i in gLsts.split('|')[2].split('/'):
                if i:
                    try:
                        card = i.split('(')[0]
                        coords = getPar(i).split(',')
                        apList.append(getCard(card))
                        getCard(card).tableCoords = int(coords[0]), int(coords[1])
                    except:
                        print('Error when decoding gLsts3 ' + i)
            game.onTable = set(apList)
            for ii in plrLsts.split('~'):
                plr = plrID(ii.split('>')[0])
                apList = []
                if ii.split('>')[1] == 'None':
                    plr.cards = []
                    continue
                for i in ii.split('>')[1].split('/'):
                    try:
                        apList.append(getCard(i))
                    except:
                        print(f'Error when decoding plrLsts {ii} > {i}')
                plr.cards = apList
            LocalPlayer = plrID(ConMenu.selfID)
        elif tag == 'plrsInit':
            if Player.instances[0].name == 'Null':
                exec(
                    f"plr1 = Player('{ConMenu.conNAME.get()}-{ConMenu.selfID}', pygame.Rect((len(Player.instances)-1) * 100, 0, 100, 120))")
                Player.instances[0] = Player.instances[1]
                Player.instances.pop()
            exec(
                f"plr{len(Player.instances) + 1} = Player('{msg1[-1]}', pygame.Rect((len(Player.instances))*100,0, 100, 120))")
            if msg1[-1].split("-")[-1] == ConMenu.selfID:
                dprint('ERROR, A player with this tag already exists')
            LocalPlayer = plrID(ConMenu.selfID)
        elif tag == 'gameState':
            game.trump = msg1[1].split('|')[0]
            game.mover = plrID(msg1[1].split('|')[1])
            gLsts = msg1[2].split('>>>')[0]
            apList = []
            for i in gLsts.split('|')[0].split('/'):
                if i: apList.append(getCard(i))
            game.deck = set(apList)
            apList = []
            for i in gLsts.split('|')[1].split('/'):
                if i: apList.append(getCard(i))
            game.discarded = set(apList)
        else:
            print(f'Decoding tag {tag} is invalid')
    except Exception as e:
        print(f"Msg decode error > {e}")
        dprint(f"Msg decode error > {e}")


def sendSync(type='full', target=None):
    if type == 'full':
        gsend(f'gmDecode("{gmEncode("full")}")', target)


def reqSync(type='full'):
    print('req sync')
    if type == 'players':
        gsend(f'sendPlr({ConMenu.selfID})')
        pass
    elif type == 'full':
        pass


def lockID(value=None):
    tdict = {
        False: 'normal',
        True: 'disabled',
        'normal': True,
        'disabled': False
    }
    if value is None: value = tdict[ConMenu.conID['state']]
    ConMenu.conID['state'] = tdict[value]


def sendPlr(target):
    print(f'sending {ConMenu.conNAME.get()}-{ConMenu.selfID} to {target}')
    gsend(f'gmDecode("plrsInit:::{ConMenu.conNAME.get()}-{ConMenu.selfID}")', target)


# gsend('gmDecode("plrsInit:::tB-13")', 12)


def download(url, saveas=None):
    try:
        if saveas is None: saveas = url.split('/')[-1]
        print(f"requesting {url.split('/')[-1]} from {url} as {saveas}")
        r = requests.get((url), allow_redirects=True)
        open(saveas, 'wb').write(r.content)
    except:
        print(f'Error downloading {url}')


userDir = Path.home()
araiDir = os.path.join(userDir, 'Arai-stuff')
exeDir = os.getcwd()
filesInvalid = False
url = serverUrl + 'pyLib/cards/'
os.chdir(userDir)
if not os.path.isdir('Arai-Stuff'): os.mkdir('Arai-Stuff')
os.chdir('Arai-Stuff')
download((serverUrl + 'pyLib/readme.txt'))
if not os.path.isdir('.cardAssets'): os.mkdir('.cardAssets')
os.chdir('.cardAssets')
print('Updating asset list')
try:
    download((url + 'AssetList.txt'))
except:
    print('error getting asset list')
    dprint('error getting asset list')
    open(f'AssetList.txt', 'wb').write('\n').flush().close()
with open('AssetList.txt', 'r') as assetList:
    fileList = assetList.readlines()
    for i in fileList:
        if not os.path.isfile(i[:-1]):
            download((url + f'{i[:-1]}'), f'{i[:-1]}')
os.chdir(araiDir)

cardSize = (88, 124)
# for i in range(2, 15):
for i in range(6, 15):
    for j in "chsd":
        try:
            exec(f"{j}{i}Img = pygame.image.load(os.path.join('.cardAssets', '{j}{i}.png'))")
            exec(f"{j}{i}Rect = pygame.Rect(-1000,0, cardSize[0], cardSize[1])")
            exec(f"card_{j}{i} = Card('{j}{i}', {j}{i}Img, {j}{i}Rect)")
        except Exception as e:
            print(f"{e}\n@{j}{i}.png")
            dprint(f"{e}\n@{j}{i}.png")

dudePic = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'dude.png')), (100, 100))
dudeHL = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'DudePicHighlight.png')).convert_alpha(),
                                (100, 100))
dudeMove = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'DudePicMove.png')).convert_alpha(),
                                  (100, 100))
dudeDef = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'DudePicDef.png')).convert_alpha(),
                                 (100, 100))
cardHL = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'CardHighlight.png')).convert_alpha(),
                                cardSize)
cardBack = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'cardBack.png')).convert_alpha(),
                                  cardSize)
beatenButImg = pygame.transform.scale(
    pygame.image.load(os.path.join('.cardAssets', 'beatenButton.png')).convert_alpha(),
    cardSize)
tahoma = pygame.font.Font(r'.cardAssets\tahoma.ttf', 17)
bombard = pygame.font.Font(r'.cardAssets\bombard.ttf', 20)
uiTable = pygame.Rect(0, WinHeight / 6, WinWidth - (WinWidth / 6), WinHeight - (WinHeight - 50 - cardSize[1] * 2))
uiEnemies = pygame.Rect(0, 0, WinWidth, WinHeight / 6)
uiRightbar = pygame.Rect(WinWidth - WinWidth / 8, WinHeight / 6, WinWidth / 6, WinHeight - WinHeight / 6)
uiSeparator = pygame.Rect(0, WinHeight - 50 - cardSize[1] * 2, WinWidth, 20)

tblMargin = 10
tblX = 0 + tblMargin
tblY = WinHeight / 6 + tblMargin
handX = 0 + tblMargin
handY = WinHeight - tblMargin - cardSize[1] * 2

global LocalPlayer
LocalPlayer = Player('Null', pygame.Rect(-100, -100, 1, 1))

def hexc(st):
    if st[0] == '#': list(st).pop(0).join()
    st = st.lower()
    if len(st) == 1: st = st * 6
    if len(st) == 2: st = st * 3
    s1 = int((st[0] + st[1]), 16)
    s2 = int((st[2] + st[3]), 16)
    s3 = int((st[4] + st[5]), 16)
    return (s1, s2, s3)

class Popup:
    instances = []

    def __init__(self, text='Text Missing', surface=root, x=0, y=0, font=None, color=(255, 255, 255), time=3, fadespeed = 10):
        self.text = text
        self.surface = surface
        self.x = x
        self.y = y
        self.font = font
        self.origColor = color
        self.color = color
        self.time = time
        self.fadespeed = fadespeed
        self.active = True
        self.fading = False
        self.instances.append(self)
        self.trun()

    def set(self, text=None, surface=None, x=None, y=None, font=None, color=None, time=1, fadespeed = 10):
        if text is not None: self.text = text
        if surface is not None: self.surface = surface
        if x is not None: self.x = x
        if y is not None: self.y = y
        if font is not None: self.font = font
        if color is None: self.color = self.origColor
        else: self.color = color
        self.active = True
        self.fading = False
        self.time = time
        self.fadespeed = fadespeed
        self.trun()

    def popup(self, text='Text not set!', color=None, time=1):
        if color is None: self.color = self.origColor
        else: self.color = color
        self.text = text
        self.time = time
        self.active = True
        self.fading = False
        self.trun()

    def trun(self):
        thread.Thread(target=self.run, args=(), daemon=True).start()

    def run(self):
        sleep(self.time)
        self.fading= True

    def check(self):
        if self.fading:
            self.fade()
            if sum(self.color) < 40:
                self.fading = False
                self.active = False

    def draw(self):
        if self.active:
            #print(f'{self.text=}, {self.surface=}, {self.x=}, {self.y=}, {self.font=}, {self.color=}')
            overlay = pygame.Surface(((len(self.text)*8 + 10), 25))
            overlay.fill(hexc('40'))
            overlay.set_alpha(130)
            root.blit(overlay, (self.x - (len(self.text)*4) - 6, self.y))
            draw_text(self.text, self.surface, self.x - (len(self.text)*4), self.y, self.font, self.color)
            self.check()

    def fade(self):
        speed = self.fadespeed
        self.color = (max((self.color[0] - speed), 0), max((self.color[1] - speed), 0), max((self.color[2] - speed), 0))

notifier = Popup('Notifier active!', root, uiTable.width / 2, uiTable.height / 2 - 2, bombard, hexc('00aa00'), 3, 10)


def draw_text(text, surface, x, y, font=None, color=(255, 255, 255)):
    global tahoma
    if font is None: font = tahoma
    for l in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
        if l in text.lower():
            font = tahoma
    textobj = pygame.font.Font.render(font, text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def draw_background():
    global debugMode
    if debugMode: return
    root.fill((64, 64, 64))
    pygame.draw.rect(root, (128, 128, 128), uiEnemies)
    pygame.draw.rect(root, (30, 30, 30), uiSeparator)
    pygame.draw.rect(root, (153, 153, 153), uiRightbar)


def reloadAv():
    try:
        for i in Card.instances:
            if (i in LocalPlayer.cards) or (i in game.onTable):
                i.visible = True
            else:
                i.visible = False
    except:
        pass


x, y = uiRightbar.x, uiRightbar.y
deckX, deckY = (x + (uiRightbar.width / 2)) - (cardSize[1] / 2), y + 100
beatenB = pygame.Rect(deckX, deckY + 350, cardSize[0], cardSize[1])

global StopUpdates
StopUpdates = False


def ToggleWinUpd(force=None):
    global StopUpdates
    if force is None:
        StopUpdates = not StopUpdates
    else:
        StopUpdates = bool(force)


def winUpd():
    global StopUpdates
    if StopUpdates: return
    global LocalPlayer
    draw_background()
    reloadAv()

    for i in Card.instances:
        if (i in LocalPlayer.cards) or (i in game.onTable):
            if i in game.onTable:
                i.rect.x = tblX + ((tblMargin + cardSize[0]) * i.tableCoords[0])
                i.rect.y = tblY + ((tblMargin + cardSize[1]) * i.tableCoords[1])

            plrCards = sortCards(LocalPlayer.cards)
            if i in plrCards:
                i.rect.x = handX + (tblMargin / 2 + cardSize[0]) * (
                        list(plrCards).index(i) - (10 * (list(plrCards).index(i) // 10)))
                i.rect.y = handY + cardSize[1] * (list(plrCards).index(i) // 10)

            root.blit(i.img, (i.rect.x, i.rect.y))

            if i.HL:
                root.blit(cardHL, (i.rect.x, i.rect.y))

    for i in Player.instances:
        root.blit(dudePic, (i.rect.x, i.rect.y))
        if i == LocalPlayer:
            root.blit(dudeHL, (i.rect.x, i.rect.y))
        try:
            id = i.name.split('-')[1]
        except IndexError:
            id = '-1'
        name = i.name.split('-')[0]
        if len(name) > 10: name = name[:-(len(name) - 10)]
        fontOverride = False
        for l in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            if l in name.lower():
                draw_text(name, root, i.rect.x + 1, i.rect.y + 100)
                fontOverride = True
        if not fontOverride: draw_text(name, root, i.rect.x + 1, i.rect.y + 100, bombard)
        draw_text(str(id), root, (i.rect.x + 50 - (len(id) * 4)), i.rect.y + 20, bombard, (80, 80, 80))
        draw_text(str(len(i.cards)), root, (i.rect.x + 50 - len(str(len(i.cards))) * 4), i.rect.y + 75, bombard,
                  hexc('0'))
        if i == game.mover:
            if game.gameType == 'durak':
                root.blit(dudeDef, (i.rect.x, i.rect.y))
                draw_text('Defends', root, (i.rect.x + 16), i.rect.y + 2, bombard, (20, 20, 20))
            else:
                root.blit(dudeMove, (i.rect.x, i.rect.y))
                draw_text('ACT', root, (i.rect.x + 38), i.rect.y + 2, bombard, (20, 20, 20))

    x, y = uiRightbar.x, uiRightbar.y
    deckX, deckY = (x + (uiRightbar.width / 2)) - (cardSize[1] / 2), y + 100
    if game.trump:
        trumpcard = getCard(game.trump)
        root.blit(trumpcard.img, (deckX, deckY - (cardSize[1] / 2) + 10))
    root.blit(cardBack, (deckX, deckY))
    draw_text(f'{len(game.deck)}', root, deckX + (cardSize[0] / 2) - (len(f'{len(game.deck)}') * 6), deckY + 15,
              pygame.font.Font(r'.cardAssets\bombard.ttf', 25), hexc('00EEEE'))
    root.blit(beatenButImg, (beatenB.x, beatenB.y))
    draw_text(f'{len(game.discarded)}', root, deckX + (cardSize[0] / 2) - (len(f'{len(game.discarded)}') * 6),
              deckY + 365,
              pygame.font.Font(r'.cardAssets\bombard.ttf', 25), hexc('ff4336'))

    for i in ContextMenu.instances:
        if i.active: i.draw()

    for i in Popup.instances:
        i.draw()

    pygame.display.update()


def draw_init():
    root.fill((64, 64, 64))
    pygame.display.update()


def sortCards(cards):
    trump = game.trump[0]
    order = {'s': 4, 'c': 3, 'h': 2, 'd': 1, trump: 5}
    try:
        res = sorted(cards, key=lambda item: (int(order.get(item.name[0], 100)), item.name[1:-1]), reverse=True)
    except:
        res = sorted(cards, key=lambda item: (int(order.get(item[0], 100)), item[1:-1]), reverse=True)
    return res


def cardMove(object, origin, target):
    origin.remove(object)
    if type(target) == type(list()): target.append(object)
    if type(target) == type(set()): target.add(object)


def gamePrep():
    try:
        getID()
    except NameError:
        dprint('You must be connected to the server to start the game')
        return
    for i in range(1, 11):
        if ConMenu.selfID == -1:
            sleep(0.5)
        else:
            break


def runAsserts():
    if ConMenu.selfID == -1:
        dprint('ID error')
        return False


def gmUpd(noSend=False):
    for i in Card.instances:
        if i not in game.onTable:
            i.tableCoords = [-1, -1]
        if (i in game.discarded) or (i in game.deck):
            i.rect.x = -100
            i.rect.y = -100
    if len(game.tableRow(0)) > len(game.tableRow(1)): game.mover.canMove = True
    if (len(LocalPlayer.cards) == 0) and (len(game.deck) == 0) and ((len(game.tableRow(0))==len(game.tableRow(1))) or (game.mover != LocalPlayer)):
        gmWinner(LocalPlayer.name.split('-')[-1], True)
    if not noSend: sendSync()

def gmWinner(winner, orig=False):
    if orig: gsend(f'gmWinner({winner})')
    winner = plrID(winner)
    for i in list(game.onTable)[:]: cardMove(i, game.onTable, game.discarded)
    for i in list(LocalPlayer.cards)[:]: cardMove(i, LocalPlayer.cards, game.discarded)
    winPop = Popup(f'Congrats, {winner.name}! You have won the game!', root, uiTable.width / 2, uiTable.height / 2 + 40, bombard, hexc('00eeee'))

def nextRound(changePlayer = True):
    for i in Player.instances:
        i.canMove = False
    if changePlayer:
        game.mover = game.mover.next()
    game.mover.next().canMove = True
    game.mover.next(-1).canMove = True
    for i in Player.instances:
        while len(i.cards) < 6 and game.deck:
            cardMove(game.deck[0], game.deck, i.cards)
    for i in list(game.onTable)[:]: cardMove(i, game.onTable, game.discarded)


    gmUpd()



def startDurak():
    gsend('game.tableClickable=True')
    game.tableClickable=True
    for i in range(6, 15):
        for j in "chsd":
            try:
                game.cards.append(getCard(j + str(i)))
                game.deck.append(getCard(j + str(i)))
            except Exception as e:
                print(e)
    game.players = Player.instances
    random.shuffle(game.deck)
    game.trump = game.deck[-1].name
    for i in game.players:
        for num in range(1, 7):
            cardMove(game.deck[0], game.deck, i.cards)
    plrCards = []
    for i in game.players:
        plrCards += i.cards
    trump = game.trump
    order = {'s': 4, 'c': 3, 'h': 2, 'd': 1, trump[0]: 5}
    highestCard = sorted(plrCards, key=lambda item: (int(order.get(item.name[0], 100)), item.name[1:]), reverse=True)
    highestCard = highestCard[0]
    print(f'{highestCard.__dict__=}')
    for i in game.players:
        print(f'{i.cards=}')
        try:
            if (highestCard in i.cards): game.mover = i.next()
        except Exception as e:
            print('highest card failed > ', e)
    game.mover.next().canMove = True
    game.mover.next(-1).canMove = True
    sendSync()


global selectedCard
selectedCard = None


def select(card):
    global selectedCard
    Card.lastClicked = card
    print(card.name + 'select called')
    if not selectedCard and LocalPlayer.canMove:
        print(card.name + 'selected')
        selectedCard = card
        card.HL = True
    elif card == selectedCard:
        print(card.name + 'deselected')
        selectedCard = None
        card.HL = False

def beatenClick():
    if len(game.tableRow(0)) == len(game.tableRow(1)) and ((LocalPlayer != game.mover) or (len(game.tableRow(0)) == 6)):
        nextRound()
    elif LocalPlayer == game.mover and (not len(game.tableRow(0)) == len(game.tableRow(1))):
        for i in list(game.onTable)[:]: cardMove(i, game.onTable, LocalPlayer.cards)
        nextRound(False)


def tableClick():
    global selectedCard
    if not selectedCard:
        print('Card not selected')
        return
    if not Card.lastClicked:
        print('Error: no cards were ever clicked')
        return
    gmUpd(True)
    try:
        if (not selectedCard.onTable()) and (LocalPlayer != game.mover) and LocalPlayer.canMove and (len(game.tableRow(0)) < (len(game.mover.cards)+len(game.tableRow(1)))) and (len(game.tableRow(0)) < 6):
            selectedCard.tableCoords = [len(game.tableRow(0)), 0]
            if len(game.tableRow(0)) == 0: cardMove(selectedCard, LocalPlayer.cards, game.onTable)
            else:
                nope = True
                for i in game.onTable:
                    if str(selectedCard)[1:] == str(i)[1:]: nope = False
                if nope: raise AssertionError('No cards with this value on table')
                cardMove(selectedCard, LocalPlayer.cards, game.onTable)
        elif (LocalPlayer == game.mover) and LocalPlayer.canMove:
            click = Card.lastClicked
            if not click.onTable(): raise AssertionError('The last clicked card is not on table')
            try:
                if game.getFromCoords(click.tableCoords[0], 1): raise AssertionError('This card is already beaten')
            except IndexError: pass
            if int(selectedCard.name[1:]) > int(click.name[1:]) and (selectedCard.name[0] == click.name[0]) and click.isTrump(False):
                selectedCard.tableCoords = [click.tableCoords[0], 1]
                cardMove(selectedCard, LocalPlayer.cards, game.onTable)
            elif selectedCard.isTrump() and click.isTrump(False):
                selectedCard.tableCoords = [click.tableCoords[0], 1]
                cardMove(selectedCard, LocalPlayer.cards, game.onTable)
            elif selectedCard.isTrump() and click.isTrump() and int(selectedCard.name[1:]) > int(click.name[1:]):
                selectedCard.tableCoords = [click.tableCoords[0], 1]
                cardMove(selectedCard, LocalPlayer.cards, game.onTable)
            else: raise AssertionError("Card's value is too low")
        else:
            if not LocalPlayer.canMove: raise AssertionError("You can't move right now!")
            elif len(game.tableRow(0)) >= len(game.mover.cards): raise AssertionError("The player doesn't have enough cards!")
            elif len(game.tableRow(0)) >= 6: raise AssertionError("Too many cards on the table!")
            else: raise AssertionError('Unable to tableClick(), unknown reason')
            #notifier.set('Unable to do that', root, uiTable.width/2-36, uiTable.height/2-3, bombard,hexc('ee1e1e'), 2)
    except AssertionError as e: notifier.popup(str(e), hexc('ee1e1e'))
    selectedCard.HL = False
    selectedCard = None
    gmUpd()


class cmButton:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.rect = pygame.Rect(0, 0, 150, 30)


class ContextMenu:
    instances = []

    def __init__(self, buttons=[], dButs=[]):
        self.instances.append(self)
        self.active = False
        self.debug = False
        self.pos = tuple()
        self.buttons = buttons
        self.dButs = dButs
        self.debug = False

    def set(self, xy, y=None):
        if type(xy) != type(tuple()): xy = (xy, y)
        self.pos = xy
        self.active = True

    def draw(self):
        pass
        for i in self.buttons:
            i.rect.x = self.pos[0]
            i.rect.y = self.pos[1] + ((i.rect.height + 1) * self.buttons.index(i))
            pygame.draw.rect(root, (170, 170, 170), i.rect)
            # root.blit(root, (i.rect.x, i.rect.y))
            draw_text(i.name, root, i.rect.x + 10, i.rect.y + 2)
        if self.debug:
            for i in self.dButs:
                i.rect.x = self.pos[0]
                i.rect.y = self.pos[1] + ((i.rect.height + 1) * (self.dButs.index(i) + len(self.buttons)))
                pygame.draw.rect(root, (170, 170, 170), i.rect)
                # root.blit(root, (i.rect.x, i.rect.y))
                draw_text(i.name, root, i.rect.x + 10, i.rect.y + 2)

    def run(self, f):
        funcs = ['LifeCheck()', 'TgDebug', 'startDurak()', 'plrsInit', 'testPopup','None']
        if f not in funcs:
            dexec(f)
        else:
            if f == funcs[0]:
                LifeCheck()
            elif f == funcs[1]:
                ConMenu.debugMode.set((not self.debug))
                self.debug = not self.debug
            elif f == funcs[2]:
                print('Starting durak')
                gamePrep()
                gsend('gamePrep()')
                startDurak()
                gsend('menu.closeAll()')
                for i in ContextMenu.instances:
                    i.active = False
                pass
            elif f == funcs[3]:
                reqSync('players')
            elif f == funcs[4]:
                notifier.popup('Testing popup!', hexc('ee00ee'))


    def hide(self):
        self.active = False

    def closeAll(self):
        game.tableClickable = True
        for i in self.instances:
            i.active = False


buttons = [
    cmButton('Test', 'LifeCheck()'),
    cmButton('Toggle debug', 'TgDebug')
]
dButs = [
    cmButton('Debug Is On', 'dprint("Yes, it is on!")'),
    cmButton('RunPopup', 'testPopup')
]
menu = ContextMenu(buttons, dButs)
buttons = [
    cmButton('Get Players', 'plrsInit'),
    cmButton('Durak', 'startDurak()'),
    cmButton("Close this menu", 'menu.closeAll()')
]
starter = ContextMenu(buttons)


def test():
    gmDecode(
        'FullState:::Arai-1¡1|B-2¡0|Я-3¡0:::s10|1:::c7/c6/h7/s7/d6/d7/h6/s6|s13|s12(0,0)>>>1>s11/s10/c11/h10/s9/c10/d11/d9/d10/h11~2>s8/h9/d8/h8/c8/c9')


# 355 180
def main():
    lmbhandling = False
    rmbhandling = False
    global RUN
    clock = pygame.time.Clock()
    draw_init()
    starter.set(355, 180)
    starter.draw()
    while RUN:
        # try:
        clock.tick(FPS)
        for event in pygame.event.get():
            # print(f"EVENT - {event}")
            if event.type == pygame.QUIT:
                RUN = False

        keys_pressed = pygame.key.get_pressed()
        # if keys_pressed[pygame.K_smth]:

        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not lmbhandling:
            lmbhandling = True
            for m in ContextMenu.instances:
                if m.active:
                    for i in m.buttons:
                        if i.rect.collidepoint(pos):
                            m.run(i.func)
                            continue
                    if menu.debug:
                        for i in m.dButs:
                            if i.rect.collidepoint(pos):
                                m.run(i.func)
                                continue
            for i in Card.instances:
                if i.rect.collidepoint(pos):
                    select(i)
                    continue

            if uiTable.collidepoint(pos) and game.tableClickable:
                dprint('tableclick')
                tableClick()
                continue

            if beatenB.collidepoint(pos) and game.tableClickable:
                dprint('beatenB click')
                beatenClick()
                continue

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not rmbhandling:
            rmbhandling = True
            if menu.active:
                menu.hide()
            else:
                menu.set(pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            lmbhandling = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            rmbhandling = False

        winUpd()
    # except Exception as e:
    #    print(f'ERROR >> {e}')
    #    try:
    #        send(f'Player {plrID(LocalPlayer)} > {e}')
    #    except: pass

    pygame.quit()


ConMenu.conNAME.insert(0, 't')
main()
exit()

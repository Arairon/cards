import pygame
import threading as thread
import requests
from tkinter import *
import socket
import sys
import os

global me
global serverUrl
serverUrl = "http://arairon.xyz/"


def strcls(classname):
    return getattr(sys.modules[__name__], classname)


def exit():
    global me
    print("DISCONNECTING")
    try:
        me.send('/disconnect')
    except Exception as e:
        print(e)


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
        while True:
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
            self.conIDlbl.grid(row=4, column=0, columnspan=2)
            self.conID.grid(row=5, column=0, columnspan=2)

            self.conMenu = Frame(self.frame)
            self.conRun = Entry(self.conMenu, width=46)
            self.conRunB = Button(self.conMenu, text="Send", command=lambda: dsend(self.conRun.get()))
            self.conText = Text(self.conMenu, height=10, width=40)
            self.conMenu.grid(row=0, column=1)
            self.conText.grid(columnspan=2)
            self.conRun.grid(row=1, column=0)
            self.conRunB.grid(row=1, column=1)
            self.menubar = Menu(self.root, tearoff=0)
            self.menubar.add_command(label="Style")
            self.menubar.add_command(label="Reload")
            self.menubar.add_separator()
            self.settings_menu = Menu(self.menubar)
            self.settings_menu.add_command(label="Toggle con/chat stuff")
            # settings_menu.add_checkbutton(label="Turn the board on move", onvalue=1, offvalue=0, variable=turnToggle)
            # settings_menu.add_checkbutton(label="Do NOT turn the board", onvalue=0, offvalue=1, variable=turnToggle)
            # settings_menu.add_command(label="Force turn the board", command = turn)
            # command = lambda: pieceSelected.setPiece(pieceColor.get() + "p")
            self.menubar.add_cascade(label='Settings', menu=self.settings_menu)
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
            # self.debug_sel.add_radiobutton(label='2', value='2', variable=self.cardNum)
            # self.debug_sel.add_radiobutton(label='3', value='3', variable=self.cardNum)
            # self.debug_sel.add_radiobutton(label='4', value='4', variable=self.cardNum)
            # self.debug_sel.add_radiobutton(label='5', value='5', variable=self.cardNum)
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
            self.debug_menu.add_command(label="ToggleVis", command=lambda: dexec("dsel().visible = not dsel().visible"))
            # self.debug_menu.add_command(label="ToggleOnTable", command=lambda: dexec("dsel().onTable = not dsel().onTable"))
            # self.debug_menu.add_command(label="ToggleOnHand",command=lambda: dexec("dsel().onHand = not dsel().onHand"))
            self.debug_menu.add_command(label="AddGOnTable", command=lambda: dexec("game.onTable.add(dsel())"))
            self.debug_menu.add_command(label="AddPLOnHand", command=lambda: dexec("LocalPlayer.cards.add(dsel())"))
            self.menubar.add_cascade(label='DebugCmd', menu=self.debug_menu)
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


def send(text):
    ConMenu.conText.insert(END, f"you: {text}\n")
    me.send(text)
    ConMenu.conText.see("end")


def gsend(text):
    me.s.send(('%' + text).encode('utf-8'))


ConMenu = Connector()

thread.Thread(target=ConMenu.run).start()

global RUN


# pygame.image.load(path)
# pygame.transform.scale(img, (x,y))

def LifeCheck():
    print('HELL YEAH!')
    dprint('HELL NO!')


def dcls():
    try:
        ConMenu.conText.delete(1.0, END)
    except Exception as e:
        print(f'ConMenu error > {e}')


def dprint(txt):
    try:
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
    def __init__(self, cards):
        self.players = set()
        self.cards = set(cards)
        self.deck = set(cards)
        self.discarded = set()
        self.onHands = set()
        self.onTable = set()
        self.trump = ''
        self.mover = None


class Player:
    instances = []

    def __init__(self, name, rect):
        self.name = name
        self.rect = rect
        self.cards = set()
        self.visible = False
        self.instances.append(self)


class Card:
    instances = []

    def __init__(self, name, img, rect):
        self.name = name
        self.img = img
        self.scale = 1
        self.rect = rect
        self.instances.append(self)
        self.visible = False
        self.onTable = False
        self.onHand = False
        self.tableCoords = [-100, -100]
        self.HL = False


game = Game(Card.instances)


# def PLRinit(plrs):
#    for num, i in enumerate(plrs):
#        exec(f"plr{num} = Player('{i}', pygame.Rect(len(Player.instances)*100,0, 100, 120))")
def plrID(id):
    for i in Player.instances:
        if i.name.split('-')[-1] == str(id):
            return i

    print('plrID failed!')
    return f'plrID({id}) failed!'


def gmEncode(type='full'):
    if type.lower() == 'full':
        fullStr = 'FullState:::'
        for i in Player.instances:
            aplist = ''
            fullStr += i.name + '|'
        fullStr = fullStr[:-1] + ':::'
        fullStr += game.trump + '|' + game.mover.name.split('-')[-1] + ':::'
        aplist = ''

        for i in game.deck:
            aplist += i.name + '/'
        fullStr += aplist[:-1] + '|'
        aplist = ''
        for i in game.discarded:
            aplist += i.name + '/'
        fullStr += aplist[:-1] + '>>>'
        print(fullStr)

        for i in Player.instances:
            aplist = ''
            fullStr += i.name.split('-')[-1] + '>'
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
        msg1 = msg.split(':::')
        tag = msg1[0]
        msg1.remove(msg1[0])
        if tag == 'FullState':
            plrs = msg1[0].split('|')
            Player.instances = []
            for num, i in enumerate(plrs):
                exec(f"plr{num} = Player('{i}', pygame.Rect(len(Player.instances)*100,0, 100, 120))")
                if i.split("-")[-1] == ConMenu.conID.get():
                    LocalPlayer = plrID(ConMenu.conID.get())
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
            game.deck = set(apList)
            apList = []
            for i in gLsts.split('|')[1].split('/'):
                if i:
                    try:
                        apList.append(getCard(i))
                    except:
                        print('Error when decoding gLsts2 ' + i)
            game.discarded = set(apList)
            for ii in plrLsts.split('~'):
                plr = plrID(ii.split('>')[0])
                apList = []
                for i in ii.split('>')[1].split('/'):
                    try:
                        apList.append(getCard(i))
                    except:
                        print(f'Error when decoding plrLsts {ii} > {i}')
                plr.cards = apList
        elif tag == 'plrsInit':
            msg1 = msg1[0].split('>')
            if ConMenu.conID.get() == msg1[0]:
                if Player.instances[0].name == 'Null':
                    exec(
                        f"plr1 = Player('{ConMenu.conNAME.get()}-{ConMenu.conID.get()}', pygame.Rect((len(Player.instances)-1) * 100, 0, 100, 120))")
                    Player.instances[0] = Player.instances[1]
                    Player.instances.pop()
                exec(
                    f"plr{len(Player.instances) + 1} = Player('{msg1[1]}', pygame.Rect((len(Player.instances))*100,0, 100, 120))")
                if msg1[1].split("-")[-1] == ConMenu.conID.get():
                    dprint('ERROR, A player with this tag already exists')
                LocalPlayer = plrID(ConMenu.conID.get())
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


def sendSync(type):
    if type == 'full':
        gsend(f'gmDecode("{gmEncode("full")}")')


def reqSync(type):
    if type == 'players':
        gsend(f'sendPlr({ConMenu.conID.get()})')
        pass


def lockID(value=True):
    tdict = {
        False: 'enabled',
        True: 'disabled'
    }
    ConMenu.conID['state'] = tdict[value]


def sendPlr(target):
    gsend(f'gmDecode("plrsInit:::{target}>{ConMenu.conNAME.get()}-{ConMenu.conID.get()}")')


def Decode(msg):
    global LocalPlayer
    try:
        tag = msg.split('>>>')[0]
        msg = msg.split('>>>')[1]
        if tag == "PLRSinit":
            Player.instances = []
            plrs = msg.split("|")
            for num, i in enumerate(plrs):
                exec(f"plr{num} = Player('{i}', pygame.Rect(len(Player.instances)*100,0, 100, 120))")
                if i.split("-")[-1] == ConMenu.conID.get():
                    LocalPlayer = plrID(ConMenu.conID.get())
        if tag == "GameStateSET":
            for line in msg.split("|||"):
                print(f"line > {line}")
                print(f"split - {line.split('>>')}")
                t = line.split(">>")[0]
                items = ''.join([str(it) for it in line.split(">>")[1:]])
                # items = line.split(">>")[1:]
                print(f"t-{t}, items-{items}")
                newlist = []
                for i in items.split(','):
                    print(f'i - {i}')
                    newlist.append(strcls(f'card_{i}'))
                if t == 'game.onTable': game.onTable = newlist
        if tag == "GameStateADD":
            for line in msg.split("|||"):
                t = line.split(">>")[0]
                items = ''.join([str(it) for it in line.split(">>")[1:]])
                for i in items.split(','):
                    if t == 'game.onTable': game.onTable.append(strcls(f'card_{i}'))
    except Exception as e:
        print(f"Msg decode error > {e}")
        dprint(f"Msg decode error > {e}")


rootDir = os.getcwd()
filesInvalid = False
url = serverUrl + 'pyLib/cards/'
if not os.path.isdir('.cardAssets'): os.mkdir('.cardAssets')
os.chdir('.cardAssets')
print('Updating asset list')
try:
    r = requests.get((url + 'AssetList.txt'), allow_redirects=True)
    open(f'AssetList.txt', 'wb').write(r.content)
except:
    print('error getting asset list')
    dprint('error getting asset list')
    open(f'AssetList.txt', 'wb').write('\n').flush().close()
with open('AssetList.txt', 'r') as assetList:
    fileList = assetList.readlines()
    for i in fileList:
        if not os.path.isfile(i[:-1]):
            print(f'requesting {i[:-1]} from ' + url + f'{i[:-1]}')
            r = requests.get((url + f'{i[:-1]}'), allow_redirects=True)
            open(f'{i[:-1]}', 'wb').write(r.content)
os.chdir(rootDir)

cardSize = (88, 124)
# loading cards
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
cardHL = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'CardHighlight.png')).convert_alpha(),
                                cardSize)
cardBack = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'cardBack.png')).convert_alpha(),
                                cardSize)
beatenButImg = pygame.transform.scale(pygame.image.load(os.path.join('.cardAssets', 'beatenButton.png')).convert_alpha(),
                                cardSize)
tahoma = pygame.font.Font(r'.cardAssets\tahoma.ttf', 17)
bombard = pygame.font.Font(r'.cardAssets\bombard.ttf', 20)
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


def draw_text(text, surface, x, y, font=None, color=(255, 255, 255)):
    global tahoma
    if font is None: font = tahoma
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

x,y = uiRightbar.x, uiRightbar.y
deckX, deckY = (x + (uiRightbar.width/2))-(cardSize[1]/2), y+100
beatenB = pygame.Rect(deckX, deckY+350, cardSize[0], cardSize[1])

def winUpd():
    global LocalPlayer
    draw_background()
    reloadAv()

    for i in Card.instances:
        if (i in LocalPlayer.cards) or (i in game.onTable):
            if i in game.onTable:
                i.rect.x = tblX + ((tblMargin + cardSize[0]) * i.tableCoords[0])
                i.rect.y = tblY + ((tblMargin + cardSize[1]) * i.tableCoords[1])

            if i in LocalPlayer.cards:
                i.rect.x = handX + (tblMargin / 2 + cardSize[0]) * (
                        list(LocalPlayer.cards).index(i) - (10 * (list(LocalPlayer.cards).index(i) // 10)))
                i.rect.y = handY + cardSize[1] * (list(LocalPlayer.cards).index(i) // 10)

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
            root.blit(dudeMove, (i.rect.x, i.rect.y))
            draw_text('ACT', root, (i.rect.x + 38), i.rect.y + 2, bombard, (20,20,20))

    x,y = uiRightbar.x, uiRightbar.y
    deckX, deckY = (x + (uiRightbar.width/2))-(cardSize[1]/2), y+100
    if game.trump:
        trumpcard = getCard(game.trump)
        root.blit(trumpcard.img, (deckX, deckY-(cardSize[1]/2)+10))
    root.blit(cardBack, (deckX, deckY))
    draw_text(f'{len(game.deck)}', root, deckX+(cardSize[0]/2)-(len(f'{len(game.deck)}')*6), deckY+15, pygame.font.Font(r'.cardAssets\bombard.ttf', 25), hexc('00EEEE'))
    root.blit(beatenButImg, (beatenB.x, beatenB.y))
    draw_text(f'{len(game.discarded)}', root, deckX + (cardSize[0] / 2) - (len(f'{len(game.deck)}') * 6), deckY + 365,
              pygame.font.Font(r'.cardAssets\bombard.ttf', 25), hexc('ff4336'))

    for i in ContextMenu.instances:
        if i.active: i.draw()

    pygame.display.update()


def draw_init():
    root.fill((64, 64, 64))
    pygame.display.update()


global selectedCard
selectedCard = None


def select(card):
    global selectedCard
    print(card.name + 'selected')
    if not selectedCard and LocalPlayer is game.mover:
        selectedCard = card
        card.HL = True
    elif card == selectedCard:
        selectedCard = None
        card.HL = False


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
        funcs = ['LifeCheck()', 'TgDebug']
        if f not in funcs:
            dexec(f)
        else:
            if f == funcs[0]:
                LifeCheck()
            elif f == funcs[1]:
                ConMenu.debugMode.set((not self.debug))
                self.debug = not self.debug

    def hide(self):
        self.active = False


buttons = [
    cmButton('Test', 'LifeCheck()'),
    cmButton('Toggle debug', 'TgDebug')
]
dButs = [
    cmButton('Debug Is On', 'dprint("Yes, it is on!")')
]
menu = ContextMenu(buttons, dButs)

def hexc(st):
    if st[0] == '#': list(st).pop(0).join()
    st = st.lower()
    if len(st) == 1: st = st * 6
    if len(st) == 3: st = st * 3
    s1 = int((st[0] + st[1]), 16)
    s2 = int((st[2] + st[3]), 16)
    s3 = int((st[4] + st[5]), 16)
    return (s1,s2,s3)

def test():
    gmDecode(
        'FullState:::Arai-1|B-2|Я-3:::s10|1:::c7/c6/h7/s7/d6/d7/h6/s6|s13>>>1>s11/s10/c11/h10/s9/c10/d11/d9/d10/h11~2>s8/h9/d8/h8/c8/c9')


def main():
    lmbhandling = False
    rmbhandling = False
    global RUN
    clock = pygame.time.Clock()
    draw_init()
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
            if menu.active:
                for i in menu.buttons:
                    if i.rect.collidepoint(pos):
                        menu.run(i.func)
                        continue
                if menu.debug:
                    for i in menu.dButs:
                        if i.rect.collidepoint(pos):
                            menu.run(i.func)
                            continue
            for i in Card.instances:
                if i.rect.collidepoint(pos):
                    select(i)
                    continue

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            lmbhandling = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not rmbhandling:
            rmbhandling = True
            if menu.active:
                menu.hide()
            else:
                menu.set(pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            rmbhandling = False

        winUpd()
    # except Exception as e:
    #    print(f'ERROR >> {e}')
    #    try:
    #        send(f'Player {plrID(LocalPlayer)} > {e}')
    #    except: pass

    pygame.quit()


main()
exit()

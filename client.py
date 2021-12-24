server = "http://152.67.77.130:8080"

import requests
try:
    requests.get(server)
except requests.exceptions.ConnectionError:
    input("Couldn't connect to server. Press Enetr to continue")
    exit()

import secrets
SECRET = secrets.token_hex(16)

mode = input("Eneter \'c\' to create a session, or \'j\' to join an existing one: ").strip()
if mode == "c":
    id = input("Enter your session name: ").strip()
    s = int(input("Enter the size of the game: ").strip())
    p = requests.post(server + "/create_session", data = {'session_id':id, 'size':s, 'p1s':SECRET})
    if p.status_code != 200:
        input(str(p.status_code) + ": " + p.reason + "\nPress enetr to continue")
        exit()
    playern = 1
elif mode == "j":
    id = input("Enter your session name: ").strip()
    p = requests.post(server + "/join_session", data = {'session_id':id, 'p2s':SECRET})
    if p.status_code != 200:
        input(str(p.status_code) + ": " + p.reason + "\nPress enetr to continue")
        exit()
    s = len(requests.get(server + "/" + id).text.splitlines())
    playern = 2
else:
    exit()

import pygame
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))


screen = pygame.display.set_mode((720, 720))
pygame.display._set_autoresize(False)
clock = pygame.time.Clock()
FPS = 15  # Frames per second.

pygame.display.set_caption("Virus Wars")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
P1T = RED
P2T = GREEN
P1CT = (255//2, 0, 0)
P2CT = (0, 255//2, 0)

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.SysFont(None, 32)

import VirusGame as vg

class Grid:
    def __init__(self, w, h):
        self.game = vg.Game(w, h)
        s = self.game.getString()
        # self.arr = [[0].copy()*w].copy()*h
        self.arr = []
        t = []
        for i in range(w):
            t.append(0)
        for i in range(h):
            self.arr.append(t.copy())
        # print(s)
        self.width = w
        self.height = h
        self.updateArr()
        # print(self.arr)

        self.c = 0
        self.cc = 3

    def updateArr(self):
        # for cell in self.game.p1:
        #     self.arr[cell[0]][cell[1]] = 1
        # for cell in self.game.p2:
        #     self.arr[cell[0]][cell[1]] = 2
        # for cell in self.game.p1c:
        #     self.arr[cell[0]][cell[1]] = 3
        # for cell in self.game.p2c:
        #     self.arr[cell[0]][cell[1]] = 4
        try:
            p = requests.get(server + "/" + id)
        except requests.exceptions.ConnectionError:
            input("Couldn\'t connect to server. Press Enetr to continue")
            exit()
        if p.status_code != 200:
            input(str(p.status_code) + ": " + p.reason + "\nPress enetr to continue")
            exit()
        gamestr = p.text
        gamearr = gamestr.splitlines()
        i = 0
        for row in gamearr:
            j = 0
            for c in row:
                if c == 'X':
                    self.arr[i][j] = 1
                if c == 'O':
                    self.arr[i][j] = 2
                if c == 'C':
                    self.arr[i][j] = 3
                if c == 'P':
                    self.arr[i][j] = 4
                j += 1
            i += 1

    def drawGrid(self):
        self.updateArr()
        w, h = pygame.display.get_surface().get_size()
        bsx = w//self.width
        bsy = h//self.height
        for x in range(w // bsx):
            for y in range(h // bsy):
                rect = pygame.Rect(x*bsx, y*bsy, bsx, bsy)
                pygame.draw.rect(screen, WHITE, rect, 1)
        for y in range(self.height):
            for x in range(self.width):
                if self.arr[y][x] == 1:
                    rect = pygame.Rect(x*bsx, y*bsy, bsx, bsy)
                    pygame.draw.rect(screen, P1T, rect)
                if self.arr[y][x] == 2:
                    rect = pygame.Rect(x*bsx, y*bsy, bsx, bsy)
                    pygame.draw.rect(screen, P2T, rect)
                if self.arr[y][x] == 3:
                    rect = pygame.Rect(x*bsx, y*bsy, bsx, bsy)
                    pygame.draw.rect(screen, P1CT, rect)
                if self.arr[y][x] == 4:
                    rect = pygame.Rect(x*bsx, y*bsy, bsx, bsy)
                    pygame.draw.rect(screen, P2CT, rect)
    
    def handleClick(self, x, y):
        w, h = pygame.display.get_surface().get_size()
        bsx = w//self.width
        bsy = h//self.height
        gy = x // bsx
        gx = y // bsy
        # print(self.c, ":", gx, gy)
        try:
            p = requests.post(server + "/" + id + "/move", data={'player':playern, 'secret':SECRET, 'movex':gx, 'movey':gy})
        except requests.exceptions.ConnectionError:
            input("Couldn't connect to server. Press Enetr to continue")
            exit()
        if p.status_code != 200:
            print(str(p.status_code) + ": " + p.reason)

grid = Grid(s, s)

while True:
    clock.tick(FPS)
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         p = requests.post(server + "/" + id + "/del", data={'player':playern, 'secret':SECRET})
    #         quit()
    try:
        p = requests.get(server + "/" + id)
    except requests.exceptions.ConnectionError:
        input("Couldn\'t connect to server. Press Enetr to continue")
        exit()
    if p.text.isnumeric():
        pl = p.text
        # create a text surface object,
        # on which text is drawn on it.
        text = font.render("Player " + pl + " won. Congratulations!", True, GREEN, BLUE)
        
        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        
        # set the center of the rectangular object.
        textRect.center = (pygame.display.get_surface().get_size()[0] // 2, pygame.display.get_surface().get_size()[1] // 2)

        # completely fill the surface object
        # with white color
        pygame.display.get_surface().fill(BLACK)
    
        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        pygame.display.get_surface().blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                p = requests.post(server + "/" + id + "/del", data={'player':playern, 'secret':SECRET})
                quit()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                p = requests.post(server + "/" + id + "/del", data={'player':playern, 'secret':SECRET})
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Click!")
                pos = pygame.mouse.get_pos()
                # print(" ", pos)
                if not(pos[0] < 0 or pos[0] > pygame.display.get_surface().get_size()[0] or pos[1] < 0 or pos[1] > pygame.display.get_surface().get_size()[1]):
                    # print("  We\'re fine")
                    grid.handleClick(pos[0], pos[1])

        screen.fill(BLACK)
        grid.drawGrid()
    pygame.display.update()  # Or pygame.display.flip()

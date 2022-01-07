import sys
import pygame
import pygame_menu
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

def open_link(*args) -> None:
    link: 'pygame_menu.widgets.MenuLink' = args[-1]
    link.open()

main = pygame_menu.Menu("VirusGame", 720, 720, theme=pygame_menu.themes.THEME_BLUE)
lc = pygame_menu.Menu("Local", 720, 720, theme=pygame_menu.themes.THEME_BLUE)
mp = pygame_menu.Menu("Multiplayer", 720, 720, theme=pygame_menu.themes.THEME_BLUE)
mpc = pygame_menu.Menu("Create", 720, 720, theme=pygame_menu.themes.THEME_BLUE)
mpj = pygame_menu.Menu("Join", 720, 720, theme=pygame_menu.themes.THEME_BLUE)
mpo = pygame_menu.Menu("Spectate", 720, 720, theme=pygame_menu.themes.THEME_BLUE)

# main
main.add.button('Multiplayer', mp)
main.add.button('Local', lc)
main.add.button('Quit', pygame_menu.events.EXIT)

# mp
mp.add.button('Create', mpc)
mp.add.button('Join', mpj)
mp.add.button('Spectate', mpo)
mp.add.button('Back', pygame_menu.events.BACK)

#mpc
c_session_widget = mpc.add.text_input('Session name: ')
mpc_size_widget = mpc.add.text_input('Size: ', default='10', input_type=pygame_menu.locals.INPUT_INT)

def c_run_client():
    from client import clnt
    id = c_session_widget.get_value()
    s = int(mpc_size_widget.get_value())
    if s > 1:
        clnt('c', id, s)

mpc.add.button('Start', c_run_client)
mpc.add.button('Back', pygame_menu.events.BACK)

#mpj
j_session_widget = mpj.add.text_input('Session name: ')

def j_run_client():
    from client import clnt
    id = j_session_widget.get_value()
    clnt('j', id, -1)

mpj.add.button('Start', j_run_client)
mpj.add.button('Back', pygame_menu.events.BACK)

#mpo
o_session_widget = mpo.add.text_input('Session name: ')

def o_run_client():
    from client import clnt
    id = o_session_widget.get_value()
    clnt('o', id, -1)

mpo.add.button('Start', o_run_client)
mpo.add.button('Back', pygame_menu.events.BACK)

# lc
size_widget = lc.add.text_input('Size: ', default='10', input_type=pygame_menu.locals.INPUT_INT)

def run_local():
    from gui import local
    s = int(size_widget.get_value())
    if s > 1:
        local(s)

lc.add.button('Start', run_local)
lc.add.button('Back', pygame_menu.events.BACK)

while True:

    screen.fill(BLACK)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if main.is_enabled():
        main.update(events)
        main.draw(pygame.display.get_surface())

    pygame.display.update()

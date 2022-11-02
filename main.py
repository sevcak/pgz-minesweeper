import pgzrun

# screen dimensions
WIDTH = 640
HEIGHT = 360
TITLE = 'Minesweeper'

policka = list()
for i in range(9):
    for j in range(20):
        policko = Actor('tile', topleft=(10 + j * 31, 71 + i * 31))
        policko.riadok = i
        policko.stlpec = j
        policka.append(policko)


def draw():
    # background fill
    screen.blit('bg', (0, 0))

    # renders tiles
    for policko in policka:
        policko.draw()


def update():
    pass


# osetruje klik mysou
def on_mouse_down(pos):
    # osetruje klik na policko
    collrect = Actor('empty', topleft=pos)
    index = collrect.collidelist(policka)
    kliknute_policko = policka[index]
    print('\nStlacene policko:\n'
          f'index: {index}\n'
          f'riadok: {kliknute_policko.riadok}\n'
          f'stlpec: {kliknute_policko.stlpec}\n')


pgzrun.go()

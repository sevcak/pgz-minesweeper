import pgzrun
import random

# screen dimensions
WIDTH = 640
HEIGHT = 360
TITLE = 'Minesweeper'

policka = list()
first_click = True
hra = True

button_mode = Actor('button-mode-uncover', (WIDTH - 160, 72 / 2))
button_restart = Actor('button-restart', (WIDTH - 100, 72 / 2))
button_save = Actor('button-save', (WIDTH - 40, 72 / 2))

button_mode.uncover = True

# vytvorenie policok
for i in range(9):
    for j in range(20):
        # vytvorenie jedneho policka
        policko = Actor('tile', topleft=(10 + j * 31, 71 + i * 31))
        # vlastnosti riadok a stlpec sluzia na identifikaciu pozicie policka
        policko.riadok = i
        policko.stlpec = j
        policko.bomb = False
        policko.flagged = False
        policko.uncovered = False
        policko.mines_near = None

        policka.append(policko)


def draw():
    # background fill
    screen.blit('bg', (0, 0))

    # renders tiles
    for policko in policka:
        policko.draw()

    button_mode.draw()
    button_restart.draw()
    button_save.draw()


def update():
    pass


# osetruje klik mysou
def on_mouse_down(pos):
    global first_click
    global hra

    if hra == True:
        # osetruje klik na policko
        collrect = Actor('empty', topleft=pos)
        index = collrect.collidelist(policka)
        if index >= 0:
            kliknute_policko = policka[index]
            print('\nStlacene policko:\n'
                  f'index: {index}\n'
                  f'riadok: {kliknute_policko.riadok}\n'
                  f'stlpec: {kliknute_policko.stlpec}\n')

        # rozdeluje program na rezim odkryvania policok a na rezim pokladania vlajek
        if button_mode.image == 'button-mode-uncover' and index >= 0 and policka[
                index].flagged == False:
            # rozlozenie min po prvom kliknuti
            if first_click == True:
                first_click = False

                for i in range(30):
                    placed_bomb = False

                    while placed_bomb == False:
                        num = random.randint(0, 179)
                        if num != index and policka[num].bomb == False:
                            placed_bomb = True

                            policka[num].bomb = True
                            # nastavi texturu bomby pre testovacie ucely (neskor odstranit/zakomentovat)
                            # policka[num].image = "tile-bomb"
                print('Miny boli rozlozene.')

                # zmapovanie min v okoli kazdeho policka, na ktorom nie je mina
                for i in range(len(policka)):
                    if policka[i].bomb == False:
                        policka[i].mines_near = get_mines_in_proximity(
                            policka, i)
                        # nastavi pocet min v okoli ako texturu pre testovacie ucely (neskor odstranit/zakomentovat)
                        # policka[i].image = f'tile-{policka[i].mines_near}'

            # overovanie policka, ci bola stlacena mina
            if policka[index].bomb == True:
                hra = False
                for i in range(180):
                    if policka[i].bomb == True and policka[i] != index:
                        policka[i].image = 'tile-bomb'
                    else:
                        policka[index].image = 'tile-bomb-red'

            if policka[index].bomb == False:
                policka[index].image = f'tile-{policka[index].mines_near}'
                policka[index].uncovered = True
                if policka[index].mines_near == 0:
                    uncover_recursive(index)

        # pokladanie a rusenie vlajok
        elif button_mode.uncover == False:
            if policka[index].flagged == False and index >= 0 and policka[
                    index].uncovered == False:
                policka[index].image = 'tile-flagged'
                policka[index].flagged = True
                # policka[index].uncovered = True
            elif policka[index].flagged == True and index >= 0:
                policka[index].image = 'tile'
                policka[index].flagged = False

        # menenie modu flags a uncover
        if button_mode.collidepoint(pos):
            if button_mode.uncover == True:
                button_mode.uncover = False
                button_mode.image = 'button-mode-flag'
            else:
                button_mode.uncover = True
                button_mode.image = 'button-mode-uncover'

    else:
        print('Neprebieha hra')
    # restart
    if button_restart.collidepoint(pos):
        print('restart')
        start_position()


# funkcia startovacej pozicie
def start_position():
    global first_click
    global hra

    for policko in policka:

        policko.bomb = False
        policko.flagged = False
        policko.uncovered = False
        policko.image = 'tile'
    button_mode.image = 'button-mode-uncover'
    button_mode.uncover = True
    first_click = True
    hra = True


# funkcia, ktora zisti pocet min v okoli policka
def get_mines_in_proximity(policka, index):
    '''
    Funkcia, ktora dostane ako parametre cele pole a index jedneho policko z neho,
    na zaklade nich vrati pocet min v okoli tohto policka.
    '''
    pocet_min = 0

    policko = policka[index]

    # urcenie policok, ktore sa budu prehladavat
    okolie = []
    # lava strana
    if policko.stlpec > 0:
        # lavy stred
        okolie.append(policka[index - 1])

        if policko.riadok > 0:
            # lavy horny roh
            okolie.append(policka[index - 1 - 20])
        if policko.riadok < 8:
            # lavy dolny roh
            okolie.append(policka[index - 1 + 20])
    # prava strana
    if policko.stlpec < 19:
        # pravy stred
        okolie.append(policka[index + 1])

        if policko.riadok > 0:
            # pravy horny roh
            okolie.append(policka[index + 1 - 20])
        if policko.riadok < 8:
            # pravy dolny roh
            okolie.append(policka[index + 1 + 20])
    # horny stred
    if policko.riadok > 0:
        okolie.append(policka[index - 20])
    # dolny stred
    if policko.riadok < 8:
        okolie.append(policka[index + 20])

    # zistenie, kolko min je na okolytych polickach
    for policko_okolia in okolie:
        if policko_okolia.bomb:
            pocet_min += 1

    return pocet_min


def uncover_recursive(index):
    '''
    Funkcia, ktora dostane ako parametre index jedneho policka so ziadnou minou v okoli,
    odkryje policka v jeho blizkosti,
    zisti, ci sa v jeho blizkosti nachadza neodkryte policko so ziadnou minou v okoli,
    a podla toho pre kazde taketo policko rekurzivne vola samu seba
    a index tohto policka prebera ako novy parameter.
    '''

    policko = policka[index]

    # urcenie policok, ktore sa budu prehladavat
    okolie = []
    # lava strana
    if policko.stlpec > 0:
        # lavy stred
        okolie.append(policka[index - 1])

        if policko.riadok > 0:
            # lavy horny roh
            okolie.append(policka[index - 1 - 20])
        if policko.riadok < 8:
            # lavy dolny roh
            okolie.append(policka[index - 1 + 20])
    # prava strana
    if policko.stlpec < 19:
        # pravy stred
        okolie.append(policka[index + 1])

        if policko.riadok > 0:
            # pravy horny roh
            okolie.append(policka[index + 1 - 20])
        if policko.riadok < 8:
            # pravy dolny roh
            okolie.append(policka[index + 1 + 20])
    # horny stred
    if policko.riadok > 0:
        okolie.append(policka[index - 20])
    # dolny stred
    if policko.riadok < 8:
        okolie.append(policka[index + 20])

    # mapovanie policok v okoli
    for policko_okolia in okolie:
        index = (policko_okolia.riadok * 20 + policko_okolia.stlpec)

        # kontrola ci je policko uz odkryte, zmena obrazku policka
        if policka[index].uncovered == False:
            policka[index].uncovered = True
            policka[index].image = f'tile-{policka[index].mines_near}'
            print(f'{index}')
            # ak policko okolo seba nema ziadnu bombu
            # znovu sa spusti funkcia uncover_recursive(index)
            if policka[index].mines_near == 0:
                uncover_recursive(index)


pgzrun.go()

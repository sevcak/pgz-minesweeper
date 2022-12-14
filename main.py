import pgzrun
import random
import json

# screen dimensions
WIDTH = 640
HEIGHT = 360
TITLE = 'Minesweeper'

policka = list()
first_click = True
hra = True

button_mode = Actor('button-mode-uncover', (WIDTH - 220, 72 / 2))
button_restart = Actor('button-restart', (WIDTH - 160, 72 / 2))
button_load = Actor('button-load', (WIDTH - 100, 72 / 2))
button_save = Actor('button-save', (WIDTH - 40, 72 / 2))

button_mode.uncover = True

game_status = Actor('button-smiley-happy', (WIDTH / 2, 72 / 2))

game_status.win = False

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
    button_load.draw()
    button_save.draw()
    game_status.draw()


def update():
    #kontroluje ci su vsetky miny 'zavlajkovane' a vsetky ostatne policka odkryte ak ano vyhral si
    global hra
    if hra:
        vyhra = True

        for policko in policka:
            if policko.uncovered == False and policko.bomb == False:
                vyhra = False
        if vyhra:
            print("Vyhral si!")
            reset_save()
            game_status.win = True
            game_status.image = 'button-win'
            hra = False
            vyhra = False


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
                game_status.image = 'button-smiley-dead'
                for i in range(180):
                    if policka[i].bomb == True and policka[i] != index:
                        policka[i].image = 'tile-bomb'
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

        if button_save.collidepoint(pos):
            save()

    else:
        print('Neprebieha hra')
    # restart
    if button_restart.collidepoint(pos):
        start_position()
        reset_save()

    if button_load.collidepoint(pos):
        load()


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
    game_status.win = False
    game_status.image = 'button-smiley-happy'
    print('restart')


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
            # ak policko okolo seba nema ziadnu bombu
            # znovu sa spusti funkcia uncover_recursive(index)
            if policka[index].mines_near == 0:
                uncover_recursive(index)


def save():
    global first_click

    policka_dict = {'policka': []}
    policka_dict['first_click'] = first_click

    for policko in policka:
        policko_dict = {}
        policko_dict['riadok'] = policko.riadok
        policko_dict['stlpec'] = policko.stlpec
        policko_dict['bomb'] = policko.bomb
        # policko_dict['index'] = policko.index
        policko_dict['mines_near'] = policko.mines_near
        policko_dict['flagged'] = policko.flagged
        policko_dict['uncovered'] = policko.uncovered

        policka_dict['policka'].append(policko_dict)

    # zapis do save suboru
    with open('savefile.json', 'w') as subor:
        subor.write(json.dumps(policka_dict, indent=4))

    print('hra bola ulozena')


def reset_save():
    policka_dict = {'policka': []}
    policka_dict['first_click'] = True

    for policko in policka:
        policko_dict = {}
        policko_dict['bomb'] = policko.bomb = False
        policko_dict['mines_near'] = policko.mines_near = None
        policko_dict['flagged'] = policko.flagged = False
        policko_dict['uncovered'] = policko.uncovered = False

        policka_dict['policka'].append(policko_dict)

    with open('savefile.json', 'w') as subor:
        subor.write(json.dumps(policka_dict, indent=4))


def load():
    global hra
    global first_click

    hra = True
    with open('savefile.json', 'r') as subor:
        load = json.load(subor)
        policka_dict = load['policka']
        first_click = load['first_click']

        for i in range(len(policka_dict)):
            policka[i].bomb = policka_dict[i]['bomb']
            policka[i].uncovered = policka_dict[i]['uncovered']
            policka[i].flagged = policka_dict[i]['flagged']
            policka[i].mines_near = policka_dict[i]['mines_near']

            if policka[i].flagged:
                policka[i].image = 'tile-flagged'
            elif policka[i].uncovered == False:
                policka[i].image = 'tile'
            elif policka[i].mines_near != None:
                policka[i].image = f'tile-{policka[i].mines_near}'

    game_status.win = False
    game_status.image = 'button-smiley-happy'
    print('ulozena hra sa nacitala')


pgzrun.go()

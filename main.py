import pgzrun
import random

# screen dimensions
WIDTH = 640
HEIGHT = 360
TITLE = 'Minesweeper'

policka = list()
first_click = True
hra = True

# vytvorenie policok
for i in range(9):
    for j in range(20):
        # vytvorenie jedneho policka
        policko = Actor('tile', topleft=(10 + j * 31, 71 + i * 31))
        # vlastnosti riadok a stlpec sluzia na identifikaciu pozicie policka
        policko.riadok = i
        policko.stlpec = j
        policko.bomb = False

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
    global first_click
    global hra
    
    if hra == True:
        # osetruje klik na policko
        collrect = Actor('empty', topleft=pos)
        index = collrect.collidelist(policka)
        kliknute_policko = policka[index]
        print('\nStlacene policko:\n'
              f'index: {index}\n'
              f'riadok: {kliknute_policko.riadok}\n'
              f'stlpec: {kliknute_policko.stlpec}\n')
    
        # rozlozenie min po prvom kliknuti
        if first_click == True:
            first_click = False
    
            for i in range(40):
                placed_bomb = False
    
                while placed_bomb == False:
                    num = random.randint(0, 179)
                    if num != index and policka[num].bomb == False:
                        placed_bomb = True
    
                        policka[num].bomb = True
                        # nastavi texturu bomby pre testovacie ucely (neskor odstranit)
                        #policka[num].image = "tile-bomb"
            print('Miny boli rozlozene.')
    
        else:
          #overovanie policka, ci bola stlacena mina
          if policka[index].bomb == True:
            hra = False
            for i in range(180):
                if policka[i].bomb == True and policka[i] != index:
                   policka[i].image = "tile-bomb" 
                else:
                    policka[index].image = "tile-bomb-red"
                
          else:
            if policka[index].bomb == False:
              policka[index].image = "tile-one"  
    else:
        print('Neprebieha hra')
pgzrun.go()

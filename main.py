import pgzrun
import random

# screen dimensions
WIDTH = 640
HEIGHT = 360
TITLE = 'Minesweeper'

policka = list()


# vytvorenie policok
for i in range(9):
    for j in range(20):
        # vytvorenie jedneho policka
        policko = Actor('tile', topleft=(10 + j * 31, 71 + i * 31))
        # vlastnosti riadok a stlpec sluzia na identifikaciu pozicie policka
        policko.riadok = i
        policko.stlpec = j

        policka.append(policko)
#test111

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
  
  # zobrazenie mín po kliknuti
  #zobrazia sa kvôli testu potom spolu s cislami ich treba schovat
  
    
    for i in range (40):
      num = random.randint(0, 179)
      if num != index and policka[num].image != "tile-bomb":
        policka[num].image = "tile-bomb" 
      else:
        num = random.randint(0, 179)
        if policka[num].image != "tile-bomb":
          policka[num].image = "tile-bomb"
        else:
          num = random.randint(0, 179)
          if policka[num].image != "tile-bomb":
            policka[num].image = "tile-bomb"
              
pgzrun.go()

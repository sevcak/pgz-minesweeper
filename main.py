import pgzrun

# screen dimensions
WIDTH = 640
HEIGHT = 360
TITLE = 'Minesweeper'

#TEST

policka = list()
for i in range(20):
  for j in range(9):
    policko = Actor('tile', topleft = (10 + i*31, 71 + j * 31))
    policka.append(policko)

def draw():
    # background fill
    screen.blit('bg', (0,0))
  
    for policko in policka:
      policko.draw()
    

def update():
    pass

pgzrun.go()

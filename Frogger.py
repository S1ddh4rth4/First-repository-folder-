import pygame
import time

# Inicialización de Pygame
pygame.init()

# Definiciones globales
pantallaw = 1000
pantallah = 1000

# Colores
fondo = (50, 50, 50)
white = (255, 255, 255)
marco = (100, 100, 200)
vereda = (40, 39, 39)
selva = (10, 150, 10)
agua = (100, 100, 230)

# Recursos
crocki_img = pygame.image.load('crockicrocki.png')
carr_img = pygame.image.load('carr.png')
carl_img = pygame.image.load('carl.png')
tortuga_img = pygame.image.load('tortugas.png')
arbol_img = pygame.image.load('arbol.png')

areajuego = pygame.display.set_mode((pantallaw, pantallah))
pygame.display.set_caption('Crocki Crocki!')

gametimer = pygame.time.Clock()


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y):
    large_text = pygame.font.Font('freesansbold.ttf', 40)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = (x, y)
    areajuego.blit(text_surf, text_rect)


def obj_colisiones(a, jposx, w):
    if jposx >= a and jposx <= a + w:
        return True
    elif jposx + 50 >= a and jposx + 50 <= a + w:
        return True
    return False


class Game:
    def __init__(self):
        self.jposx = 950
        self.jposy = 900
        self.puntaje = 0
        self.ciclos = 5000
        self.termino = False
        self.crockis = []

        self.auto_pos_y = [550, 600, 650, 700, 750, 800, 850]
        self.agua_pos_y = [100, 150, 200, 250, 300, 350, 400, 450]

        self.autos = [
            [100, 300],
            [200, 400],
            [300, 400],
            [100, 700],
            [600, 800],
            [100, 900],
            [500, 950]
        ]

        self.aguas = [
            [100, 350],
            [200, 500],
            [400, 950],
            [100, 400],
            [500, 750],
            [100, 900],
            [700, 850],
            [300, 600]
        ]

        self.velocidades = {
            "g1mx": 7,
            "g2mx": 4,
            "g3mx": -4
        }

    def detectar_colisiones(self):
        if self.jposy in self.auto_pos_y:
            idx = self.auto_pos_y.index(self.jposy)
            for a in self.autos[idx]:
                self.termino = obj_colisiones(a, self.jposx, 50)
                if self.termino:
                    break

        if self.jposy in self.agua_pos_y:
            idx = self.agua_pos_y.index(self.jposy)
            notenelagua = False
            for a in self.aguas[idx]:
                notenelagua = obj_colisiones(a, self.jposx, 150)
                if notenelagua:
                    break
            if notenelagua:
                velocidad = self.velocidades[f"g{idx % 3 + 1}mx"]
                self.jposx = self.jposx + velocidad
            else:
                self.termino = True

    def actualizar_posiciones(self):
        for i in range(len(self.autos)):
            for j in range(len(self.autos[i])):
                if self.autos[i][j] >= 990:
                    self.autos[i][j] = 0
                else:
                    self.autos[i][j] += self.velocidades[f"g{i % 3 + 1}mx"]

        for i in range(len(self.aguas)):
            for j in range(len(self.aguas[i])):
                if self.aguas[i][j] >= 990:
                    self.aguas[i][j] = -100
                else:
                    self.aguas[i][j] += self.velocidades[f"g{i % 3 + 1}mx"]

    def render(self):
        # Pintar fondo
        areajuego.fill(fondo)
        # Pintar marco y cosas fijas
        pygame.draw.rect(areajuego, marco, [0, 0, pantallaw, 50])
        pygame.draw.rect(areajuego, marco, [0, 950, pantallaw, 50])
        pygame.draw.rect(areajuego, vereda, [0, 500, pantallaw, 50])
        pygame.draw.rect(areajuego, vereda, [0, 900, pantallaw, 50])
        pygame.draw.rect(areajuego, selva, [0, 50, pantallaw, 50])
        pygame.draw.rect(areajuego, agua, [0, 100, pantallaw, 400])

        message_display(f"Ciclos restantes: {self.ciclos}", 300, 975)
        message_display(f"Puntaje de Crockis salvados: {self.puntaje}", 300, 25)

        for y, fila in zip(self.agua_pos_y, self.aguas):
            for x in fila:
                areajuego.blit(tortuga_img if y % 2 == 0 else arbol_img, (x, y))

        for y, fila in zip(self.auto_pos_y, self.autos):
            for x in fila:
                areajuego.blit(carr_img if y % 2 == 0 else carl_img, (x, y))

        areajuego.blit(crocki_img, (self.jposx, self.jposy))

        for a in self.crockis:
            areajuego.blit(crocki_img, (a, 50))

        pygame.display.update()

    def game_loop(self):
        while not self.termino:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.termino = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        self.termino = True
                    if event.key == pygame.K_LEFT:
                        self.jposx = max(0, self.jposx - 50)
                    if event.key == pygame.K_RIGHT:
                        self.jposx = min(950, self.jposx + 50)
                    if event.key == pygame.K_UP:
                        self.jposy = max(50, self.jposy - 50)
                    if event.key == pygame.K_DOWN:
                        self.jposy = min(900, self.jposy + 50)

            self.detectar_colisiones()

            if self.jposy == 50:
                self.puntaje += 20000
                self.jposy = 900
                self.crockis.append(self.jposx)

            self.actualizar_posiciones()
            self.render()

            self.gametimer.tick(60)
            self.ciclos -= 1
            if self.ciclos == 0:
                self.termino = True

        if self.puntaje == 0:
            self.ciclos = 0

        return self.ciclos + self.puntaje

def main():
    # Cuerpo del programa que llama al juego
    areajuego.fill(fondo)
    game = Game()
    score = game.game_loop()

    time.sleep(4)
    areajuego.fill(fondo)
    for a in range(5):
        message_display('Game Over', 500, 200)
        message_display(f'Tu score es: {score}', 500, 500)
        pygame.display.update()
        time.sleep(1)
    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Inicialização do Pygame
pygame.init()

# Definição das dimensões da janela
largura = 800
altura = 600

# Configuração do display do Pygame com OpenGL
pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)

# Definição das propriedades da câmera
posicao = [0, 0, 0]  # Posição inicial da câmera
rotacao = [0, 0]  # Rotação inicial da câmera

# Variáveis para controle do mouse
ultima_posicao_mouse = None
mouse_na_janela = False

# Lista de coordenadas das paredes
paredes = [
    # Paredes laterais
    ((-10, -1, -10), (-10, -1, 10)),
    ((10, -1, -10), (10, -1, 10)),
    # Paredes frontal e traseira
    ((-10, -1, -10), (10, -1, -10)),
    ((-10, -1, 10), (10, -1, 10)),
]

# Função para desenhar as paredes
def desenhar_paredes():
    for parede in paredes:
        glBegin(GL_QUADS)
        glColor3f(0.5, 0.5, 0.5)  # Cor cinza
        glVertex3fv(parede[0])
        glVertex3f(parede[0][0], parede[0][1] + 5, parede[0][2])
        glVertex3f(parede[1][0], parede[1][1] + 5, parede[1][2])
        glVertex3fv(parede[1])
        glEnd()

# Função para desenhar o chão quadriculado
def desenhar_chao():
    for i in range(-10, 10):
        for j in range(-10, 10):
            if (i + j) % 2 == 0:
                cor = (1, 1, 1)  # Quadrados brancos
            else:
                cor = (0, 0, 0)  # Quadrados pretos

            glBegin(GL_QUADS)
            glColor3fv(cor)
            glVertex3fv((i, -1, j))
            glVertex3fv((i + 1, -1, j))
            glVertex3fv((i + 1, -1, j + 1))
            glVertex3fv((i, -1, j + 1))
            glEnd()

# Função para atualizar a visão da câmera
def atualizar_camera():
    glLoadIdentity()
    glRotatef(rotacao[0], 1, 0, 0)
    glRotatef(rotacao[1], 0, 1, 0)
    glTranslatef(-posicao[0], -posicao[1], -posicao[2])

# Captura do movimento do mouse
def capturar_movimento_mouse():
    global rotacao, ultima_posicao_mouse

    posicao_mouse_atual = pygame.mouse.get_pos()

    if ultima_posicao_mouse is not None:
        if mouse_na_janela:
            delta_mouse = (
                posicao_mouse_atual[0] - ultima_posicao_mouse[0],
                posicao_mouse_atual[1] - ultima_posicao_mouse[1]
            )

            sensibilidade_mouse = 0.1
            rotacao[0] -= delta_mouse[1] * sensibilidade_mouse
            rotacao[1] -= delta_mouse[0] * sensibilidade_mouse

            if rotacao[0] > 90:
                rotacao[0] = 90
            elif rotacao[0] < -90:
                rotacao[0] = -90

    ultima_posicao_mouse = posicao_mouse_atual

# Posiciona o cursor do mouse no centro da tela
pygame.mouse.set_pos(largura // 2, altura // 2)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_na_janela = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_na_janela = False

    # Captura do movimento do mouse
    capturar_movimento_mouse()

    # Captura das teclas pressionadas para movimentação do personagem
    teclas = pygame.key.get_pressed()
    velocidade = 0.1
    proxima_posicao = posicao.copy()
    if teclas[pygame.K_w]:
        proxima_posicao[0] += velocidade * math.sin(rotacao[1] * math.pi / 180.0)
        proxima_posicao[2] -= velocidade * math.cos(rotacao[1] * math.pi / 180.0)
    if teclas[pygame.K_s]:
        proxima_posicao[0] -= velocidade * math.sin(rotacao[1] * math.pi / 180.0)
        proxima_posicao[2] += velocidade * math.cos(rotacao[1] * math.pi / 180.0)
    if teclas[pygame.K_a]:
        proxima_posicao[0] -= velocidade * math.cos(rotacao[1] * math.pi / 180.0)
        proxima_posicao[2] -= velocidade * math.sin(rotacao[1] * math.pi / 180.0)
    if teclas[pygame.K_d]:
        proxima_posicao[0] += velocidade * math.cos(rotacao[1] * math.pi / 180.0)
        proxima_posicao[2] += velocidade * math.sin(rotacao[1] * math.pi / 180.0)

    # Atualização da posição da câmera
    posicao = proxima_posicao

    # Configuração do OpenGL
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (largura / altura), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    atualizar_camera()

    # Desenho do ambiente
    desenhar_paredes()
    desenhar_chao()

    # Atualização do display
    pygame.display.flip()
    pygame.time.wait(10)

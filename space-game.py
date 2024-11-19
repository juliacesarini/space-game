import pygame
import random
pygame.init()

x = 1280
y = 720

janela = pygame.display.set_mode((x,y)) #determinando o tamanho de tela
pygame.display.set_caption('Simple Space') #determinando o nome do jogo

bg = pygame.image.load("bg.png").convert_alpha() #inserindo a imagem de fundo
bg = pygame.transform.scale(bg,(x, y))

#criação do "inimigo"
inimigo = pygame.image.load("inimigo.png").convert_alpha()
inimigo = pygame.transform.scale(inimigo, (80, 100))


#criação personagem principal
nave = pygame.image.load("nave.png").convert_alpha()
nave = pygame.transform.scale(nave, (130,130))
nave = pygame.transform.rotate(nave, -90)

#criação missil
missil = pygame.image.load("missil.png").convert_alpha()
missil = pygame.transform.scale(missil, (50,50))


#definindo a posição dos objetos

pos_inimigo_x = 1300
pos_inimigo_y = 360

pos_nave_x = 100
pos_nave_y = 300

vel_missil_x = 0
pos_missil_x = 140
pos_missil_y = 340

pontos = 1

tiro = False


janela_aberta = True #determinando que a janela fique aberta até que o usuário feche

fonte = pygame.font.SysFont('Arial', 25)

nave_rect = nave.get_rect() #definindo retângulos de colisão
inimigo_rect = inimigo.get_rect()
missil_rect = missil.get_rect()


#funções
def respawn():
    x = 1350
    y = random.randint(1,640)
    return[x,y]

def respawn_missil():
    tiro = False
    respawn_missil_y = pos_nave_y + 40
    respawn_missil_x = pos_nave_x + 40
    vel_missil_x = 0 
    return [respawn_missil_x, respawn_missil_y, tiro, vel_missil_x]

def colisoes():
    global pontos 
    if nave_rect.colliderect(inimigo_rect) or inimigo_rect == 60:
        pontos -= 1
        return True
    
    elif missil_rect.colliderect(inimigo_rect):
        pontos += 1
        return True
    
    else: 
        return False



while janela_aberta:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela_aberta = False

    janela.blit(bg, (0, 0))

    rel_x = x % bg.get_rect().width
    janela.blit(bg, (rel_x - bg.get_rect().width,0)) #cria bg
    if rel_x < 1280:
        janela.blit(bg, (rel_x, 0))

    #teclas de movimento
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_nave_y > 1:
        pos_nave_y -= 1

        if not tiro:
            pos_missil_y -= 1

    if tecla [pygame.K_DOWN] and pos_nave_y < 665:
        pos_nave_y += 1
        

        if not tiro:
            pos_missil_y += 1

    if tecla[pygame.K_SPACE]:
        tiro = True
        vel_missil_x = 2

    #definindo fim de jogo por pontos
    if pontos == -1:
        janela_aberta = False

    #respawn

    if pos_inimigo_x == 50:
        pos_inimigo_x = respawn()[0]
        pos_inimigo_y = respawn()[1]


    if pos_missil_x == 1300:
       pos_missil_x, pos_missil_y, tiro, vel_missil_x = respawn_missil()


    if pos_inimigo_x == 50 or colisoes():
        pos_inimigo_x = respawn()[0]
        pos_inimigo_y = respawn()[1]


    #posição rect

    nave_rect.y = pos_nave_y
    nave_rect.x = pos_nave_x

    missil_rect.y = pos_missil_y
    missil_rect.x = pos_missil_x

    inimigo_rect.y = pos_inimigo_y
    inimigo_rect.x = pos_inimigo_x


    #movimento
    x-=1
    pos_inimigo_x -=1

    pos_missil_x += vel_missil_x

    pygame.draw.rect(janela, (0, 0 , 0), nave_rect, 1)
    pygame.draw.rect(janela, (0, 0 , 0), missil_rect, 1)
    pygame.draw.rect(janela, (0, 0 , 0), inimigo_rect, 1)

    pontos_text = fonte.render(f' Score: {int(pontos)} ', True, (255, 255, 255))

    #criar as imagens
    janela.blit(pontos_text, (20,20))
    janela.blit(inimigo,(pos_inimigo_x, pos_inimigo_y))
    janela.blit(missil, (pos_missil_x, pos_missil_y))
    janela.blit(nave,(pos_nave_x, pos_nave_y))

    print(pontos)
    
    pygame.display.update()


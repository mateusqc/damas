# jogo de damas
# coding: utf-8

import time
import pygame
from pygame import gfxdraw

def desenha_tabuleiro(pecas):
	tam_quad = 70
	x, y = 0, 0
	for i in range (8):
		for j in range (8):
			if (i + j) % 2 == 0:
				cor = peru
			else:
				cor = wheat
			pygame.draw.rect(gameDisplay, cor, [x, y, tam_quad, tam_quad])
						
			if pecas[i][j] == 1:
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, black)
				pygame.gfxdraw.aacircle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, black)
			elif pecas[i][j] == 2:
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, white)
				pygame.gfxdraw.aacircle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, white)
			elif pecas[i][j] == 3:
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, black)
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 15, dimgray)
				pygame.gfxdraw.aacircle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, black)
			elif pecas[i][j] == 4:
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, white)
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 15, lightgray)
				pygame.gfxdraw.aacircle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, white)
				
			x += tam_quad
		y += tam_quad
		x = 0
	pygame.draw.rect(gameDisplay, burlywood, [560, 0, 800, 560])
	pygame.draw.rect(gameDisplay, saddlebrown, [560, 0, 5, 560])


def eh_peca(casa, pecas):
	return pecas[casa[0]][casa[1]]
	
def eh_diagonal(casa1, casa2):
	# função que verifica se a casa2 é diagonal com a casa1
	# 0 = nao é diagonal; 1 = diagonal direta; 2 = diagonal inversa
	
	if (casa1[0] + casa1[1]) == (casa2[0] + casa2[1]): # diagonais diretas
		return 2
	elif (casa1[0] + casa1[1]) == - 2 * (casa2[0] - casa1[0]) + (casa2[0] + casa2[1]): # diagonais inversas
		return 1
	else:
		return 0
		
def mov_dama_eh_livre(casa1, casa2, pecas, tipo_diag):
	# 0 = movimento obstruído; 1 = movimento possível; 2 = movimento de captura
	dist = (casa2[0] - casa1[0])
	tipo_peca = pecas[casa1[0]][casa1[1]]
	tipo_peca_captura = 0
	casa_captura = (-1, -1)
	obstruido = 0 # 1 = obstruido; 2 = captura.
	captura = False
	
	if dist < 0:
		sinal = -1
		dist *= -1
	else:
		sinal = 1
	
	print "Tipo de diagonal:", tipo_diag
	
	if tipo_diag == 1: # diagonal direta
		for n in range(1, dist):
			if pecas[casa1[0] + n * sinal][casa1[1] + n * sinal] != 0:
				if n == dist - 1 and obstruido == 0:
					tipo_peca_captura = pecas[casa1[0] + n * sinal][casa1[1] + n * sinal]
					casa_captura = (casa1[0] + n * sinal, casa1[1] + n * sinal)
					obstruido = 2
				else:
					obstruido = 1
					
	elif tipo_diag == 2: # diagonal inversa 
		for n in range(1, dist):
			if pecas[casa1[0] + n * sinal][casa1[1] - n * sinal] != 0:
				if n == dist - 1 and obstruido == 0:
					tipo_peca_captura = pecas[casa1[0] + n * sinal][casa1[1] - n * sinal]
					casa_captura = (casa1[0] + n * sinal, casa1[1] - n * sinal)
					obstruido = 2
				else:
					obstruido = 1
	
	print "Casa de captura:", casa_captura
	
	if tipo_peca == 3 and (tipo_peca_captura == 2 or tipo_peca_captura == 4):
		captura = True
	elif tipo_peca == 4 and (tipo_peca_captura == 1 or tipo_peca_captura == 3):
		captura = True
	
	if obstruido == 0:
		return (1, casa_captura)
	elif obstruido == 2 and captura:
		return (2, casa_captura)
	else:
		return (0, casa_captura)

def mover_peca(peca_selec, casa, pecas):
	# retorna se houve movimento
	tipo_peca = pecas[peca_selec[0]][peca_selec[1]]
	eh_possivel = False
	comeu = False
	houve_mov = False
	
	# as casas estão dispostas em coordenadas (Y, X)
	# adicionar damas e seus movimentos
	
	if tipo_peca == 1:
		if casa[0] - peca_selec[0] == 1 and ((casa[1] == peca_selec[1] + 1) or (casa[1] == peca_selec[1] - 1)):
			eh_possivel = True
		elif casa[0] - peca_selec[0] == 2 and ((casa[1] == peca_selec[1] + 2) or (casa[1] == peca_selec[1] - 2)):
			if casa[1] > peca_selec[1]:
				casa_p_comer = (casa[0] - 1, casa[1] - 1)
			else:
				casa_p_comer = (casa[0] - 1, casa[1] + 1)
			if pecas[casa_p_comer[0]][casa_p_comer[1]] == 2 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 4:
				eh_possivel = True
				comeu = True
				
	elif tipo_peca == 2:
		if casa[0] - peca_selec[0] == -1 and ((casa[1] == peca_selec[1] + 1) or (casa[1] == peca_selec[1] - 1)):
			eh_possivel = True
		elif casa[0] - peca_selec[0] == -2 and ((casa[1] == peca_selec[1] + 2) or (casa[1] == peca_selec[1] - 2)):
			if casa[1] > peca_selec[1]:
				casa_p_comer = (casa[0] + 1, casa[1] - 1)
			else:
				casa_p_comer = (casa[0] + 1, casa[1] + 1)
			if pecas[casa_p_comer[0]][casa_p_comer[1]] == 1 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 3:
				eh_possivel = True
				comeu = True
				
	elif tipo_peca == 3 or tipo_peca == 4: # como as damas se movimentam em todas as direções, ambas terão movimentos semelhantes
		# inicialmente, deve-se obter a direção em que o movimento está sendo realizado
		tipo_diag = eh_diagonal(peca_selec, casa)
		if tipo_diag:
			tipo_mov_dama, casa_p_comer = mov_dama_eh_livre(peca_selec, casa, pecas, tipo_diag)
			if tipo_mov_dama == 1:
				eh_possivel = True
			elif tipo_mov_dama == 2:
				eh_possivel = True
				comeu = True

		
	
	if pecas[casa[0]][casa[1]] == 0 and peca_selec != casa and eh_possivel:
		pecas[casa[0]][casa[1]] = pecas[peca_selec[0]][peca_selec[1]]
		pecas[peca_selec[0]][peca_selec[1]] = 0
		houve_mov = True
	else:
		print "Movimento inválido."
		
	if comeu:
		pecas[casa_p_comer[0]][casa_p_comer[1]] = 0
	
	
	#transforma ultima linha em dama
	for j in range(8):
		if pecas[0][j] == 2:
			pecas[0][j] = 4
		if pecas[7][j] == 1:
			pecas[7][j] = 3
	
	return houve_mov

# cores pre-definidas
black = (0, 0, 0)
white = (255, 255, 255)
dimgray = (105, 105, 105)
lightgray = (211, 211, 211)
red = (255, 0, 0)
blue = (0, 0, 255)
# tons de marrom
saddlebrown = (139, 69, 19)
sienna = (160, 82, 45)
sandybrown = (244, 164, 96)
burlywood = (222, 184, 135)
wheat = (245, 222, 179)
peru = (205, 133, 63)

# 1 = preta; 2 = branca; 3 = dama preta; 4 = dama branca;
pecas = [[1,0,1,0,1,0,1,0],
		 [0,1,0,1,0,1,0,1],
		 [1,0,3,0,1,0,1,0],
		 [0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0],
		 [0,4,0,2,0,2,0,2],
		 [2,0,2,0,2,0,2,0],
		 [0,2,0,2,0,2,0,2]]

pygame.init()
gameDisplay = pygame.display.set_mode((800,560))
pygame.display.set_caption('Damas')

selecao = 0
turno = 1

while True: #loop principal
	for event in pygame.event.get():
		if event.type == pygame.QUIT: #evento de saída do jogo
			pygame.quit()
			quit()
			
		if pygame.mouse.get_pressed() == (1, 0, 0):
			mouse_x, mouse_y = pygame.mouse.get_pos()
						
			if mouse_x <= 560 and mouse_y <= 560:
				print "Casa selecionada:", mouse_y/70, mouse_x/70
				casa = mouse_y/70, mouse_x/70
				
				if selecao == 1:
					if mover_peca(peca_selec, casa, pecas):
						turno *= -1
					selecao = 0
				elif eh_peca(casa, pecas):
					print "É PEÇA!"
					peca_selec = casa
					selecao = 1
			else:
				selecao = 0
						
			
	
	gameDisplay.fill(white)
	desenha_tabuleiro(pecas)
	
	pygame.display.update()

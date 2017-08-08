# jogo de damas
# coding: utf-8

import time
import pygame
from pygame import gfxdraw

def desenha_tabuleiro(pecas, num_jogadas, turno, mov_poss):
	tam_quad = 70
	x, y = 0, 0

	ha_cap = False
	for i in range(8):
		if 2 in mov_poss[i]:
			ha_cap = True

	for i in range (8):
		for j in range (8):
			if (i + j) % 2 == 0:
				cor = peru
			else:
				cor = wheat
			pygame.draw.rect(gameDisplay, cor, [x, y, tam_quad, tam_quad])

			if not ha_cap:
				if mov_poss[i][j] != 0:
					if mov_poss[i][j] == 1:
						pygame.draw.rect(gameDisplay, cyan, [x, y, 3, tam_quad])
						pygame.draw.rect(gameDisplay, cyan, [x, y, tam_quad, 3])
						pygame.draw.rect(gameDisplay, cyan, [x, y + tam_quad -3, tam_quad, 3])
						pygame.draw.rect(gameDisplay, cyan, [x + tam_quad -3, y, 3, tam_quad])
					else:
						pygame.draw.rect(gameDisplay, red, [x, y, 3, tam_quad])
						pygame.draw.rect(gameDisplay, red, [x, y, tam_quad, 3])
						pygame.draw.rect(gameDisplay, red, [x, y + tam_quad -3, tam_quad, 3])
						pygame.draw.rect(gameDisplay, red, [x + tam_quad -3, y, 3, tam_quad])
			else:
				if mov_poss[i][j] == 2:
					pygame.draw.rect(gameDisplay, red, [x, y, 3, tam_quad])
					pygame.draw.rect(gameDisplay, red, [x, y, tam_quad, 3])
					pygame.draw.rect(gameDisplay, red, [x, y + tam_quad -3, tam_quad, 3])
					pygame.draw.rect(gameDisplay, red, [x + tam_quad -3, y, 3, tam_quad])
						
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

	fonte_jogadas = pygame.font.SysFont(fonte_padrao, 20)
	
	if turno == 1:
		turno_str = "Turno das Brancas"
	else:
		turno_str = "Turno das Pretas"

	texto_jogadas = fonte_jogadas.render('Numero de Jogadas: %d' % num_jogadas, 1, saddlebrown)
	texto_turno = fonte_jogadas.render(turno_str, 1, saddlebrown)
	gameDisplay.blit(texto_jogadas, (610, 30))
	gameDisplay.blit(texto_turno, (610, 60))

def eh_peca(casa, pecas):
	#retorna o tipo de peça presente na casa ou a ausência de uma
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

def eh_possivel_capturar(pecas, turno, houve_cap_antes): # verifica se é possivel capturar alguma peça no turno

	if turno == 1:
		resto_teste = 0 #peças brancas são pares
	else:
		resto_teste = 1 #peças pretas são ímpares

	for i in range(8):
		for j in range(8):
			if pecas[i][j] % 2 == resto_teste and pecas[i][j] != 0:
				movimentos = gera_matriz_movs_possiveis((i, j), pecas, houve_cap_antes)
				for k in range(8):
					if 2 in movimentos[k]:
						return True
	return False

def mover_peca(peca_selec, casa, pecas, mov_poss, houve_cap_antes):
	# retorna se houve movimento
	tipo_peca = pecas[peca_selec[0]][peca_selec[1]]
	eh_possivel = False
	comeu = False
	houve_mov = False

	print "Houve cap antes?", houve_cap_antes
	# as casas estão dispostas em coordenadas (Y, X)
	
	# os testes abaixo devem ser feitos novamente para obter a casa_p_comer específica do movimento selecionado
	if not houve_cap_antes:
		if tipo_peca == 1:
			if casa[0] - peca_selec[0] == 1 and abs(casa[1] - peca_selec[1]) == 1:
				eh_possivel = True
			elif casa[0] - peca_selec[0] == 2 and abs(casa[1] - peca_selec[1]) == 2:
				if casa[1] > peca_selec[1]:
					casa_p_comer = (casa[0] - 1, casa[1] - 1)
				else:
					casa_p_comer = (casa[0] - 1, casa[1] + 1)
				if pecas[casa_p_comer[0]][casa_p_comer[1]] == 2 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 4:
					eh_possivel = True
					comeu = True
					
		elif tipo_peca == 2:
			if casa[0] - peca_selec[0] == -1 and abs(casa[1] - peca_selec[1]) == 1:
				eh_possivel = True
			elif casa[0] - peca_selec[0] == -2 and abs(casa[1] - peca_selec[1]) == 2:
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
	else:
		if tipo_peca == 1 or tipo_peca == 2:
			if abs(casa[0] - peca_selec[0]) == 2 and abs(casa[1] - peca_selec[1]) == 2:

				if casa[0] < peca_selec[0]:
					if casa[1] > peca_selec[1]:
						casa_p_comer = (casa[0] + 1, casa[1] - 1)
					else:
						casa_p_comer = (casa[0] + 1, casa[1] + 1)
				else:
					if casa[1] > peca_selec[1]:
						casa_p_comer = (casa[0] - 1, casa[1] - 1)
					else:
						casa_p_comer = (casa[0] - 1, casa[1] + 1)

				if tipo_peca == 1 and (pecas[casa_p_comer[0]][casa_p_comer[1]] == 2 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 4) or tipo_peca == 2 and (pecas[casa_p_comer[0]][casa_p_comer[1]] == 1 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 3):
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

	if tipo_peca == 2 or tipo_peca == 4:
		turno = 1
	elif tipo_peca == 1 or tipo_peca == 3:
		turno = -1

	ha_cap = eh_possivel_capturar(pecas, turno, houve_cap_antes)

	if ha_cap and mov_poss[casa[0]][casa[1]] != 2:
		return False, ha_cap, peca_selec, houve_cap_antes
	
	if pecas[casa[0]][casa[1]] == 0 and peca_selec != casa and eh_possivel:
		pecas[casa[0]][casa[1]] = pecas[peca_selec[0]][peca_selec[1]]
		pecas[peca_selec[0]][peca_selec[1]] = 0
		houve_mov = True
	else:
		print "Movimento inválido."
		
	if comeu:
		pecas[casa_p_comer[0]][casa_p_comer[1]] = 0

	ha_cap_possivel = eh_possivel_capturar(pecas, turno, ha_cap)
	
	if not ha_cap_possivel: # só devemos transformar a peça em dama quando não houverem mais capturas a serem feitas
		#transforma ultima linha em dama
		for j in range(8):
			if pecas[0][j] == 2:
				pecas[0][j] = 4
			if pecas[7][j] == 1:
				pecas[7][j] = 3
	
	return houve_mov, ha_cap_possivel, casa, comeu

def gera_matriz_movs_possiveis(peca_selec, pecas, houve_cap_antes):
	# retorna se houve movimento
	tipo_peca = pecas[peca_selec[0]][peca_selec[1]]
	mov_poss = [[0,0,0,0,0,0,0,0],
		        [0,0,0,0,0,0,0,0],
		        [0,0,0,0,0,0,0,0],
		        [0,0,0,0,0,0,0,0],
		        [0,0,0,0,0,0,0,0],
		        [0,0,0,0,0,0,0,0],
		        [0,0,0,0,0,0,0,0],
		        [0,0,0,0,0,0,0,0]]
	
	# as casas estão dispostas em coordenadas (Y, X)
	# adicionar damas e seus movimentos
	if not houve_cap_antes:
		for i in range(8):
			for j in range(8):
				casa = (i, j)
				eh_possivel = False
				comeu = False

				if tipo_peca == 1:
					if casa[0] - peca_selec[0] == 1 and abs(casa[1] - peca_selec[1]) == 1:
						eh_possivel = True
					elif casa[0] - peca_selec[0] == 2 and abs(casa[1] - peca_selec[1]) == 2:
						if casa[1] > peca_selec[1]:
							casa_p_comer = (casa[0] - 1, casa[1] - 1)
						else:
							casa_p_comer = (casa[0] - 1, casa[1] + 1)
						if pecas[casa_p_comer[0]][casa_p_comer[1]] == 2 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 4:
							eh_possivel = True
							comeu = True
							
				elif tipo_peca == 2:
					if casa[0] - peca_selec[0] == -1 and abs(casa[1] - peca_selec[1]) == 1:
						eh_possivel = True
					elif casa[0] - peca_selec[0] == -2 and abs(casa[1] - peca_selec[1]) == 2:
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
					if comeu:
						mov_poss[i][j] = 2
					else:
						mov_poss[i][j] = 1

	else:
		for i in range(8):
			for j in range(8):
				casa = (i, j)
				eh_possivel = False
				comeu = False

				if tipo_peca == 1 or tipo_peca == 2:
					if abs(casa[0] - peca_selec[0]) == 2 and abs(casa[1] - peca_selec[1]) == 2:

						if casa[0] < peca_selec[0]:
							if casa[1] > peca_selec[1]:
								casa_p_comer = (casa[0] + 1, casa[1] - 1)
							else:
								casa_p_comer = (casa[0] + 1, casa[1] + 1)
						else:
							if casa[1] > peca_selec[1]:
								casa_p_comer = (casa[0] - 1, casa[1] - 1)
							else:
								casa_p_comer = (casa[0] - 1, casa[1] + 1)

						if tipo_peca == 1 and (pecas[casa_p_comer[0]][casa_p_comer[1]] == 2 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 4) or tipo_peca == 2 and (pecas[casa_p_comer[0]][casa_p_comer[1]] == 1 or pecas[casa_p_comer[0]][casa_p_comer[1]] == 3):
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
					if comeu:
						mov_poss[i][j] = 2
					else:
						mov_poss[i][j] = 1

	return mov_poss

def zera_movs_possiveis():
	mov_poss = [[0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,0],
		    	[0,0,0,0,0,0,0,0]]
	return mov_poss

# cores pre-definidas
black = (0, 0, 0)
white = (255, 255, 255)
dimgray = (105, 105, 105)
lightgray = (211, 211, 211)
red = (255, 0, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
# tons de marrom
saddlebrown = (139, 69, 19)
sienna = (160, 82, 45)
sandybrown = (244, 164, 96)
burlywood = (222, 184, 135)
wheat = (245, 222, 179)
peru = (205, 133, 63)

# 1 = preta; 2 = branca; 3 = dama preta; 4 = dama branca;
pecas = [[0,0,0,0,0,0,0,0],
		 [0,0,1,0,1,0,1,0],
		 [0,0,0,0,0,0,0,0],
		 [0,0,1,0,1,0,1,0],
		 [0,0,0,0,0,0,0,2],
		 [0,0,0,0,0,0,0,0],
		 [0,0,0,0,0,0,0,0],
		 [0,0,0,2,0,0,0,0]]

mov_poss = zera_movs_possiveis()

pygame.init()

gameDisplay = pygame.display.set_mode((800,560))
pygame.display.set_caption('Damas')

pygame.font.init()
fonte_padrao = pygame.font.get_default_font()

selecao = 0
turno = 1 # 1 brancas, -1 pretas
num_jogadas = 0
houve_cap_antes = False
ainda_ha_cap = False
ultima_peca = (-1, -1)

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
					houve_mov, ainda_ha_cap, ultima_peca, houve_cap_antes = mover_peca(peca_selec, casa, pecas, mov_poss, ainda_ha_cap)
					if houve_mov and not houve_cap_antes:
						turno *= -1
						num_jogadas += 1
						houve_cap_antes = False

					selecao = 0
					mov_poss = zera_movs_possiveis()
					
					

				elif eh_peca(casa, pecas):
					print "É PEÇA!"
					peca_selec = casa
					if ((pecas[peca_selec[0]][peca_selec[1]] == 2 or pecas[peca_selec[0]][peca_selec[1]] == 4)  and turno == 1) or ((pecas[peca_selec[0]][peca_selec[1]] == 1 or pecas[peca_selec[0]][peca_selec[1]] == 3) and turno == -1):
						selecao = 1
						mov_poss = gera_matriz_movs_possiveis(peca_selec, pecas, houve_cap_antes)
					else:
						print "Turno inválido!"
			else:
				selecao = 0
				mov_poss = zera_movs_possiveis()
						
			
	
	gameDisplay.fill(white)
	desenha_tabuleiro(pecas, num_jogadas, turno, mov_poss)
	
	pygame.display.update()
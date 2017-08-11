# jogo de damas
# coding: utf-8

import time
import pygame
from pygame import gfxdraw

# cores pre-definidas
black = (0, 0, 0)
white = (255, 255, 255)
dimgray = (105, 105, 105)
lightgray = (211, 211, 211)
red = (255, 0, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
green = (0, 255, 0)
darkorange = (255, 140, 0)
gold = (255, 215, 0)
# tons de marrom
saddlebrown = (139, 69, 19)
sienna = (160, 82, 45)
sandybrown = (244, 164, 96)
burlywood = (222, 184, 135)
wheat = (245, 222, 179)
peru = (205, 133, 63)

pygame.init()

gameDisplay = pygame.display.set_mode((800,560))
pygame.display.set_caption('Damas')

pygame.font.init()
fonte_padrao = pygame.font.get_default_font()
tam_quad = 70

def desenha_tabuleiro(pecas, num_jogadas, turno, mov_poss, status_do_jogo):
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
					elif mov_poss[i][j] == 2:
						pygame.draw.rect(gameDisplay, red, [x, y, 3, tam_quad])
						pygame.draw.rect(gameDisplay, red, [x, y, tam_quad, 3])
						pygame.draw.rect(gameDisplay, red, [x, y + tam_quad -3, tam_quad, 3])
						pygame.draw.rect(gameDisplay, red, [x + tam_quad -3, y, 3, tam_quad])
					elif mov_poss[i][j] == 3:
						pygame.draw.rect(gameDisplay, green, [x, y, tam_quad, tam_quad])
					elif mov_poss[i][j] == 4:
						pygame.draw.rect(gameDisplay, red, [x, y, tam_quad, tam_quad])
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
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 15, gold)
				pygame.gfxdraw.aacircle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, black)
			elif pecas[i][j] == 4:
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 10, white)
				pygame.gfxdraw.filled_circle(gameDisplay, x + tam_quad/2, y + tam_quad/2, tam_quad/2 - 15, gold)
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
				if obstruido == 0:
					tipo_peca_captura = pecas[casa1[0] + n * sinal][casa1[1] + n * sinal]
					casa_captura = (casa1[0] + n * sinal, casa1[1] + n * sinal)
					obstruido = 2
				else:
					obstruido = 1
					
	elif tipo_diag == 2: # diagonal inversa 
		for n in range(1, dist):
			if pecas[casa1[0] + n * sinal][casa1[1] - n * sinal] != 0:
				if obstruido == 0:
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

def eh_possivel_capturar_especifico(pecas, turno, capturas_suce, peca_selec): # verifica se uma peça específica pode capturar alguma peça no turno

	movimentos = gera_matriz_movs_possiveis(peca_selec, pecas, capturas_suce, turno)
	for k in range(8):
		if 2 in movimentos[k]:
			return True
	return False

def eh_possivel_capturar_geral(pecas, turno, capturas_suce): # verifica se é possivel capturar alguma peça no turno

	if turno == 1:
		resto_teste = 0 #peças brancas são pares
	else:
		resto_teste = 1 #peças pretas são ímpares

	for i in range(8):
		for j in range(8):
			if pecas[i][j] % 2 == resto_teste and pecas[i][j] != 0:
				movimentos = gera_matriz_movs_possiveis((i, j), pecas, capturas_suce, turno)
				for k in range(8):
					if 2 in movimentos[k]:
						return True
	return False

def mover_peca(peca_selec, casa, pecas, mov_poss, capturas_suce, casa_atual):
	# retorna se houve movimento
	tipo_peca = pecas[peca_selec[0]][peca_selec[1]]
	eh_possivel = False
	comeu = False
	houve_mov = False

	if len(capturas_suce) > 0:
		houve_cap_antes = True
	else:
		houve_cap_antes = False

	if tipo_peca == 2 or tipo_peca == 4:
		turno = 1
	elif tipo_peca == 1 or tipo_peca == 3:
		turno = -1
	# as casas estão dispostas em coordenadas (Y, X)
	
	# os testes abaixo devem ser feitos novamente para obter a casa_p_comer específica do movimento selecionado
	if tipo_peca == 1 or tipo_peca == 2:
		if tipo_peca == 1:
			if casa[0] - peca_selec[0] == 1 and abs(casa[1] - peca_selec[1]) == 1:
				eh_possivel = True
		else:
			if casa[0] - peca_selec[0] == -1 and abs(casa[1] - peca_selec[1]) == 1:
				eh_possivel = True
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

	if eh_possivel_capturar_geral(pecas, turno, capturas_suce) and mov_poss[casa[0]][casa[1]] != 2 and not houve_cap_antes:
		return False, True, casa_atual
	elif eh_possivel_capturar_especifico(pecas, turno, capturas_suce, casa_atual) and mov_poss[casa[0]][casa[1]] != 2:
		return False, True, casa_atual
	
	if pecas[casa[0]][casa[1]] == 0 and peca_selec != casa and eh_possivel:
		pecas[casa[0]][casa[1]] = pecas[peca_selec[0]][peca_selec[1]]
		pecas[peca_selec[0]][peca_selec[1]] = 0
		houve_mov = True
		casa_atual = casa
	else:
		print "Movimento inválido."
	
	if comeu:
		capturas_suce.append((casa_p_comer[0], casa_p_comer[1]))

	if len(capturas_suce) > 0:
		houve_cap_antes = True
	else:
		houve_cap_antes = False

	if not houve_cap_antes:
		ha_cap_possivel = eh_possivel_capturar_geral(pecas, turno, capturas_suce)
	else:
		ha_cap_possivel = eh_possivel_capturar_especifico(pecas, turno, capturas_suce, casa_atual)
	
	if not ha_cap_possivel: # só devemos transformar a peça em dama quando não houverem mais capturas a serem feitas
		#transforma ultima linha em dama
		for j in range(8):
			if pecas[0][j] == 2:
				pecas[0][j] = 4
			if pecas[7][j] == 1:
				pecas[7][j] = 3

		for j in range(len(capturas_suce)): # as peças capturadas só deverão sumir do tabuleiro ao fim da jogada
			pecas[capturas_suce[j][0]][capturas_suce[j][1]] = 0
	
	if houve_mov and not comeu:
		return True, False, casa_atual

	return houve_mov, ha_cap_possivel, casa_atual

def gera_matriz_movs_possiveis(peca_selec, pecas, capturas_suce, turno):
	# retorna se houve movimento
	tipo_peca = pecas[peca_selec[0]][peca_selec[1]]
	mov_poss = zera_movs_possiveis()
	ha_captura = False

	if ((pecas[peca_selec[0]][peca_selec[1]] == 2 or pecas[peca_selec[0]][peca_selec[1]] == 4)  and turno == 1) or ((pecas[peca_selec[0]][peca_selec[1]] == 1 or pecas[peca_selec[0]][peca_selec[1]] == 3) and turno == -1):
		for i in range(8):
			for j in range(8):
				casa = (i, j)
				eh_possivel = False
				comeu = False

				if tipo_peca == 1 or tipo_peca == 2:
					if tipo_peca == 1:
						if casa[0] - peca_selec[0] == 1 and abs(casa[1] - peca_selec[1]) == 1:
							eh_possivel = True
					else:
						if casa[0] - peca_selec[0] == -1 and abs(casa[1] - peca_selec[1]) == 1:
							eh_possivel = True
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
					if comeu and casa_p_comer not in capturas_suce:
						houve_cap = True
						mov_poss[i][j] = 2
					else:
						mov_poss[i][j] = 1
	return mov_poss

def verifica_movs_possiveis(mov_poss, pecas, capturas_suce, turno):
	if eh_possivel_capturar_geral(pecas, turno, capturas_suce):
		for i in range(8):
			for j in range(8):
				if mov_poss[i][j] == 1:
					mov_poss[i][j] = 0

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

def testa_fim_de_jogo(pecas, num_jogadas, status_do_jogo):
	# False para não terminou; True para terminou. 0 para empate, 1 para pretas, 2 para brancas
	qtde_pecas = [0, 0, 0, 0, 0]
	for i in range(8):
		for j in range(8):
			qtde_pecas[pecas[i][j]] += 1

	if (qtde_pecas[2] != 0 or qtde_pecas[4] != 0) and (qtde_pecas[1] == 0 and qtde_pecas[3] == 0):
		return True, 2
	elif (qtde_pecas[1] != 0 or qtde_pecas[3] != 0) and (qtde_pecas[2] == 0 and qtde_pecas[4] == 0):
		return True, 1
	elif qtde_pecas[1] + qtde_pecas[2] == 2 and qtde_pecas[3] + qtde_pecas[4] == 0:
		return True, 0

	return False, 0

def tela_fim_de_jogo(vencedor):
	if vencedor == 0:
		str_venc = "         Houve empate!"
	elif vencedor == 1:
		str_venc = "O jogador Preto venceu!"
	else:
		str_venc = "O jogador Branco venceu!"

	fonte_vencedor = pygame.font.SysFont(fonte_padrao, 60)
	fonte_legenda = pygame.font.SysFont(fonte_padrao, 30)

	texto_vencedor = fonte_vencedor.render(str_venc, 1, saddlebrown)
	texto_continuar = fonte_legenda.render("Pressione qualquer tecla para continuar.", 1, saddlebrown)

	gameDisplay.fill(burlywood)
	gameDisplay.blit(texto_vencedor, (150, 240))
	gameDisplay.blit(texto_continuar, (200, 530))
	pygame.display.update()

	sair = False
	while not sair:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				sair = True

def regras():
	fonte_titulo = pygame.font.SysFont(fonte_padrao, 60)
	fonte_legenda = pygame.font.SysFont(fonte_padrao, 30)

	texto_titulo = fonte_titulo.render("Regras", 1, saddlebrown)
	texto_continuar = fonte_legenda.render("Pressione qualquer tecla para retornar.", 1, saddlebrown)

	gameDisplay.fill(burlywood)
	gameDisplay.blit(texto_titulo, (320, 10))
	gameDisplay.blit(fonte_legenda.render("1. O jogo de damas e praticado em um tabuleiro de 64 casas, claras e escuras,", 1, saddlebrown), (20, 80))
	gameDisplay.blit(fonte_legenda.render("    entre dois parceiros, com 12 pedras brancas de um lado e com 12 pedras", 1, saddlebrown), (20, 110))
	gameDisplay.blit(fonte_legenda.render("    pretas de outro lado.", 1, saddlebrown), (20, 140))
	gameDisplay.blit(fonte_legenda.render("2. A pedra anda apenas para frente, uma casa por vez. Ao atingir a oitava linha", 1, saddlebrown), (20, 170))
	gameDisplay.blit(fonte_legenda.render("    do tabuleiro, vira dama.", 1, saddlebrown), (20, 200))
	gameDisplay.blit(fonte_legenda.render("3. A dama tem movimentacao diferenciada, anda para frente e para tras quantas", 1, saddlebrown), (20, 230))
	gameDisplay.blit(fonte_legenda.render("    casas quiser.", 1, saddlebrown), (20, 260))
	gameDisplay.blit(fonte_legenda.render("4. A captura e obrigatoria. Tanto a pedra quanto a dama podem capturar para", 1, saddlebrown), (20, 290))
	gameDisplay.blit(fonte_legenda.render("    frente e para tras.", 1, saddlebrown), (20, 320))
	gameDisplay.blit(fonte_legenda.render("5. A pedra so sera coroada dama ao finalizar a jogada numa casa de coroacao.", 1, saddlebrown), (20, 350))
	gameDisplay.blit(fonte_legenda.render("Fonte: http://www.damasciencias.com.br/regras/regras_do_jogo.html", 1, saddlebrown), (60, 410))
	gameDisplay.blit(texto_continuar, (200, 530))
	pygame.display.update()

	sair = False
	while not sair:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				sair = True

def creditos():
	fonte_titulo = pygame.font.SysFont(fonte_padrao, 60)
	fonte_legenda = pygame.font.SysFont(fonte_padrao, 30)

	texto_titulo = fonte_titulo.render("Creditos", 1, saddlebrown)
	texto_continuar = fonte_legenda.render("Pressione qualquer tecla para retornar.", 1, saddlebrown)

	gameDisplay.fill(burlywood)
	gameDisplay.blit(texto_titulo, (300, 10))
	gameDisplay.blit(fonte_legenda.render("Jogo de damas feito para a disciplina de Programacao 1 - UFCG", 1, saddlebrown), (100, 150))
	gameDisplay.blit(fonte_legenda.render("Aluno: Mateus Queiroz Cunha", 1, saddlebrown), (100, 180))
	gameDisplay.blit(fonte_legenda.render("Versao Python: 2.7.x", 1, saddlebrown), (100, 210))
	gameDisplay.blit(fonte_legenda.render("Versao Pygame: 1.9.1", 1, saddlebrown), (100, 240))
	gameDisplay.blit(texto_continuar, (200, 530))
	pygame.display.update()

	sair = False
	while not sair:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				sair = True

def menu_inicial():
	gameDisplay.fill(burlywood)
	fonte_titulo = pygame.font.SysFont(fonte_padrao, 60)
	fonte_botao = pygame.font.SysFont(fonte_padrao, 30)
	gameDisplay.blit(fonte_titulo.render("Jogo de Damas", 1, saddlebrown), (250, 150))
	while True:
		
		for event in pygame.event.get():
			mouse_x, mouse_y = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if mouse_y > 250 and mouse_y < 250 + 30 and mouse_x > 325 and mouse_x < 325 + 150:
				pygame.draw.rect(gameDisplay, saddlebrown, [325, 250, 150, 30])
				gameDisplay.blit(fonte_botao.render("Iniciar", 1, wheat), (370,253))
			else:
				pygame.draw.rect(gameDisplay, wheat, [325, 250, 150, 30])
				gameDisplay.blit(fonte_botao.render("Iniciar", 1, saddlebrown), (370,253))

			if mouse_y > 300 and mouse_y < 300 + 30 and mouse_x > 325 and mouse_x < 325 + 150:
				pygame.draw.rect(gameDisplay, saddlebrown, [325, 300, 150, 30])
				gameDisplay.blit(fonte_botao.render("Regras", 1, wheat), (365,303))
			else:
				pygame.draw.rect(gameDisplay, wheat, [325, 300, 150, 30])
				gameDisplay.blit(fonte_botao.render("Regras", 1, saddlebrown), (365,303))

			if mouse_y > 350 and mouse_y < 360 + 30 and mouse_x > 325 and mouse_x < 325 + 150:
				pygame.draw.rect(gameDisplay, saddlebrown, [325, 350, 150, 30])
				gameDisplay.blit(fonte_botao.render("Creditos", 1, wheat), (360,353))
			else:
				pygame.draw.rect(gameDisplay, wheat, [325, 350, 150, 30])
				gameDisplay.blit(fonte_botao.render("Creditos", 1, saddlebrown), (360,353))

			if mouse_y > 400 and mouse_y < 400 + 30 and mouse_x > 325 and mouse_x < 325 + 150:
				pygame.draw.rect(gameDisplay, saddlebrown, [325, 400, 150, 30])
				gameDisplay.blit(fonte_botao.render("Sair", 1, wheat), (380,403))
			else:
				pygame.draw.rect(gameDisplay, wheat, [325, 400, 150, 30])
				gameDisplay.blit(fonte_botao.render("Sair", 1, saddlebrown), (380,403))

			if pygame.mouse.get_pressed() == (1, 0, 0):
				if mouse_x > 325 and mouse_x < 325 + 150:
					if mouse_y > 250 and mouse_y < 250 + 30:
						jogo()
						gameDisplay.fill(burlywood)
						gameDisplay.blit(fonte_titulo.render("Jogo de Damas", 1, saddlebrown), (250, 150))
					elif mouse_y > 300 and mouse_y < 300 + 30:
						regras()
						gameDisplay.fill(burlywood)
						gameDisplay.blit(fonte_titulo.render("Jogo de Damas", 1, saddlebrown), (250, 150))
					elif mouse_y > 350 and mouse_y < 360 + 30:
						creditos()
						gameDisplay.fill(burlywood)
						gameDisplay.blit(fonte_titulo.render("Jogo de Damas", 1, saddlebrown), (250, 150))
					elif mouse_y > 400 and mouse_y < 400 + 30:
						pygame.quit()
						quit()

		pygame.display.update()

def jogo():
	# 1 = preta; 2 = branca; 3 = dama preta; 4 = dama branca;

	#teste dama fim da jogada e empate 1vs1
	pecas = [[0,0,0,0,0,0,0,0],
			 [0,0,1,0,1,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [1,0,0,0,0,0,1,0],
			 [0,0,0,0,0,0,0,2],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [0,0,2,0,0,0,0,0]]

	# Tabuleiro completo
	#pecas = [[1,0,1,0,1,0,1,0],
	#  		 [0,1,0,1,0,1,0,1],
	#		 [1,0,1,0,1,0,1,0],
	#  		 [0,0,0,0,0,0,0,0],
	#  		 [0,0,0,0,0,0,0,0],
	#		 [0,2,0,2,0,2,0,2],
	#  		 [2,0,2,0,2,0,2,0],	
	#  		 [0,2,0,2,0,2,0,2]]

	# Teste captura dupla
	#pecas = [[1,0,1,0,1,0,1,0],
	#  		 [0,1,0,1,0,1,0,1],
	#		 [0,0,0,0,0,0,0,0],
	#  		 [0,0,0,0,0,0,0,0],
	#  		 [0,0,0,0,0,0,0,0],
	#		 [0,1,0,0,0,1,0,0],
	#  		 [2,0,2,0,2,0,2,0],	
	#  		 [0,2,0,2,0,2,0,2]]

	mov_poss = zera_movs_possiveis()

	selecao = 0
	status_do_jogo = [0, 0, 0, 1] #qtde de brancas, qtde de pretas, num_jogadas, turno
	ainda_ha_cap = False
	ultima_peca = (-1, -1)
	capturas_suce = []
	fim_de_jogo = False
	casa_atual = (0,0)

	fonte_botao = pygame.font.SysFont(fonte_padrao, 30)

	while not fim_de_jogo: #loop principal

		for event in pygame.event.get():
			mouse_x, mouse_y = pygame.mouse.get_pos()
			if event.type == pygame.QUIT: #evento de saída do jogo
				pygame.quit()
				quit()
			
			if pygame.mouse.get_pressed() == (1, 0, 0):
				if mouse_y > 500 and mouse_y < 500 + 30 and mouse_x > 600 and mouse_x < 600 + 150:
					fim_de_jogo = True
				if mouse_x < 560 and mouse_y < 560:
					print "Casa selecionada:", mouse_y/70, mouse_x/70
					casa = mouse_y/70, mouse_x/70
					
					if selecao == 1:
						houve_mov, ainda_ha_cap, casa_atual = mover_peca(peca_selec, casa, pecas, mov_poss, capturas_suce, casa_atual)
						if houve_mov and not ainda_ha_cap:
							status_do_jogo[3] *= -1 #muda o turno
							status_do_jogo[2] += 1 #qtde de jogadas
							capturas_suce = []

						selecao = 0
						mov_poss = zera_movs_possiveis()
						
						

					elif eh_peca(casa, pecas):
						print "É PEÇA!"
						peca_selec = casa
						if ((pecas[peca_selec[0]][peca_selec[1]] == 2 or pecas[peca_selec[0]][peca_selec[1]] == 4)  and status_do_jogo[3] == 1) or ((pecas[peca_selec[0]][peca_selec[1]] == 1 or pecas[peca_selec[0]][peca_selec[1]] == 3) and status_do_jogo[3] == -1):
							selecao = 1
							mov_poss = gera_matriz_movs_possiveis(peca_selec, pecas, capturas_suce, status_do_jogo[3])
						else:
							print "Turno inválido!"
				else:
					selecao = 0
					mov_poss = zera_movs_possiveis()

		
		verifica_movs_possiveis(mov_poss, pecas, capturas_suce, status_do_jogo[3])
		jogo_acabou, vencedor = testa_fim_de_jogo(pecas, status_do_jogo[2], status_do_jogo)

		gameDisplay.fill(white)
		desenha_tabuleiro(pecas, status_do_jogo[2], status_do_jogo[3], mov_poss, status_do_jogo)
		pygame.draw.rect(gameDisplay, saddlebrown, [600, 500, 150, 30])
		gameDisplay.blit(fonte_botao.render("Voltar", 1, wheat), (647,503))
		
		pygame.display.update()
		
		if jogo_acabou:
			tela_fim_de_jogo(vencedor)
			fim_de_jogo = True

menu_inicial()
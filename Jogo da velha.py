# Interpretação de um jogo da velha a partir de câmera com Open CV 
# Vinicius de Andrade Piovezan - Novembro 2020
# Obejtivo - Jogar o jogo da velha contra uma pessoa, sendo que um robô industrial irá desenhar para o PC
# Foi utilizado como referância desse código o livro : "Introdução a visão computacional com Python e OpenCV", do autor : Ricardo Antonello 
#COM 7
 #Bibliotecas necessárias para o código
from matplotlib import pyplot as plt
import mahotas
import numpy as np
from cv2 import cv2
import time

import Logica_jogo_velha as logica




#Função para facilitar a escrita nas imagem
def escreve(img, texto, cor=(255,0,0)):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, texto, (10,20), fonte, 0.5, cor, 0,cv2.LINE_AA)

def Arrumar_img(imgY,tamanho): #Função para diminuir o tamanho da imagem, mantendo a proporção
    (x,y) = (imgY.shape[1],imgY.shape[0]) #Pega o tamanho da imagem em pixels
    proporcao = float(y/x) #Descobre qual a proporção atual
    largura_nova = tamanho #Aqui a nova largura é especificada 
    altura_nova = int(largura_nova*proporcao)
    tamanho_novo = (largura_nova,altura_nova)
    img_menor = cv2.resize(imgY,tamanho_novo, interpolation = cv2.INTER_AREA)
    return img_menor #Retorna a imagem e uma nova proporção

video = cv2.VideoCapture(0) #chamar abertura da webcam

logica.criar_malha()

fff , imgk = video.read() #Fazer a leitura de um frame do vídeo e armazenar na variável frame
imgk = Arrumar_img(imgk,600)

def Achar_objetos(imgX): #Função para encontrar objetos na imagem, no caso os objetos serão a malha do JOGO > # < e os caracteres utilizados no jogo > X < e > O <

    #img_menor = Arrumar_img(imgX) #Diminui o tamanho da imagem na função apresentada anteriormente 
    img_menor = imgX

    #Passo 1: Conversão para tons de cinza
    imgXX = cv2.cvtColor(img_menor, cv2.COLOR_BGR2GRAY)

    #Passo 2: Blur/Suavização da imagem
    suave = cv2.blur(imgXX, (5, 5)) #A suavização da iamgem pode ser maior, mudando seus parâmetros para 5,5 / 7,7 / 9,9 ... Mas 3,3 já foi o sufuciente nos testes
   # suave = imgXX.copy()
    #Passo 3: Binarização resultando em pixels brancos e pretos
    #A imagem que será binarizada está em tons de cinza, assim tem apenas uma variável de cor, sendo que quando mais próximo de 0, mais preto e quanto mais próximo de 255, mais branco
    bin = suave.copy() #Copia a imagem suavizada

    bin[bin > 100] = 255 #Pixels a cima de 100 são transformados em completamente brancos
    bin[bin < 60] = 0 #Pixels a baixo de 60 são transformados em completamente pretos
    #esses valores de 100 e 60 podem variar de acordo com a imagem e iluminação do ambiente, então testes sãop encessários para encontrar os melhores valores.
    bin = cv2.bitwise_not(bin) # aplica as mudanças e inverte a imagem 

    #Passo 4: Detecção de bordas com Canny
    bordas = cv2.Canny(bin, 70, 150) #Nessa linha, as bordas dos objetos brancos em um fundo preto são detectadas

    #Passo 5: Identificação e contagem dos contornos da imagem
    #OBS: Apenas bordas externas a um desenho são contadas e identificadas, isso para que as bordas internas ao "O" sejam ignoradas
    # então o quadrado central da malha do jogo deve ser aberto em um ponto, para que o que estiver dentro dele possa ser detectado
    # O parâmetro responsável apenas pela identificação da borda externa dos objetos é o >> cv2.RETR_EXTERNAL
    (objetos, lx) = cv2.findContours(bordas.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    #A variável lx (lixo) recebe dados que não são utilizados
    #A váriável objetos armazena um vetor, esse vetor tem o número de objetos como seu número de endereços, então a função len(objetos) retorna o número de objetos encontrados
    #Porem esse não é um vetor siples e sim um vetor multidimencional, cada endereço contem as coordenadas de cada ponto necessário para formar o contorno do objeto
    #isso será utilizado mais a frente para a itentificação do tamanho do objeto e  se é um "X" , "O" ou a malha "#"


    #Toda a parte a baixo que está comentada, abre uma janela mostrando todas as etapas do tratamento de imagem e os contornos identificados
    #Caso queira ver, descomente as linhas, mas para que o código flua e o jogo possa ser jogado, elas devem ser comentadas

    #escreve(imgXX, "Imagem em tons de cinza", 0)
    #escreve(suave, "Suavizacao com Blur", 0)
    #escreve(bin, "Binarizacao com Metodo Otsu", 255)
    #escreve(bordas, "Detector de bordas Canny", 255)
    #temp = np.vstack([np.hstack([imgXX, suave]),np.hstack([bin, bordas])])
    #cv2.imshow("Quantidade de objetos: "+str(len(objetos)), temp)
    #cv2.waitKey(0)

    return objetos #retorna os objetos encontraos

obj_malha = 0 #essa variável irá armazenar qual dos objetos encontrados é a malha do jogo
objetos = Achar_objetos(imgk) #Descobre os objetos contidos no primeiro frame do vídeo salvo
print("Iniciando...")



while 1: # loop principal,irá ficar verificando se há alguma mudança na malha do jogo e caso haja, irá atualizar um vetor que contém tudo que foi jogado na malha
    varNimg = 0 #Essa  variável será urtilizada  para armazenar o número de vezes em que o mesmo frame foi visto em seguida, isso será utilizado na lógica mais a frente
    #As variáveis a seguir vão servir para armazenar a soma dos valores de uma cor de todos os pixel de um frame. Isso servirá para entender quando ocorreu mudanças na imagem
    ValIMGk = 0
    ValIMG1 = 0
    ValIMG2 = 0

    fff , img1 = video.read() #É feita a quisição de um novo frame da câmera
    img1 = Arrumar_img(img1,200)

    for yy in range(0, imgk.shape[0]): # Somatória de uma cor de todos os pixels do primeiro frame retirado no inicio do código
        for xx in range(0, imgk.shape[1]):
            ValIMGk = ValIMGk + imgk[yy, xx,0]

    for yy in range(0, img1.shape[0]): # Somatória de uma cor de todos os pixels de um frame atual
        for xx in range(0, img1.shape[1]):
            ValIMG1 = ValIMG1 + img1[yy, xx,0]

   # objetos = Achar_objetos(imgk)
    n_objetos = len(objetos)
    n_objetos1 = len(objetos)

    #  Essa etapa entende quando a pessoa fez a jogada e libera para o programa interpretar os objetos e atualizar o vetro do jogo
    # Enquanto não houver uma sequencia igual de frames novos, que são diferentes do frame salvo no inicio do código, o programa ficará parado
    # verificando essas condições
    #while (ValIMGk <= (ValIMG1+0.009*ValIMG1) and ValIMGk >= (ValIMG1-0.009*ValIMG1)) or varNimg <= 25: 
    while n_objetos == n_objetos1:
        while varNimg <= 20:

            fff , img1 = video.read() #atualiza o frame img1 para uma foto atual
            img1 = Arrumar_img(img1,200)
            ValIMG1 = 0 #Zera a variável da somatória de cores
            for yy in range(0, img1.shape[0]): #faz uma nova somatória 
                for xx in range(0, img1.shape[1]):
                    ValIMG1 = ValIMG1 + img1[yy, xx,0]

            time.sleep(0.05) # Aguarda um tempo 
            #print(varNimg)
            ff , img2 = video.read() #Faz a leitura de um novo frame atual e salva na img2
            img2 = Arrumar_img(img2,200)
            ValIMG2 = 0 #Zera a variável da somatória de cores
            for yy in range(0, img2.shape[0]): #faz uma nova somatória desse frame
                for xx in range(0, img2.shape[1]):
                    ValIMG2 = ValIMG2 + img2[yy, xx,0]

            if(ValIMG1 <= (ValIMG2 + 0.005*ValIMG2) and ValIMG1 >= (ValIMG2 - 0.005*ValIMG2)): #Verifica se a img1 e a img2 são pelo menos 99,9% iguais
                varNimg = varNimg+1 #Caso sejam iguais,a variável de sequencia de frames igual é incrementada
            else:
                varNimg = 0 #Caso sejam diferentes, a variável de sequencia de frames é zerada
                time.sleep(0.05) # Aguarda um tempo
            
        fff , img1 = video.read() #atualiza o frame img1 para uma foto atual
        img1 = Arrumar_img(img1,600)
        objetos = Achar_objetos(img1) #Achga os objetos presentes em um frame atual
        n_objetos1 = len(objetos)
        varNimg = 0

    #A etapa a seguir vai identificar a malha do jogo "#" e setorizar ela com 9 quadrantes 

    k = 1000 #Vai armazenar o menor valor do eixo vertical
    j = 0 #Vai armazenar o maior valor do eixo vertical
    maior_malha = 0 #Essa variável irá armazenar o mior valor do eixo vertival encontrado, assim achando a malha do jogo

    for ii in range(0, len(objetos)):  #Percorre todo o vetor de objetos pegando o menor e o maior valor do eixo vertical e subtraindo eles para achar o maior objeto
        for y in range(0, len(objetos[ii])):
            if k > objetos[ii][y][0][1]:
                k = objetos[ii][y][0][1]
            if j < objetos[ii][y][0][1]:
                j = objetos[ii][y][0][1]
            if j - k > maior_malha:
                maior_malha = j - k
                obj_malha = ii #Quando o maior objeto for encontrado, ele se´ra armazenado na variável obj_malha
            
    k = 1000 #Vai armazenar o menor valor do eixo vertical
    kk = 1000 #Vai armazenar o menor valor do eixo horizantal
    j = 0 #Vai armazenar o maior valor do eixo vertical
    jj = 0 #Vai armazenar o maior valor do eixo horizantal

    for y in range(0, len(objetos[obj_malha])): #Pega  o menor e o maior valor de coordenada do objeto da malha
        if k > objetos[obj_malha][y][0][1]:
            k = objetos[obj_malha][y][0][1]
        if j < objetos[obj_malha][y][0][1]:
            j = objetos[obj_malha][y][0][1]
            
        if kk > objetos[obj_malha][y][0][0]:
            kk = objetos[obj_malha][y][0][0]
        if jj < objetos[obj_malha][y][0][0]:
            jj = objetos[obj_malha][y][0][0]

            # H   V     H     V   
    malha = (kk,  k,    jj,   j) #Os pontos das extremikdades da malha são armazenados na variável malha

    #>>>Setorização da malha
    distV = (malha[2] - malha[0]) / 3 #Divide o valor vertical da malha em 3 pedaços iguais e armazena o tamanho deles
    distH = (malha[3] - malha[1]) / 3 #Divide o valor horizontal da malha em 3 pedaços iguais e armazena o tamanho deles
    #Inicio no canto superior esquerdo
    #A variável setores irá aramzenar os pontos de cada um dos 9 setores da malha do jogo, isso para que possa ser identificado onde cada letra "X" ou "Y" está 
    #Setores [N quadrado] [Nponto (0 ou 1)] [Val V e val H ]
    Setores =          ( ((malha[0],malha[1]),((malha[0]+distV), (malha[1]+distH))) , (((malha[0]+distV), (malha[1])) , ((malha[0]+2*distV),(malha[1]+distH))) ,  (((malha[0]+2*distV), (malha[1])) , ((malha[0]+3*distV),(malha[1]+distH)))   )
    Setores = Setores +( ((malha[0],malha[1]+distH),((malha[0]+distV), (malha[1]+2*distH))) , (((malha[0]+distV), (malha[1]+distH)) , ((malha[0]+2*distV),(malha[1]+2*distH))) ,  (((malha[0]+2*distV), (malha[1]+distH)) , ((malha[0]+3*distV),(malha[1]+2*distH)))   )
    Setores = Setores +( ((malha[0],malha[1]+2*distH),((malha[0]+distV), (malha[1]+3*distH))) , (((malha[0]+distV), (malha[1]+2*distH)) , ((malha[0]+2*distV),(malha[1]+3*distH))) ,  (((malha[0]+2*distV), (malha[1]+2*distH)) , ((malha[0]+3*distV),(malha[1]+3*distH)))   )

                      #0,1,2,3,4,5,6,7,8
    MALHA_PRINCIPAL = [0,0,0,0,0,0,0,0,0] #Esse vetor vai armazenar a sutuação atual do jogo, onde:
    # 0 > Setor da malha sem nenhuma letra
    # 1 > Setor da malha com "O"
    # 2 > Setor da malha com "X"
    # O jogo fica salva da seguinte forma na variável "MALHA_PRINCIPAL":

    # 0|1|2
    # 3|4|5
    # 6|7|8

    for ii in range (0, len(objetos)):#Verifica todos os objetos encontrados
        x = ii
        fff , imgZ = video.read()
        imgC2 = Arrumar_img(imgZ,400)
        if len(objetos[x]) > 30 and ii != obj_malha: #Se o objeto tiver menos de 30 pontos ele é desconsiderado, pois é um ruidom já que o 'X' e o "O" tem muito mais que isso

            teste = objetos[x]
            k = 1000 #Vai armazenar o menor valor do eixo y
            kk = 1000 #Vai armazenar o menor valor do eixo x

            j = 0 #Vai armazenar o maior valor do eixo y
            jj = 0 #Vai armazenar o maior valor do eixo x
            for y in range(0, len(teste)): #PEga  o menor e o maior valor de coordenada de cada objeto, para poder situar o objeto no tabuleiro
                if k > teste[y][0][1]:
                    k = teste[y][0][1]
                if j < teste[y][0][1]:
                    j = teste[y][0][1]
                    
                if kk > teste[y][0][0]:
                    kk = teste[y][0][0]
                if jj < teste[y][0][0]:
                    jj = teste[y][0][0]
            Endereco = 0
            Qv2_1 = (kk,k)
            Qv2_2 = (jj,j)
            cv2.rectangle(imgC2, Qv2_1, Qv2_2, (234,215,125), 2, 2)
            Qv2_1 = (0,0)
            Qv2_2 = (0,0)
            for i in range(0,9):
                if( kk >= int(Setores[i][0][0])+1 and k >=  int(Setores[i][0][1])+1 and jj <= int(Setores[8][1][0])-1 and j <= int(Setores[8][1][1])-1):
                    Qv2_1 = (int(Setores[i][0][0]) , int(Setores[i][0][1]))#(kk,k)
                    Qv2_2 = (int(Setores[i][1][0]) , int(Setores[i][1][1]))#(jj,j)
                    Endereco = i
                
            #print(i)
            cv2.rectangle(imgC2, Qv2_1, Qv2_2, (234,215,125), 2, 2)

            vet_x = []
            vet_y = []

            for y in range(0, len(teste)):
                teste[y][0][1] = teste[y][0][1] - k
                vet_x.append(teste[y][0][1])
                teste[y][0][0] = teste[y][0][0] - kk
                vet_y.append(teste[y][0][0])

            flag = True
            y = 0
            maior_val_esq = 0 
            while flag == True:
                y = y+1
                if teste[y-1][0][1] <= teste[y][0][1]:
                    maior_val_esq = y
                else:
                    flag = False

            #print(maior_val_esq)

            flag = 0
            numTest = 0
            for y in range(0, len(teste)):
                if teste[y-1][0][1] < teste[y][0][1]:
                    if flag != 1:
                        flag = 1 
                        numTest = numTest + 1

                elif teste[y-1][0][1] > teste[y][0][1]:
                    if flag != 2:
                        flag = 2
                        numTest = numTest + 1
                    
                    
           # print(numTest)

            if teste[int(maior_val_esq/2)][0][0] < teste[0][0][0] and teste[int(maior_val_esq/2)][0][0] < teste[maior_val_esq][0][0]:
                print('o')
                MALHA_PRINCIPAL[Endereco] = 1
            elif numTest >=6 and numTest <= 8:
                print('x')
                MALHA_PRINCIPAL[Endereco] = 2
            else:
                print('não é o')
                #plt.figure()
                #plt.title("'Coordenadas do X e O")
                #plt.xlabel("Numero de pontos")
                #plt.ylabel("Valor do ponto")

                #plt.plot(vet_y, 'r')
                #plt.plot(vet_x, 'b')
                #plt.xlim([0, len(teste)])
                #plt.show()

            #print(MALHA_PRINCIPAL)

            #print(teste)
            objetos[x] = teste

            cv2.drawContours(imgC2, objetos, x, (0, 255, 255), 2)
            escreve(imgC2, str(len(objetos))+" objetos encontrados!")
            #cv2.imshow("Resultado", imgC2)
            #cv2.waitKey(0)
        else:
            print("Objeto ignorado")
    print(MALHA_PRINCIPAL)
    #cv2.waitKey(0)

    logica.Logica(MALHA_PRINCIPAL , 4)
    print("Terminou")
    fff , imgk =  video.read()
    imgk = Arrumar_img(imgk,600)
    objetos = Achar_objetos(imgk)
    imgk = Arrumar_img(imgk,200)

    
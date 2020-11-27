
#EXISTE UM ERRO NO MODO DE JOGO IMPOSSÍVEL!!

#MATRIZ_JOGO = [0,0,0,  0,0,0,  0,0,0]
Dificuldade = 3
from random import randint
import serial
import time

ser = serial.Serial('COM7', 9600)

def criar_malha():
    textoSaida = 'W'
    ser.write(textoSaida.encode()) 
    time.sleep(0.5)
    print("Enviada malha")
    teste = " "
    teste = ser.read()
    print(teste)
    print("terminado malha")
    time.sleep(0.8)
    textoSaida = 'V'
    ser.write(textoSaida.encode()) 
    

def serial_enviar(num):
    letras = ['a','c','d', 'e','f','g', 'h','i','j']
    #time.sleep(1)
    textoSaida = letras[num]
    ser.write(textoSaida.encode()) 
    time.sleep(0.8)
    print("Enviada malha")
    teste = " "
    teste = ser.read()
    print(teste)
    print("terminado malha")
    time.sleep(0.8)
    textoSaida = 'V'
    ser.write(textoSaida.encode()) 

#Dificuldade = 0 # 0 - Fácil - 90% de chance de erro do robô
                # 1 -  Médio - 50% de chance de erro do robô
                # 2 - Difícil - 25% de chance de erro do robô
                # 3 - Impossível - O robô não erra
def Escolher_dificuldade():
    print("Escolha a dificuldade:")
    print("Digite \"0\" para fácil")
    print("Digite \"1\" para médio")
    print("Digite \"2\" para difícil")
    print("Digite \"3\" para impossível")   

    flag_input = 0
    while flag_input == 0:
        Dificuldade_temp = input()
        try:
            if(int(Dificuldade_temp) >= 0 and int(Dificuldade_temp) <= 3 ):
                Dificuldade = int(Dificuldade_temp)
                if Dificuldade == 0:
                    print("Dificuldade selecionada: Fácil!")
                elif Dificuldade == 1:
                    print("Dificuldade selecionada: médio!")
                elif Dificuldade == 2:
                    print("Dificuldade selecionada: dificil!")
                elif Dificuldade == 3:
                    print("Dificuldade selecionada: impossível!")
                flag_input = 1
            else:
                print("Digite um valor entre 0 e 3!")
        except:
            print("Digite um valor válido!")
    return(Dificuldade)

Flag_jogo = 0

#              0                     1                     2                     3                    4                     5                     6                     7                   
#              0 1 2 3 4 5 6 7 8
estrategias = [[1,1,1,0,0,0,0,0,0] , [0,0,0,1,1,1,0,0,0] , [0,0,0,0,0,0,1,1,1] , [1,0,0,1,0,0,1,0,0], [0,1,0,0,1,0,0,1,0] , [0,0,1,0,0,1,0,0,1] , [0,0,1,0,1,0,1,0,0] , [1,0,0,0,1,0,0,0,1] ] 



def Escolher_estrategia(Vet_quadrantes,info,MATRIZ_JOGO):
    var1 = 0
    varx = 0
    valores_iguais = []
    estrategias_liberadas= []
    quadrante_escolhido = 0
    Matriz_dificuldade = [] #Vai armazenar todas as casas disponíveis para escolher uma alatóriamente e jogar, a chance de isso acontecer depende da dificuldade
    var_temp = 0
    flag_dificuldade = 0
    #print(Dificuldade)
    if Dificuldade == 0:
        if randint(0, 100) < 90:
            flag_dificuldade = 1
            #print("Vai ser aleatorio")
    elif Dificuldade == 1:
        if randint(0, 100) < 50:
            flag_dificuldade = 1
    elif Dificuldade == 2:
        if randint(0, 100) < 25:
            flag_dificuldade = 1
    elif Dificuldade == 3:
        flag_dificuldade = 0
                                    #[7, 8, 0, 3] [0, 1, 5, 8] [6, 7, 2, 5] [1, 2, 3, 6]
    if flag_dificuldade == 0:
        #print(Vet_quadrantes)
        flag_situacao = 0
        if Vet_quadrantes == [3, 5, 1, 7, 0, 8] or Vet_quadrantes == [3, 5, 1, 7, 2, 6]:
            flag_situacao = 1
            #print("Situação 1")

        if Vet_quadrantes == [7, 8, 0, 3] or  Vet_quadrantes == [0, 1, 5, 8] or Vet_quadrantes == [6, 7, 2, 5] or  Vet_quadrantes == [1, 2, 3, 6] :
            flag_situacao = 2
            #print("Situação 2")
            Vet_quadrantes_temp = []
            for i in range (0 , len(Vet_quadrantes)):
                if Vet_quadrantes[i] != 1 and Vet_quadrantes[i] != 3 and Vet_quadrantes[i] != 5 and Vet_quadrantes[i] != 7:
                    Vet_quadrantes_temp.append(Vet_quadrantes[i])
            Vet_quadrantes = Vet_quadrantes_temp
        
        if MATRIZ_JOGO == [0,2,0,  0,0,0,  0,0,0] or MATRIZ_JOGO == [0,0,0,  2,0,0,  0,0,0] or MATRIZ_JOGO == [0,0,0,  0,0,2,  0,0,0] or MATRIZ_JOGO == [0,0,0,  0,0,0,  0,2,0]:
            flag_situacao = 3
            Vet_quadrantes_temp = []
            for i in range (0 , len(Vet_quadrantes)):
                if Vet_quadrantes[i] != 4 :
                    Vet_quadrantes_temp.append(Vet_quadrantes[i])
            Vet_quadrantes = Vet_quadrantes_temp

        for i in range (0, 8):
            for ii in range( 0, 9):
                if estrategias[i][ii] * MATRIZ_JOGO[ii] == info:
                    var_temp = 1
            if var_temp == 0:
                if flag_situacao == 0 or (i != 6 and i!= 7):
                    estrategias_liberadas.append(i)
                
            var_temp = 0
        
        #print(Vet_quadrantes)
        #print(estrategias_liberadas)

        for ii in range (0, len(Vet_quadrantes)):
            var1 = 0
            for i in range (0, len(estrategias_liberadas)):
                #print(estrategias_liberadas[i])
                if estrategias[estrategias_liberadas[i]][Vet_quadrantes[ii]] == 1:
                    var1 = var1 + 1
                if varx < var1:
                    varx = var1
                    valores_iguais = []
                    quadrante_escolhido = Vet_quadrantes[ii]
                if varx == var1:
                    valores_iguais.append(Vet_quadrantes[ii])
        #print("Valores iguais" + str(valores_iguais))
        #print("Escolhendo 1 aleatoriamente: " + str(valores_iguais[randint(0, len(valores_iguais)-1)]))
        if(len(valores_iguais) > 0):
            quadrante_escolhido = valores_iguais[randint(0, len(valores_iguais)-1)]
            return(quadrante_escolhido)
        elif(len(valores_iguais) == 0):
            return(Vet_quadrantes[randint(0,len(Vet_quadrantes)-1)])

    elif flag_dificuldade == 1:
        for i in range ( 0, 9):
            if MATRIZ_JOGO[i] == 0:
                Matriz_dificuldade.append(i)

        return(Matriz_dificuldade[randint(0, len(Matriz_dificuldade)-1)])

def Verificar_jogo(MATRIZ_JOGO):
    jogo_Caracteres = []
  
    for i in range (0, 9):
        if MATRIZ_JOGO[i] == 0:
           jogo_Caracteres.append(' ')
        if MATRIZ_JOGO[i] == 1:
           jogo_Caracteres.append('O')
        if MATRIZ_JOGO[i] == 2:
           jogo_Caracteres.append('X')


    print("O jogo atual é: ")

    print(jogo_Caracteres[0] +'|'+ jogo_Caracteres[1] +'|'+ jogo_Caracteres[2])
    print(jogo_Caracteres[3] +'|'+ jogo_Caracteres[4] +'|'+ jogo_Caracteres[5])
    print(jogo_Caracteres[6] +'|'+ jogo_Caracteres[7] +'|'+ jogo_Caracteres[8])
    return



def Logica(MATRIZ,DIFIC):

    MATRIZ_JOGO = MATRIZ
    print(MATRIZ)
    Dificuldade = DIFIC #Escolher_dificuldade()
    Flag_jogo = 0

    Verificar_jogo(MATRIZ_JOGO)

    #flag_jogava_correta = 0
    #valores_aceitos = ['0','1','2','3','4','5','6','7','8']
    #while flag_jogava_correta == 0:
    #    print("\n digite de 0 a 8 o valor da casa em que deseja jogar o X: ")
    #    jogada = input()
    #    try:
    #        if(int(jogada) < 0 or int(jogada) > 8):
    #            print("Jogue um valor de casa válido!")
    #        elif MATRIZ_JOGO[int(jogada)] == 0:
    #            MATRIZ_JOGO[int(jogada)] = 2
    #            flag_jogava_correta = 1
    #        else:
    #            print("Essa casa já está ocupada! Escolha outra.")
    #    except:
    #        print("Jogue um valor de casa válido!")
            
    flag_vitoria = 0

    if (flag_vitoria == 0):

        X_ESTRATEGIAS = [0,0,0,0,0,0,0,0]
        X_N_ESTRATEGIAS = [99]
        O_ESTRATEGIAS = [0,0,0,0,0,0,0,0]
        O_N_ESTRATEGIAS = [99]
        for i in range(0, 8):
            for ii in range(0,9):
                if estrategias[i][ii] * MATRIZ_JOGO[ii] == 2:
                    X_ESTRATEGIAS[i] = X_ESTRATEGIAS[i] + 1
                    if X_N_ESTRATEGIAS[len(X_N_ESTRATEGIAS)-1] != i:
                        X_N_ESTRATEGIAS.append(i)

                if estrategias[i][ii] * MATRIZ_JOGO[ii] == 1:
                    O_ESTRATEGIAS[i] = O_ESTRATEGIAS[i] + 1
                    if O_N_ESTRATEGIAS[len(O_N_ESTRATEGIAS)-1] != i:
                        O_N_ESTRATEGIAS.append(i)

        #print(X_ESTRATEGIAS)
        #print(X_N_ESTRATEGIAS)
        #print(O_ESTRATEGIAS)
        #print(O_N_ESTRATEGIAS)


        X_N_ESTRATEGIAS_PRIORIDADE = [[],[],[]]
        if  len(X_N_ESTRATEGIAS)- 1 > 0:
            for i in range(1,len(X_N_ESTRATEGIAS)):
                if X_ESTRATEGIAS[X_N_ESTRATEGIAS[i]] == 3:
                    X_N_ESTRATEGIAS_PRIORIDADE[2].append(X_N_ESTRATEGIAS[i])

            for i in range(1,len(X_N_ESTRATEGIAS)):
                if X_ESTRATEGIAS[X_N_ESTRATEGIAS[i]] == 2:
                    X_N_ESTRATEGIAS_PRIORIDADE[0].append(X_N_ESTRATEGIAS[i])

            for i in range(1,len(X_N_ESTRATEGIAS)):
                if X_ESTRATEGIAS[X_N_ESTRATEGIAS[i]] == 1:
                    X_N_ESTRATEGIAS_PRIORIDADE[1].append(X_N_ESTRATEGIAS[i])

        #print(X_N_ESTRATEGIAS_PRIORIDADE[0])
        #print(X_N_ESTRATEGIAS_PRIORIDADE[1])      



        O_N_ESTRATEGIAS_PRIORIDADE = [[],[],[]]
        if  len(O_N_ESTRATEGIAS)- 1 > 0:
            for i in range(1,len(O_N_ESTRATEGIAS)):
                if O_ESTRATEGIAS[O_N_ESTRATEGIAS[i]] == 3:
                    O_N_ESTRATEGIAS_PRIORIDADE[2].append(O_N_ESTRATEGIAS[i])

            for i in range(1,len(O_N_ESTRATEGIAS)):
                if O_ESTRATEGIAS[O_N_ESTRATEGIAS[i]] == 2:
                    O_N_ESTRATEGIAS_PRIORIDADE[0].append(O_N_ESTRATEGIAS[i])

            for i in range(1,len(O_N_ESTRATEGIAS)):
                if O_ESTRATEGIAS[O_N_ESTRATEGIAS[i]] == 1:
                    O_N_ESTRATEGIAS_PRIORIDADE[1].append(O_N_ESTRATEGIAS[i])

        

        if (len(X_N_ESTRATEGIAS_PRIORIDADE[2]) > 0) and flag_vitoria == 0:
            #print("Você ganhou, com a estratégia: " + str(X_N_ESTRATEGIAS_PRIORIDADE[2][0]))
            print("Parabéns, você ganhou!")
            flag_vitoria = 1
            Flag_jogo = 1
            Verificar_jogo(MATRIZ_JOGO)
        
        if flag_vitoria == 0:
            flag_velha = 1
            for i in range (0 , 9):
                if MATRIZ_JOGO[i] == 0:
                    flag_velha = 0 

            if flag_velha == 1:
                print("Deu velha!")
                flag_vitoria = 1
                Flag_jogo = 1
                Verificar_jogo(MATRIZ_JOGO)

        

    #São feitas 4 verificações na lógica do jogo:

    #1 - verifica se não tem alguma forma de o robô ganhar o jogo
    #2 - Verifica se a pessoa quee stá jogando não está a um passo de ganhar para poder impedir ela de vencer
    #3 - verifica qual a melhor casa para jogar, de acordo com o que ele já fez
    #4 - Verifica qual a melhor forma de impedir a jogada da pessoa e ainda jogar em um local onde as possibilidades são melhores

    if len(O_N_ESTRATEGIAS_PRIORIDADE[0]) > 0 and flag_vitoria == 0: #Verifica se não existe uma situação em que o robô ganha para jogar no quadrante necessário
        for ii in range (0, len(O_N_ESTRATEGIAS_PRIORIDADE[0])):
            for i in range(0, 9):
                if estrategias[O_N_ESTRATEGIAS_PRIORIDADE[0][ii]][i] == 1 and MATRIZ_JOGO[i] == 0 and flag_vitoria == 0:
                    print("A Jogue no quadrante " + str(i))  
                    MATRIZ_JOGO[i] = 1
                    serial_enviar(i)
                    flag_vitoria = 1
                    Flag_jogo = 1
                    print("Vitoria do robô!!!")
                    Verificar_jogo(MATRIZ_JOGO)

    if len(X_N_ESTRATEGIAS_PRIORIDADE[0]) > 0 and flag_vitoria == 0: 
        for ii in range (0, len(X_N_ESTRATEGIAS_PRIORIDADE[0])): #Verifica se não existe uma situação em que a pessoa ganha para jogar no quadrante necessário e impedir
            for i in range(0, 9):
                if estrategias[X_N_ESTRATEGIAS_PRIORIDADE[0][ii]][i] == 1 and MATRIZ_JOGO[i] == 0 and flag_vitoria == 0:
                    print("B Jogue no quadrante " + str(i))
                    MATRIZ_JOGO[i] = 1
                    serial_enviar(i)
                    flag_vitoria = 1

    if len(O_N_ESTRATEGIAS_PRIORIDADE[1]) > 0 and flag_vitoria == 0: 
        vet_qua_vazio= []
        for ii in range (0, len(O_N_ESTRATEGIAS_PRIORIDADE[1])): #Caso não tenha ngm engatilhado para ganhar, o robô verifica qual o melhor local para jogar de acordo com oq ele já fez
            for i in range(0, 9):
                if estrategias[O_N_ESTRATEGIAS_PRIORIDADE[1][ii]][i] == 1 and MATRIZ_JOGO[i] == 1:
                
                    for iii in range (0,9):
                        
                        if estrategias[O_N_ESTRATEGIAS_PRIORIDADE[1][ii]][iii] == 1 and iii != i and MATRIZ_JOGO[iii] != 2:
                            vet_qua_vazio.append(iii)
        #print("Quadrantes disponíveis 1 " + str(vet_qua_vazio))
        val_temp = Escolher_estrategia(vet_qua_vazio,2,MATRIZ_JOGO)
        print("C Jogue no quadrante " + str(val_temp) )
        MATRIZ_JOGO[val_temp] = 1
        serial_enviar(val_temp)
        flag_vitoria = 1

    if len(X_N_ESTRATEGIAS_PRIORIDADE[1]) > 0 and flag_vitoria == 0: 
        vet_qua_vazio= []
        for ii in range (0, len(X_N_ESTRATEGIAS_PRIORIDADE[1])): #Verifica o que fazer quando a pessoa colocou apenas 1/3 de uma estratégia, como impedir ela e ainda jogar em um lugar bom
            for i in range(0, 9):
                if estrategias[X_N_ESTRATEGIAS_PRIORIDADE[1][ii]][i] == 1 and MATRIZ_JOGO[i] == 2:
                
                    for iii in range (0,9):
                        
                        if estrategias[X_N_ESTRATEGIAS_PRIORIDADE[1][ii]][iii] == 1 and iii != i and MATRIZ_JOGO[iii] != 1:
                            vet_qua_vazio.append(iii)
        #print("Quadrantes disponíveis 2 " + str(vet_qua_vazio))
        val_temp = Escolher_estrategia(vet_qua_vazio,10,MATRIZ_JOGO)
        print("D Jogue no quadrante " + str(val_temp) )
        MATRIZ_JOGO[val_temp] = 1
        serial_enviar(val_temp)
        flag_vitoria = 1

    if (len(O_N_ESTRATEGIAS_PRIORIDADE[2]) > 0) and flag_vitoria == 0:
        print("O robô ganhou, com a estratégia: " + str(O_N_ESTRATEGIAS_PRIORIDADE[2][0]))
        flag_vitoria = 1
        Flag_jogo = 1
    Verificar_jogo(MATRIZ_JOGO)
    
    print("Imagem nova...")
    #input()



         
           
           
           
        


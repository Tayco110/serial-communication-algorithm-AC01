#Código base para se comunicar com um leitor AC-01 via porta serial
#Aldemir Melo Rocha Filho
#Sandoval da Silva ALmeidsa Junior
#Tayco Murilo Santos Rodrigues

#Comentários:
#A ideia foi tentar manter o código o mais modularizado possível
#O bug do aumento da potencia pode ser resolvido encontrando alguma forma de esvaziar o buffer da serial após executar a ação
#Parametros como: Potencia de leitura base, Módulos de controle e tempo que se leva para aguardar o retorno da tag podem ser modificados
#Essas modificações no momento não quebram o código, pois basta apenas mudar variáveis

import serial

#Criação do objeto que vai se comunicar via porta serial
#O leitor está conectado na porta 'COM6' e possui um timeout de leitura de 1.2s
ser = serial.Serial('COM6', 9600, timeout = 1.2)

#tratamento para a tag ativa(precisa ser implementado o controle)
def activatedTagtreatment():
    #Módulo de controle aqui
    print('ATIVADA')
    return

#tratamento para a tag viva(precisa ser implementado o controle)
def aliveTagtreatment():
    #Módulo de controle aqui
    print('VIVA')
    return

#tratamento para a tag que vai para a qualidade(precisa ser implementado o controle)
def qualityTagtreatment():
    #Módulo de controle aqui
    print('QUALIDADE')
    return

#tratamento para a tag morta(precisa ser implementado o controle)
def deadTagTreatment():
    #Módulo de controle aqui
    print('DESCARTE')
    return

#Método que modifica a potencia de leitura do AC-01 e limpa o lixo gerado por essa mudança
#Apresenta um pequeno bug de delay
def setReadPower(readpower):
    ser.write(bytes('readpower '+str(readpower)+'\r\n','utf-8'))
    # A linha (ser.readlines()) que deveria esvaziar o buffer da serial executa com o delay de leitura, 1.2 segundos para esse caso.
    # Quando na verdade deveria funcionar com o tempo de execução do Python
    # Isso implica todo aumento na potencia de leitura irá levar no mínimo 1.2s para ser executado
    ser.readlines() 
    return

#Variável que define a potencia base de leitura das Tags
readpower = 5

while(1):

    #Seta a potencia de leitura base(1.2s)
    setReadPower(readpower)
    #Tentamos ler com a potencia Base (5)
    print('TENTANTO LER COM POTENCIA ' +str(readpower))
    input = ser.readline().decode('utf-8')

    #Se a tag não apresentar retorno em 1.2s 
    if(len(input) == 0):

        #Aumentamos a potencia em potencia base + 2
        setReadPower(readpower + 2)
        #Tentamos ler com a potencia base + 2 (7)
        print('TENTANTO LER COM POTENCIA ' +str(readpower + 2))
        input = ser.readline().decode('utf-8')

        #Se a tag não apresentar retorno em 1.2s 
        if(len(input) == 0):
            #Aumentamos a potencia em potencia base + 5 (10)
            setReadPower(readpower + 5)
            #Tentamos ler com a potencia base + 5 (10)
            print('TENTANTO LER COM POTENCIA ' +str(readpower + 5))
            input = ser.readline().decode('utf-8')
            #Se a tag não apresentar retorno em 1.2s 
            if(len(input) == 0):
                #Tratamos como tag morta e chamamos o tratamento para tag's mortas
                deadTagTreatment()
            #Se a tag apresentar retorno em 1.2s com a potencia base aumentada 
            else:
                #Chamamos o tratamento para tag's enviadas para a qualidade
                qualityTagtreatment()
        #Se a tag apresentar retorno em 1.2s com a potencia base aumentada 
        else:
             #Chamamos o tratamento para tag's enviadas para a qualidade
            qualityTagtreatment()

    #Se a tag em 1.2s retornou uma string com tamanho maior que 30, dois conjuntos de caracteres
    elif(len(input) > 30):
        #Tratamos como tag viva e chamamos o tratamento devido
        aliveTagtreatment()

    #Se a tag em 1.2s não retornou um string com menos de 30 caracteres que não é vazia 
    else:
        #Tratamos como tag ativada e chamamos o tratamento devido
        activatedTagtreatment()

#Fechamos a porta serial ao fim da execução
ser.close()
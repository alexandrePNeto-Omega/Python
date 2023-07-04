####   VAR'S
txtProcess  = open("open.txt")
listToKill  = []

#   Passa por todas as linhas
for p in txtProcess:
    listP  = p.split(' ')
    #   Identifica a palavra
    for c in listP:
        if c != 'root' and c != '':
            strKill = 'kill' + str(c) + "\n"
            listToKill += [strKill]
            break

#   Gerando o arquivo
result  = open("reult.txt", "a")
result.writelines(listToKill)
print("\n------- ARQUIVO GERADO COM SUCESSO! -------")

# Algorito feito para auxiliar em situações 
# adversar no servidores do autosystem.
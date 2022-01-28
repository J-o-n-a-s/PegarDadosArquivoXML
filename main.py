# Realiza a leitura de arquivos XML com o intuito de pegar alguns campos selecionados

import sys
import time


def _abrir_arquivo(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError as erro:
        _log_error(str(sys.exc_info()[0]), erro)
        print(f'\nNão foi possível abrir o arquivo. Verifique o caminho e o nome do arquivo.')
        return 1, ''
    except OSError as erro:
        _log_error(str(sys.exc_info()[0]), erro)
        print(f'\nNão foi possível abrir o arquivo. Verifique o caminho e o nome do arquivo.')
        return 1, ''
    else:
        return 0, linhas


def _log_error(exception, erro):
    with open('\\log\\' + str(time.strftime("%x")) + '.log', 'w') as arquivo:
        arquivo.write(f'{str(time.strftime("%X"))} - {exception} - {erro}')


def leitura_arquivo(caminho):
    while True:
        ret, linhas = _abrir_arquivo(caminho)
        if ret == 0:
            break

        else:
            correto = input('Deseja retentar? "S" para sim e "N" para não: ')
            if correto.lower() == 'n':
                break

    return ret, linhas


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    object_device = []
    bacnet_device = []

    print('Programa para realizar a leitura de arquivos XML e retornar em arquivo CSV o campo selecionado!\n')
    caminho = input('Por gentileza digite o caminho completo e inicio do nome dos arquivos que deseja ler: ')
    num_inicial = int(input('Por gentileza digite o número do index do primeiro arquivo que deseja ler: '))
    num_final = int(input('Por gentileza digite o número do index do último arquivo que deseja ler: '))
    while True:
        info = int(input('Por gentileza digite a opção desejada entre as opções:\n'
                         '1 - Identifier;\n'
                         '2 - Name;\n'
                         '3 - Ambos;\n'
                         '4 - Finalizar.\n'
                         '-> '))
        if info == 4:
            print('\nAté logo!')
            break
        print("\n")
        for num in range(1 + (num_final - num_inicial)):
            pos1 = -1
            pos2 = -1
            caminho_completo = caminho + str(num + num_inicial) + ".xml"
            ret, linhas = leitura_arquivo(caminho_completo)
            try:
                cont = 0
                cont1 = 0
                cont2 = 0
                for linha in linhas:
                    cont += 1
                    if info == 1 or info == 3:
                        if pos1 == -1:
                            pos1 = linha.find('OBJECT_DEVICE:')
                            if pos1 != -1:
                                object_device.append(linha[pos1 + 14: pos1 + 21])
                                cont1 = cont
                                pos1 = -2

                    if info == 2 or info == 3:
                        if pos2 == -1:
                            pos2 = linha.find('BACnetDevice_100_')
                            if pos2 != -1:
                                bacnet_device.append(linha[pos2: pos2 + 25])
                                cont2 = cont
                                pos2 = -2

                    if (info == 1 and pos1 == -2) or\
                            (info == 2 and pos2 == -2) or\
                            (info == 3 and pos1 == -2 and pos2 == -2):
                        print(f'Arquivo {num + num_inicial}:\n')
                        if info == 1 or info == 3:
                            print(f' - Encontrado na linha {cont1} -> Identifier = {object_device[num]}.')
                            # if info == 3:
                            #    print('\n')
                        if info == 2 or info == 3:
                            print(f' - Encontrado na linha {cont2} -> Name = {bacnet_device[num]}.')
                        break

            except KeyboardInterrupt as erro:
                _log_error(str(sys.exc_info()[0]), erro)
                print('\nLeitura interrompida!')
            else:
                print('')

            if num + num_inicial < num_final:
                print('Iniciando verificação do próximo arquivo...\n')
            else:
                try:
                    with open(caminho[0:len(caminho) - 3] + 'Resultado.csv', 'w', encoding='utf-8') as arquivo:
                        arquivo.write('Add;Instance;Name\n')
                        for num1 in range(1 + (num_final - num_inicial)):
                            arquivo.write(f'{num1 + num_inicial};{object_device[num1]};{bacnet_device[num1]}\n')
                except FileNotFoundError as erro:
                    _log_error(str(sys.exc_info()[0]), erro)
                    print(f'\nNão foi possível abrir o arquivo. Verifique o caminho e o nome do arquivo.')
                except OSError as erro:
                    _log_error(str(sys.exc_info()[0]), erro)
                    print(f'\nNão foi possível abrir o arquivo. Verifique o caminho e o nome do arquivo.')

                print('Fim da verificação dos arquivos!\n')
                if info == 3:
                    break

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import json
import csv


def readjson(ano):
    processos = []
    with open("arquivos/json/" + str(ano) + "-dados.json", encoding='utf-8') as meu_json:
        dados = json.load(meu_json)

    for i in dados:
        if i['Situação do Processo'] == "Encerrado":
            splits = i['Deliberações'].split('/')
            num = splits[len(splits) - 1].split('.')
            processos.append(num[0])

    return processos


def crawler(processo, chromeDrivePath, dicProcessos, linksError):
    url1 = 'https://pesquisa.apps.tcu.gov.br/#/documento/processo/*/NUMEROSOMENTENUMEROS%253A'
    url2 = '/DTAUTUACAOORDENACAO%2520desc%252C%2520NUMEROCOMZEROS%2520desc/0/%2520'
    url = url1 + processo + url2
    webdriver0 = webdriver.Chrome(executable_path=chromeDrivePath)
    pecasLink = []
    with webdriver0 as driver:
        WebDriverWait(driver, 10)
        print("Url: " + url)
        driver.get(url)
        time.sleep(10)
        doc = driver.find_elements(By.TAG_NAME, 'app-conteudo-documento')
        for e in doc:
            # Número do processo
            try:
                numProcesso = e.find_element(By.ID, 'conteudo_processo').text
                dicProcessos['processo'].append(numProcesso)
            except:
                print("Não há número do processo: " + processo)
                dicProcessos['processo'].append(processo)

            # Ano do processo
            try:
                anoProcesso = e.find_element(By.ID, 'conteudo_ano').text
                dicProcessos['ano'].append(anoProcesso)
            except:
                print("Não há ano do processo: " + processo)
                dicProcessos['ano'].append("null")

            # Tipo do processo
            try:
                tipoProcesso = e.find_element(By.ID, 'conteudo_tipo_processo').text
                dicProcessos['tipo processo'].append(tipoProcesso)
            except:
                print("Não há tipo do processo: " + processo)
                dicProcessos['tipo processo'].append("null")

            # Unidade técnica responsável
            try:
                unidade = e.find_element(By.ID, 'conteudo_unidade_tecnica_responsavel').text
                dicProcessos['unidade técnica responsável'].append(unidade)
            except:
                print("Não há unidade do processo: " + processo)
                dicProcessos['unidade técnica responsável'].append("null")

            # Unidade responsável por agir
            try:
                agir = e.find_element(By.ID, 'conteudo_unidade_responsavel_agir').text
                dicProcessos['unidade responsável agir'].append(agir)
            except:
                print("Não há agir do processo: " + processo)
                dicProcessos['unidade responsável agir'].append("null")

            # Relator
            try:
                relator = e.find_element(By.ID, 'conteudo_relator').text
                dicProcessos['relator'].append(relator)
            except:
                print("Não há relator do processo: " + processo)
                dicProcessos['relator'].append("null")

            # Responsáveis
            try:
                responsaveis = e.find_element(By.ID, 'conteudo_responsaveis').text
                dicProcessos['responsáveis'].append(responsaveis)
            except:
                try:
                    print("Não há texto direto em id responsáveis!")
                    responsaveis = e.find_elements(By.XPATH, '//*[@id="conteudo_responsaveis"]/div/ul/li')
                    respText = []
                    for r in responsaveis:
                        respText.append(r.text)
                    dicProcessos['responsáveis'].append(respText)
                except:
                    print("Não há responsáveis no processo: " + processo)
                    dicProcessos['responsáveis'].append("null")

            # Estado
            try:
                estado = e.find_element(By.ID, 'conteudo_estado').text
                dicProcessos['estado'].append(estado)
            except:
                print("Não há estado no processo: " + processo)
                dicProcessos['estado'].append("null")

            # Assunto
            try:
                assunto = e.find_element(By.ID, 'conteudo_assunto_processo').text
                dicProcessos['assunto'].append(assunto)
            except:
                print("Não há assunto no processo: " + processo)
                dicProcessos['assunto'].append("null")

            # Unidades Jurisdiconadas
            try:
                unijur = e.find_element(By.ID, 'conteudo_unidadesJurisdicionadas').text
                dicProcessos['unidades jurisdicionadas'].append(unijur)
            except:
                try:
                    print("Não há texto direto em id unidades jurisdicionadas!")
                    unijur = e.find_elements(By.XPATH, '//*[@id="conteudo_unidadesJurisdicionadas"]/div/ul/li')
                    unijurText = []
                    for u in unijur:
                        unijurText.append(u.text)
                    dicProcessos['unidades jurisdicionadas'].append(unijurText)
                except:
                    print("Não há unidades jurisdicionadas no processo: " + processo)
                    dicProcessos['unidades jurisdicionadas'].append("null")

            # Peças
            try:
                pecas = e.find_elements(By.CLASS_NAME, 'relacionados__link')
                print(len(pecas))
                pecastext = []
                for a in pecas:
                    pecastext.append(a.text)
                    pecasLink.append(a.get_attribute('href'))

                dicProcessos['peças'].append(pecastext)
                dicProcessos['peças links'].append(pecasLink)
            except:
                print("Não há peças no processo: " + processo)
                dicProcessos['peças'].append("null")
                dicProcessos['peças links'].append("null")

            # Movimentações
            try:
                mov = e.find_element(By.ID, 'conteudo_movimentacoes').text
                dicProcessos['movimentações'].append(mov)
            except:
                print("Não há movimentações no processo: " + processo)
                dicProcessos['movimentações'].append("null")

            if len(pecasLink) > 0:
                crawlerLinks(pecasLink, chromeDrivePath, linksError, processo)


def crawlerLinks(pecasLink, chromeDrivePath, linksError, processo):
    webdriver1 = webdriver.Chrome(executable_path=chromeDrivePath)
    for link in pecasLink:
        try:
            WebDriverWait(webdriver1, 10)
            webdriver1.get(link)
            time.sleep(10)
        except:
            linksError['processo'].append(processo)
            linksError['link'].append(link)


if __name__ == '__main__':
    chromeDrivePath = 'E:/DownloadsProgramas/chromedriver_win32/chromedriver.exe'
    dicProcessos = {'processo': [], 'ano': [], 'tipo processo': [], 'unidade técnica responsável': [],
                    'unidade responsável agir': [],
                    'relator': [], 'responsáveis': [], 'estado': [], 'assunto': [], 'unidades jurisdicionadas': [],
                    'peças': [], 'peças links': [],
                    'movimentações': []}
    linksError = {'processo': [], 'link': []}
    ano = 2020
    processosField = readjson(ano)
    print(processosField)
    print(len(processosField))
    for index, processo in enumerate(processosField):
        print(str(index) + ": " + processo)
        crawler(processo, chromeDrivePath, dicProcessos, linksError)
    print(dicProcessos)
    df = pd.DataFrame(dicProcessos)
    df.to_csv('C:/Users/Sabrina/PycharmProjects/tcu/' + str(ano) + '-dadosFaltantes.csv', encoding='utf-8', sep=';')
    print(linksError)
    df1 = pd.DataFrame(linksError)
    df1.to_csv('C:/Users/Sabrina/PycharmProjects/tcu/' + str(ano) + '-linksError.csv', encoding='utf-8', sep=';')

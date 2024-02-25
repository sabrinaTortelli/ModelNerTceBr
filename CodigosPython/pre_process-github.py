import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import textract
from typing import List
from unicodedata import normalize
import unicodedata


def _convert_pdf_to_text(path):
    text = ''
    try:
        resource_manager = PDFResourceManager(caching=True)
        out_text = StringIO()
        laparams = LAParams()
        text_converter = TextConverter(resource_manager, out_text, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(resource_manager, text_converter)

        for page in PDFPage.get_pages(fp, set(), maxpages=0, password="", caching=True, check_extractable=True):
            interpreter.process_page(page)

        text = out_text.getvalue()
        fp.close()
        text_converter.close()
        out_text.close()
        # Limpa o texto antes de salvar em txt
        return clean_text(text, path)
    except:
        print("Erro na conversão para pdf no arquivo " + path)
        return text


def clean_text(text, path):
    try:
        res = re.sub(
            "para verificar as assinaturas, acesse www.tcu.gov.br/autenticidade, informando o código [0-9]*.\s*[0-9]*\s*\f",
            '',
            text, flags=re.IGNORECASE)
        res = re.sub(
            "TRIBUNAL DE CONTAS DA UNIÃO\s*Secretaria-Geral de Controle Externo\s*Secretaria de Controle Externo de Tomada de Contas Especial\s*[1-9]*\s*",
            '',
            res, flags=re.IGNORECASE)
        res = re.sub(
            "TC\s*[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,4}-[0-9]{1}\s*TRIBUNAL DE CONTAS DA UNIÃO",
            '',
            res, flags=re.IGNORECASE)
        res = re.sub(
            "TRIBUNAL DE CONTAS DA UNIÃO\s*TC\s*[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,4}-[0-9]{1}",
            '',
            res, flags=re.IGNORECASE)
        res = re.sub(
            "TRIBUNAL DE CONTAS DA UNIÃO\s*Secretaria-Geral de Controle Externo\s*Secretaria de Controle Externo no Estado de Goiás\s*[1-9]*\s*",
            '',
            res, flags=re.IGNORECASE)
        res = re.sub(
            "TRIBUNAL DE CONTAS DA UNI\s*ÃO\s*Secretaria-Geral de Controle Externo\s*Secretaria de Controle Externo no Estado de Minas Gerais\s*[1-9]*\s*",
            '',
            res, flags=re.IGNORECASE)
        res = re.sub(
            "TRIBUNAL DE CONTAS DA UNIÃO\s*(Secretaria-Geral de Controle Externo)*\s*Secretaria de Recursos\s*1",
            '',
            res, flags=re.IGNORECASE)
        res = re.sub("\f|\v|\r|\t|\a|\b|\n", '', res)
        res = re.sub(" +", ' ', res)
        res = re.sub(
            "Documento eletrônico gerado automaticamente pelo Sistema SAGAS",
            '',
            res, flags=re.IGNORECASE)
        res = re.sub(r"[\\(]*assinado eletr[ô|o]nicamente[\\)]*", '', res, flags=re.IGNORECASE)
        res = re.sub(u"\u2013", u"\u002D", res, flags=re.IGNORECASE)
        res = re.sub(u"\u2018", u"\u0060", res, flags=re.IGNORECASE)
        res = re.sub(
            u"[\u2022|\u2023|\u2024|\u2025|\u2026|\u2027|\u00B7|\u2043|\u204C|\u204D|\u2219|\u25CB|\u25CF|\u25E6|\u2619|\u2765|\u2767|\u29BE|\u29BF|\u25C9|]",
            '', res)
        res = re.sub(u"[\uFFFD|\u001A|\u2BD1|\U0001FBC4|\uFFF0-\uFFFF|\uF0B7]", '', res)
        res = non_ascii_to_ascii(res)
        res = re.sub(" +", ' ', res)
        res = res.strip()
        return res
    except:
        print("Erro ao limpar o arquivo: " + path)
        return text


def save_txt(text, name_file):
    try:
        with open(name_file, 'w') as file:
            file.write(text)
    except:
        print("Erro ao salvar o arquivo: " + name_file)


def convert_pdf_to_text(folder):
    for file_name in os.listdir(folder):
        try:
            address_file = folder + file_name
            text = _convert_pdf_to_text(address_file)
            # remove a extensão do nome do arquivo
            y = file_name.find(".")
            name = file_name[:y]
            dest_folder = r'E:/TCC/TodosDados/AC_TXT//'
            new_name_file = dest_folder + name + '.txt'
            save_txt(text, new_name_file)
        except:
            print("Erro no arquivo: " + file_name)
            continue


def get_unicode_code_points(string: str) -> List[str]:
    string_normalized = normalize('NFD', string)
    code_points: List[str] = [
        'U+' + hex(ord(letter))[2:].zfill(4).upper()
        for letter in string_normalized
    ]
    return code_points


def non_ascii_to_ascii(string: str) -> str:
    ascii_only = unicodedata.normalize('NFKD', string) \
        .encode('ascii', 'ignore') \
        .decode('ascii')
    return ascii_only


if __name__ == '__main__':
    url_path = r'E:/TCC/TodosDados/AC//'
    convert_pdf_to_text(url_path)

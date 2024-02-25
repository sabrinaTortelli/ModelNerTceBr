import os
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

def tokenizar_e_salvar_em_arquivo(input_folder, output_folder):
    try:
        # Garante que a pasta de saída exista
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Lista de arquivos na pasta de entrada
        file_list = os.listdir(input_folder)

        for file_name in file_list:
            if file_name.endswith(".txt"):
                input_file_path = os.path.join(input_folder, file_name)
                output_file_path = os.path.join(output_folder, file_name)

                with open(input_file_path, 'r', encoding='utf-8') as input_file:
                    text = input_file.read()

                # Tokenização
                tokens = word_tokenize(text)

                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for token in tokens:
                        output_file.write(token + '\n')

                print(f"Tokenização concluída para {file_name}. Tokens salvos em {output_file_path}")

    except FileNotFoundError:
        print(f"Pasta {input_folder} não encontrada.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")


def separar_sentencas_e_salvar_em_arquivo(input_folder, output_folder):
    try:
        # Garante que a pasta de saída exista
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Lista de arquivos na pasta de entrada
        file_list = os.listdir(input_folder)

        for file_name in file_list:
            if file_name.endswith(".txt"):
                input_file_path = os.path.join(input_folder, file_name)
                output_file_path = os.path.join(output_folder, file_name)

                with open(input_file_path, 'r', encoding='utf-8') as input_file:
                    text = input_file.read()

                # Separação das sentenças
                sentences = sent_tokenize(text)

                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for sentence in sentences:
                        output_file.write(sentence + '\n')

                print(f"Separação das sentenças concluída para {file_name}. Sentenças salvas em {output_file_path}")

    except FileNotFoundError:
        print(f"Pasta {input_folder} não encontrada.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")


if __name__ == '__main__':

    input_folder = 'E:/TCC/TodosDados/AC_INC_SEM_SENTENCE_2'
    output_folder = 'E:/TCC/TodosDados/AC_INC_FINAL_2'

    separar_sentencas_e_salvar_em_arquivo(input_folder, output_folder)
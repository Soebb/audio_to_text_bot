import tokens
import telebot
import requests
import speech_recognition as sr
from pydub import AudioSegment
import os
import pretty_errors

bot = telebot.AsyncTeleBot(tokens.BOT_TOKEN)
r = sr.Recognizer()
pasta_de_audio = os.path.join(os.getcwd(), 'audios')

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """Responde a com uma mensagem de boas vindas e uma descrição da usabilidade.
    Args:
        message (Message): Mensagem recebida do usuário.
    """

    text = ("Este é um bot foi desenvolvido para receber audios e devolver a transcrição do texto\n"
            "Este projeto ainda está em desenvolvimento.\n"
            "\nDesenvolvido por: Ed Carlos Bicudo."
            "\ned.carlos.bicudo@pm.me")

    bot.reply_to(message, text).wait()


@bot.message_handler(content_types=['voice'])
def recebe_audio(message):
    """Recebe um 'voice' do Telegram e retorna a mensagem em texto.

    Args:
        message (Message): Mensagem recebida do usuário.
    """

    file_info = bot.get_file(message.voice.file_id).wait()

    file_name = file_info.file_path.split('/')[1]

    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(tokens.BOT_TOKEN, file_info.file_path))

    audio = converter_audio(file_name, file)

    response = extrair_texto(audio)

    esvaziar_pasta()

    bot.reply_to(message, response).wait()


def converter_audio(file_name, file):
    """Converte o audio recebido do Telegram em formato ogg para wav.

    Args:
        file_name (String): Nome do arquivo de audio
        file (Raw): Conteúdo do arquivo

    Returns:
        Path: Caminho do arquivo convertido.
    """
    if not os.path.exists(pasta_de_audio):
        os.makedirs(pasta_de_audio)

    path_ogg = os.path.join(pasta_de_audio, f"{file_name}.ogg")
    path_wav = os.path.join(pasta_de_audio, f"{file_name}.wav")

    with open(path_ogg, 'wb') as f:
        f.write(file.content)

    sound = AudioSegment.from_ogg(path_ogg)
    sound.export(path_wav, format="wav")

    return path_wav


def esvaziar_pasta():
    """Excluí todos os arquivos da pasta 'audio'
    """

    for filename in os.listdir(pasta_de_audio):
        file_path = os.path.join(pasta_de_audio, filename)

        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def extrair_texto(audio):
    """Envia o audio para a Engine do Google converter em texto.

    Args:
        audio (Path): Caminho do arquivo de audio

    Returns:
        String: Texto extraído do audio
    """

    with sr.AudioFile(audio) as source:

        audio_data = r.record(source)

        try:
            text = r.recognize_google(audio_data,language='pt-BR')
        except sr.UnknownValueError:
            text = "Texto não entendido"

        return text


if __name__ == "__main__":

    while True:
        try:
            bot.polling()
        except Exception as error:
            print(error)

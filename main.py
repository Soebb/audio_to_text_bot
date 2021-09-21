import tokens
import telebot
import requests
import pretty_errors

bot = telebot.AsyncTeleBot(tokens.BOT_TOKEN)

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

    file_info = bot.get_file(message.voice.file_id).wait()

    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(tokens.BOT_TOKEN, file_info.file_path))

    bot.reply_to(message, "Ainda em desenvolvimento").wait()

if __name__ == "__main__":

    while True:
        try:
            bot.polling()
        except Exception as error:
            print(error)

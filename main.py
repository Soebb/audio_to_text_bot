import tokens
import telebot
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

if __name__ == "__main__":

    while True:
        try:
            bot.polling()
        except Exception as error:
            print(f"Bot Caiu: {str(error)}")

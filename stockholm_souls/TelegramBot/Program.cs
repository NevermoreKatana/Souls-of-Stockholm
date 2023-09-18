using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Telegram.Bot;
using Telegram.Bot.Types;
using Telegram.Bot.Types.ReplyMarkups;

namespace Telegram
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string Token = "6477258940:AAGieZaJCnuVhna1AcX8pBMdcL2wM9N5Ilc";
            var client = new TelegramBotClient(Token);
            client.StartReceiving(Update, Error);
            var me = client.GetMeAsync().Result;

            Console.WriteLine($"Start listening for @{me.Username}");
            Console.ReadLine();

        }

        async static Task Update(ITelegramBotClient botClient, Update update, CancellationToken token)
        {
            var message = update.Message;
            Console.WriteLine($"{message.From.FirstName}{message.From.LastName} : {message.Text}");
            if (message.Text != null)
            {
                if (message.Text == "/start")
                {
                    await botClient.SendTextMessageAsync(message.Chat.Id, $"Welcome home, {message.From.FirstName}{message.From.LastName}!", replyMarkup: GetButton());
                    return;
                }
                switch (message.Text)
                {
                    case "Первый":
                        await botClient.SendTextMessageAsync(message.Chat.Id, "А может второй?");
                        break;
                    case "Второй":
                        await botClient.SendTextMessageAsync(message.Chat.Id, "А может третий?");
                        break;
                    case "Третий":
                        await botClient.SendTextMessageAsync(message.Chat.Id, "А может четвертый?");
                        break;
                    case "Четвертый":
                        await botClient.SendTextMessageAsync(message.Chat.Id, "А может теперь нахуй пойдешь?");
                        break;

                    default:
                        await botClient.SendTextMessageAsync(message.Chat.Id, "Выбери команду: ", replyMarkup: GetButton());
                        break;
                }
            }

        }

        private static IReplyMarkup GetButton()
        {
            var keyboard = new ReplyKeyboardMarkup(
                new List<List<KeyboardButton>>
                {
                    new List<KeyboardButton> { new KeyboardButton("Первый"), new KeyboardButton("Второй") },
                    new List<KeyboardButton> { new KeyboardButton("Третий"), new KeyboardButton("Четвертый") }
                }
            );

            return keyboard;

        }

        private static Task Error(ITelegramBotClient arg1, Exception arg2, CancellationToken arg3)
        {
            throw new NotImplementedException();
        }
    }
}

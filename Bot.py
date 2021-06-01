import handlers
import settings
from pony.orm import *
import time
from csv_exam import make_model
from main import get_class_of_email
from settings import *
import re
import imaplib
import pandas as pd
from imapclient import imap_utf7
import logging
import init_db



log = logging.getLogger('SortLog')


def logconfig():
    """
    Конфигурация логгера
    :return:
    """
    stream_logger = logging.StreamHandler()
    stream_logger.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    stream_logger.setLevel(logging.DEBUG)
    log.addHandler(stream_logger)

    filehandler = logging.FileHandler(LOG_FILE_NAME, 'a', 'utf-8')
    formatter = logging.Formatter(LOG_FORMAT)
    formatter.datefmt = '%d-%m-%Y %H:%M'
    filehandler.setLevel(logging.DEBUG)
    # все возможные аттрибуты см https://docs.python.org/3.5/library/logging.html#logrecord-attributes
    filehandler.setFormatter(formatter)
    log.addHandler(filehandler)
    log.setLevel(logging.DEBUG)
    #logging.basicConfig(handlers=(filehandler, stream_logger))



pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')

class Bot:
    def parse_uid(self,data):
        match = pattern_uid.match(data)
        return match.group('uid')


    def run(self):
        # запуск разбора писем

        mail = imaplib.IMAP4_SSL('imap.mail.ru')
        mail.login(user, password)
        log.debug('Connect to imap server')
        mail.list()
        mail.select('inbox')
        status, response = mail.uid('search', None, 'UNSEEN')
        if status == "OK":
            unread_msg_nums = response[0].split()
        else:
            unread_msg_nums = []


        train_csv = pd.read_csv('Classyfy_.csv', sep=';')
        text_clf = make_model(train_csv)

        try:
           last = init_db.EmailState[1]

        except BaseException as er:
            with db_session:
                last = init_db.EmailState(last_email=0)
            init_db.db.commit()

        last_email_index = max(0, last.last_email)

        for item in unread_msg_nums:
            if int(item) > last_email_index:
                predicted, email = get_class_of_email(item, mail, text_clf)

                mail.uid("store",item,'-FLAGS', '(\Seen)')
                self.sort_post(item, predicted,mail)
                with db_session:
                    init_db.EmailState[1].last_email = int(item)

                    try:
                        n_class = init_db.Class_of_mail.get(name_of_class=predicted[0])
                        n_class.count_of_emails += 1
                        init_db.db.commit()
                    except BaseException:
                        n_class = init_db.Class_of_mail(name_of_class = predicted[0], count_of_emails=1)
                        log.debug(f'Class: {predicted[0]}, was added')
                        init_db.db.commit()



                init_db.db.commit()
                log.debug(f'Post form: {email}, item:{int(item)}, Class: {predicted[0]} ')



    def sort_post(self,item, predicted, mail):
        if predicted:
            name = f'"{predicted[0]}"'
            folder = imap_utf7.encode(name)
            rv, folders = mail.list()
            list_of_folders = [imap_utf7.decode(x).split(' "/" ')[1] for x in folders]
            if name not in list_of_folders:
                mail.create(f'"{predicted[0]}"'.encode('utf-8'))
            else:
                i = list_of_folders.index(name)
                direct = folders[i]

            self.move_post(folder, item, mail)

    def move_post(self, folder, item, mail):
        res_copy = mail.uid('COPY', item, folder)
        if res_copy[0] == 'OK':
            mail.uid('STORE', item, '+FLAGS', '\\Deleted')
            #mail.store(item, '+FLAGS', '\\Deleted')
            mail.expunge()

    def on_event(self,predicted, email):
        #новое письмо пришло начинаем его разбор

        #state = UserState.get(user_id=str(email)) # найти в БД бота данные о пользовтеле
        state = None# {'user_id':'pupkin_vad@mail.ru'}
        # если данные есть продолжам сценарий с ним
        if state is not None:
            self.continue_scenario(state=state)
        else: # если данных нет, то запускаем сценарий
            if predicted:
                predicted = predicted[0]
                scenario_name = settings.SCENARIOS[predicted]
                self.start_scenario(user_id=email,scenario_name=scenario_name)
                #работа с классифицированным письмом
            else:
                #класс письма не определен, необходимо перемещать письмо в директорию неотсортированные
                pass
            for intent in settings.INTENTS:

                if any(token in text.lower() for token in intent['tokens']):
                    #log.debug(f'User {user_id} получил {intent}')
                    if intent['answer']:
                        pass
                        #self.send_text(email, intent['answer'], user_id)
                    else:
                        pass
                        #self.start_scenario(user_id=str(email), scenario_name=intent['scenario'], event=event)
                    break
            else:
                """"
                pass#self.send_text(email, settings.DEFAULT_ANSWER, user_id)
            """
    def start_scenario(self, user_id, scenario_name):
        #старт сценария работы с пользователем
        first_step = scenario_name['first_step']
        step = scenario_name['steps'][first_step]
        handler = step['handler']
        handle = getattr(handlers,handler)
        if handle(user_id):
            # хандлер должен возвращать решение проблемы, подготовленное письмо с ответом, со ссылками
            pass
        else:
            pass
            # если ни чего не вернул, тогда отправляем письмо поьзователю с уточнением проблемы, тоже может возвращаться из хандлера

        #UserState(user_id=user_id, scenario_name=scenario_name, step_name=first_step, context={})

    def continue_scenario(self, state):
        #продолжене работы по сценарию
        pass
        #handler = getattr(handlers, step['handler'])



if __name__ == '__main__':
    logconfig()
    bot = Bot()
    while True:
        bot.run()
        time.sleep(10)



#server settings
server = 'smtp.mail.ru'
#user = 
#password =
#user = 
#password = 

user = 
password = 
sender = 'example@mail.ru'
subject = 'Тема сообщения'
text = 'Текст сообщения'
html = '<html><head></head><body><p>'+text+'</p></body></html>'


LOG_FILE_NAME = 'sort.log'
LOG_FORMAT = '%(asctime)s : %(levelname)s - %(message)s'
#DB_CONFIG = {"provider": 'postgres', "user": 'postgres', "password": '123456', "host": 'localhost',
#             "database": "db_bot_states"}
DB_CONFIG  = {'provider': 'sqlite', 'filename':'database.sqlite', 'create_db':'True'}
#post classyfying
#темы и категории писем

droped_emails = ['no_reply@free-lance.ru',
                     'info@r.molodost.bz',
                     'info@jivosite.com',
                     'info@emailstream.ru',
                     'donotreplyconsumer.relations@gsk.com',
                     'mailer-daemon@corp.mail.ru',
                     'info@pedsovet.su',
                     'notification@russianpost.ru',
                     'alert@uptimerobot.com',
                     'mzs@r.molodost.bz',
                     'support@miran.ru',
                     'no_reply@free-lance.ru',
                     'support@sendpulse.com',
                     'mailer-daemon@googlemail.com',
                     'noreply.otpravka@russianpost.ru',
                     'info@vitvet.com',
                     'open@garant.ru',
                     'info@seoslon.com',
                     'serafim@rzdtour.com',
                     'mihail.dashkiev@r.molodost.bz',
                     'petr.osipov@r.molodost.bz',
                     'noreply@hypercomments.com']

#ключевые слова для классификаторов

INTENTS = [
    {
        'name':'Потеря диплома',
        'token': 'Потеря диплома',
        "scenario": 'Потеря диплома',
        'answer': None
    }
]

SCENARIOS ={
    'Потеря диплома':
        {
            'first_step': 'step1',
            'steps':
                {
                    'step1':
                        {
                        "text": ":Жаль что так получилось,мы уже работаем над этим. Спасибо за обращение. "
                                "В ближайшее время все поправим.",
                        "failure_text": "Уточните пожалуста, какая почта использовалась при совершении оплаты?",
                        "handler": "handle_diplom_failure",
                        "next_step": "step2"
                        }
                }
        }
}

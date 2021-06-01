from pony.orm import *
import settings


db = Database()
db.bind(settings.DB_CONFIG)


#текущее состояние юзера
class UserState(db.Entity):
    user_id = Required(str, unique=True)
    scenario_name = Required(str) # название сценария куда папл юзер
    step_name = Required(str) #текущий шаг, на котором находится юзер
    context = Required(Json)


#номер последнего обработанного письма. храниться в БД
class EmailState(db.Entity):
    last_email=Required(int)

class Class_of_mail(db.Entity):
    name_of_class = Required(str) #название класса
    count_of_emails = Required(int)

db.generate_mapping(create_tables=True)

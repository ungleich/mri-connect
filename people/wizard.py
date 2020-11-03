import data_wizard
from .models import Person, Expertise, Topic

data_wizard.register(Person)
data_wizard.register(Expertise)
data_wizard.register(Topic)

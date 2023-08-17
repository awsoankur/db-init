from faker.providers import BaseProvider
import faker as f
from random import randint,choices
from datetime import datetime,date

# default faker to use in all the Providers
faker = f.Faker("en_IN")

"""
A Provider for the column faker must follow the following template:

class NewProvider(BaseProvider):
    def fake(self,column):
        return "i am fake"

Each provider must be added to different faker, so create a new faker 

new_faker = faker.Faker("en.IN")
new_faker.add_provider(NewProvider)
"""

class PhoneProvider(BaseProvider):
    def fake(self,column)-> str:
        phone ="+91"
        phone = phone + str(randint(1,10))
        phone = phone + faker.bothify(text="#########")
        return phone
    def name(self):
        return "phone_faker"

class BankProvider(BaseProvider):
    def fake(self,column) -> str :
        if "ifsc" in column:
            return faker.bothify(text="????#######")
        elif "amount" in column:
            return float(faker.bothify(text="####.##"))
        elif "vpa" in column or "upi" in column:
            return faker.bothify(text="?????##@upi")
        elif "va" in column:
            return faker.bothify(text="???#############")
        elif "imei" in column:
            return faker.bothify(text="###############")
        elif "gender" in column:
            gender = ["male","female","not specified"]
            return gender[randint(0,2)]
        elif "number" in column:
            return faker.bothify(text="#"*13)
        elif "utr" in column:
            return faker.bothify(text="#"*16)
    def name(self):
        return "bank_faker"

class DateProvder(BaseProvider):
    def fake(self,column):
        if "date" in column:
            return date.today()
        return datetime.now()
    def name(self):
        return "date_faker"

class UrlProvider(BaseProvider):
    def fake(self,column) -> str:
        return faker.bothify(text="www.??????.com/???###??#?#?")
    def name(self):
        return "url_faker"

class IdProvider(BaseProvider):
    def fake(self,column) -> str:
        if "ids" in column:
            return self.fake("")+","+self.fake("")
        return faker.bothify(text="".join(choices(["#","?"],k=randint(8,12))))
    def name(self):
        return "id_faker"

class NameProvider(BaseProvider):
    def fake(self,column):
        return faker.name()
    def name(self):
        return "name_faker"

class FloatProvider(BaseProvider):
    def fake(self,column):
        return float(faker.bothify(text="####.##"))
    def name(self):
        return "float_faker"


# Define all base fakers
phone_faker = f.Faker("en_IN")
bank_faker = f.Faker("en_IN")
date_faker = f.Faker("en_IN")
url_faker = f.Faker("en_IN")
id_faker = f.Faker("en_IN")
name_faker = f.Faker("en_in")
float_faker = f.Faker("en_IN")

# Add corresponding providers to each faker
# Each provider must have a method "fake" which returns the required value

phone_faker.add_provider(PhoneProvider)
bank_faker.add_provider(BankProvider)
date_faker.add_provider(DateProvder)
url_faker.add_provider(UrlProvider)
id_faker.add_provider(IdProvider)
name_faker.add_provider(NameProvider)
float_faker.add_provider(FloatProvider)

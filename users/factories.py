import factory
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")

    @factory.post_generation
    def password(self, create, extracted):
        if not create or not extracted:
            return

        self.set_password(extracted)

    class Meta:
        model = User

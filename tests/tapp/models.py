from django.db import models

from encrypted_id.models import EncryptedIDModel, EncryptedIDManager


class Foo(EncryptedIDModel):
    text = models.TextField()


class Foo2Manager(EncryptedIDManager):
    pass


class Foo2(EncryptedIDModel):
    text = models.TextField()

from django.db import models
from django.db.models import options

from encrypted_id import EncryptedIDDecodeError
from encrypted_id import encode, decode, get_object_or_404, get_model_sub_key

options.DEFAULT_NAMES += ("ek_key",)


class EncryptedIDManager(models.Manager):
    def get_by_ekey(self, ekey, **kwargs):
        return self.get(id=decode(ekey, get_model_sub_key(self.model)), **kwargs)

    def get_by_ekey_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)


class EncryptedIDQuerySet(models.QuerySet):
    def filter(self, *args, **kwargs):
        if "ekey" in kwargs:
            ekey = kwargs.pop("ekey")
            try:
                assert ekey is not None
                kwargs["id"] = decode(ekey, get_model_sub_key(self.model))
            except (AssertionError, EncryptedIDDecodeError):
                return self.none()
        return super(EncryptedIDQuerySet, self).filter(*args, **kwargs)


class EncryptedIDModel(models.Model):
    class Meta:
        abstract = True

    objects = EncryptedIDManager.from_queryset(EncryptedIDQuerySet)()

    @property
    def ekey(self):
        return encode(self.id, get_model_sub_key(self))

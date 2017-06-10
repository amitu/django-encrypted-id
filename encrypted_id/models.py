# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db import models
from django.db.models import options

from encrypted_id import EncryptedIDDecodeError
from encrypted_id import encode, decode, get_object_or_404, get_model_sub_key

options.DEFAULT_NAMES += ('ek_key',)


class EncryptedIDManager(models.Manager):
    def get_by_ekey(self, ekey, **kw):
        return self.get(id=decode(ekey, get_model_sub_key(self.model)), **kw)

    def get_by_ekey_or_404(self, *args, **kw):
        return get_object_or_404(self.model, *args, **kw)


class EncryptedIDQuerySet(models.QuerySet):
    def filter(self, *args, **kw):
        if 'ekey' in kw:
            ekey = kw.pop('ekey')
            try:
                assert ekey is not None
                kw['id'] = decode(ekey, get_model_sub_key(self.model))
            except (AssertionError, EncryptedIDDecodeError):
                return self.none()
        return super(EncryptedIDQuerySet, self).filter(*args, **kw)


class EncryptedIDModel(models.Model):
    class Meta:
        abstract = True

    objects = EncryptedIDManager.from_queryset(EncryptedIDQuerySet)()

    @property
    def ekey(self):
        return encode(self.id, get_model_sub_key(self))

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db import models

from encrypted_id import encode, decode, get_object_or_404


class EncryptedIDManager(models.Manager):
    def get_by_ekey(self, ekey, **kw):
        return self.get(id=decode(ekey), **kw)

    def get_by_ekey_or_404(self, *args, **kw):
        return get_object_or_404(self.model, *args, **kw)


class EncryptedIDModel(models.Model):
    class Meta:
        abstract = True

    objects = EncryptedIDManager()

    @property
    def ekey(self):
        return encode(self.id)

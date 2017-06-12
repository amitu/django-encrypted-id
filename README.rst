django-encrypted-id
===================

**Note**: Version 0.2.0 is a breaking change from versions
`0.1.x <https://github.com/amitu/django-encrypted-id/tree/v0.1>`_.
If you've been using *ekey* in permalinks, then it is recommended for you to
not upgrade to 0.2.x.

----

Consider this example model:

.. code-block:: python

    from django.db import models

    from encrypted_id.models import EncryptedIDModel


    class Foo(EncryptedIDModel):
        text = models.TextField()


By inheriting from ``EncryptedIDModel``, you get .ekey as a property on your
model instances. This is how they will look like:

.. code-block:: python

    In [1]: from tapp.models import Foo

    In [2]: f = Foo.objects.create(text="asd")

    In [3]: f.id
    Out[3]: 1

    In [4]: f.ekey
    Out[4]: 'bxuZXwM4NdgGauVWR-ueUA'
    You can do reverse lookup:

    In [5]: from encrypted_id import decode

    In [6]: decode(f.ekey)
    Out[6]: 1

If you can not inherit from the helper base class, no problem, you can just use
the ``ekey()`` function from ``encrypted_id`` package:

.. code-block:: python

    In [7]: from encrypted_id import ekey

    In [8]: from django.contrib.auth.models import User

    In [9]: ekey(User.objects.get(pk=1))
    Out[9]: 'bxuZXwM4NdgGauVWR-ueUA'


To do the reverse lookup, you have two helpers available. First is provided by
``EncryptedIDManager``, which is used by default if you inherit from
``EncryptedIDModel``, and have not overwritten the ``.objects``:

.. code-block:: python

    In [10]: Foo.objects.get_by_ekey(f.ekey)
    Out[10]: <Foo: Foo object>


But sometimes you will prefer the form:

.. code-block:: python

    In [11]: Foo.objects.get_by_ekey_or_404(f.ekey)
    Out[11]: <Foo: Foo object>


Which works the same, but instead of raising ``DoesNotExist``, it raises
``Http404``, so it can be used in views.

You your manager is not inheriting from ``EncryptedIDManager``, you can use:

.. code-block:: python

    In [12]: e = ekey(User.objects.first())

    In [13]: e
    Out[13]: 'bxuZXwM4NdgGauVWR-ueUA'

    In [14]: get_object_or_404(User, e)
    Out[14]: <User: amitu>


``encrypted_id.get_object_or_404``, as well as
``EncryptedIDManager.get_by_ekey`` and
``EncryptedIDManager.get_by_ekey_or_404`` take extra keyword argument, that can
be used to filter if you want.

If you are curios, the regex used to match the generated ids is:

.. code-block:: python

    "[0-9a-zA-Z-_]+"


If you are using `smarturls <http://amitu.com/smarturls/>`_, you can use URL
pattern like:

.. code-block:: python

    "/<ekey:foo>/"


I recommend this usage of encrypted-id over UUID, as UUIDs have significant
issues that should be considered (tldr: they take more space on disk and RAM,
and have inferior indexing than integer ids), and if your goal is simply to
make URLs non guessable, encrypted id is a superior approach.

If you are curious about the encryption used: I am using ``AES``, from
``pycrypto`` library, and am using ``SECRET_KEY`` for password
(``SECRET_KEY[:32]``) and ``IV`` (first 16 characters of hash of ``SECRET_KEY``
and a *sub_key*), in the ``AES.CBC`` mode. The *sub_key* is taken from the
model's ``Meta`` attribute ``ek_key``, or simply ``db_table`` if ``ek_key`` is
not set.

In general it is recommended not to have static ``IV``, but ``CBC`` offsets
some of the problems with having static IV.  What is the the issue with static
IV you ask: if plain text "abc" and "abe" are encrypted, the first two bytes
would be same.  Now this does not present a serious problem for us, as the
plain text that I am encrypting uses ``CRC32`` in the beginning of payload, so
even if you have ids, 1, 11, an attacker can not say they both start with same
first character.

The library also supports the scenario that you have to cycle ``SECRET_KEY``
due to some reason, so URLs encrypted with older ``SECRET_KEY`` can still be
decoded after you have changed it (as long as you store old versions in
``SECRET_KEYS`` setting).  In order to decrypt the library tries each secret
key, and compares the ``CRC32`` of data to know for sure (as sure as things get
in such things), that we have decrypted properly.

Do feel free to raise an issue here, if you face any issues, I would be happy
to help. The library supports both python 2.7 and 3.5, as well as it all
versions of django that django team supports.


import binascii
from cryptography.fernet import Fernet, InvalidToken, MultiFernet

from django.conf import settings
from django.core.exceptions import FieldError, ImproperlyConfigured
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.functional import cached_property

from .utils import force_text
from . import hkdf


__all__ = [
    'EncryptedField',
    'EncryptedTextField',
    'EncryptedCharField',
    'EncryptedEmailField',
    'EncryptedIntegerField',
    'EncryptedDateField',
    'EncryptedDateTimeField',
    'EncryptedBinaryField',
]


class EncryptedField(models.Field):
    """A field that encrypts values using Fernet symmetric encryption."""
    _internal_type = 'BinaryField'

    def __init__(self, *args, **kwargs):
        if kwargs.get('primary_key'):
            raise ImproperlyConfigured(
                "%s does not support primary_key=True."
                % self.__class__.__name__
            )
        if kwargs.get('unique'):
            raise ImproperlyConfigured(
                "%s does not support unique=True."
                % self.__class__.__name__
            )
        if kwargs.get('db_index'):
            raise ImproperlyConfigured(
                "%s does not support db_index=True."
                % self.__class__.__name__
            )
        super(EncryptedField, self).__init__(*args, **kwargs)

    @cached_property
    def keys(self):
        keys = getattr(settings, 'FERNET_KEYS', None)
        if keys is None:
            keys = [settings.SECRET_KEY]
        return keys

    @cached_property
    def fernet_keys(self):
        if getattr(settings, 'FERNET_USE_HKDF', True):
            return [hkdf.derive_fernet_key(k) for k in self.keys]
        return self.keys

    @cached_property
    def fernet(self):
        if len(self.fernet_keys) == 1:
            return Fernet(self.fernet_keys[0])
        return MultiFernet([Fernet(k) for k in self.fernet_keys])

    def get_internal_type(self):
        return self._internal_type

    def get_db_prep_save(self, value, connection):
        value = super(
            EncryptedField, self
        ).get_db_prep_save(value, connection)
        if value is not None:
            retval = self.fernet.encrypt(force_bytes(value))
            return connection.Database.Binary(retval)

    def from_db_value(self, value, expression, connection, *args):
        if value is None:
            return

        value = bytes(value)
        try:
            decrypted = self.fernet.decrypt(value)
        except InvalidToken:
            message = [f'Could not decrypt {value}']
            if getattr(settings, 'FERNET_KEYS', None):
                message.append('with an FERNET_KEYS, are you missing one?')
            else:
                message.append(
                    'with SECRET_KEY, has another process written data with a'
                    'different SECRET_KEY? See documentation about Keys for'
                    'details'
                )
            raise Exception(' '.join(message))
        return self.to_python(force_text(decrypted))

    @cached_property
    def validators(self):
        # Temporarily pretend to be whatever type of field we're masquerading
        # as, for purposes of constructing validators (needed for
        # IntegerField and subclasses).
        self.__dict__['_internal_type'] = super(
            EncryptedField, self
        ).get_internal_type()
        try:
            return super(EncryptedField, self).validators
        finally:
            del self.__dict__['_internal_type']


def get_prep_lookup(self):
    """Raise errors for unsupported lookups"""
    raise FieldError("{} '{}' does not support lookups".format(
        self.lhs.field.__class__.__name__, self.lookup_name))


# Register all field lookups (except 'isnull') to our handler
for name, lookup in models.Field.class_lookups.items():
    # Dynamically create classes that inherit from the right lookups
    if name != 'isnull':
        lookup_class = type('EncryptedField' + name, (lookup,), {
            'get_prep_lookup': get_prep_lookup
        })
        EncryptedField.register_lookup(lookup_class)


class EncryptedTextField(EncryptedField, models.TextField):
    pass


class EncryptedCharField(EncryptedField, models.CharField):
    pass


class EncryptedEmailField(EncryptedField, models.EmailField):
    pass


class EncryptedIntegerField(EncryptedField, models.IntegerField):
    pass


class EncryptedDateField(EncryptedField, models.DateField):
    pass


class EncryptedDateTimeField(EncryptedField, models.DateTimeField):
    pass


class EncryptedBinaryField(EncryptedField, models.TextField):
    """
    We're going to use Python's binascii module to deal with binary data.
    """

    def get_db_prep_save(self, value, connection):
        if value:
            value = binascii.b2a_base64(value)
        return super().get_db_prep_save(
            value,
            connection,
        )

    def from_db_value(self, value, expression, connection, *args):
        if value is not None:
            value = binascii.a2b_base64(bytes(value))
            breakpoint()
            return self.to_python(self.fernet.decrypt(value))

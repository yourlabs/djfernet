Changelog
=========

master
------

- Add support for Django 3.2, 4.1 & 4.2
- Add support for Python 3.8, 3.9, 3.10 & 3.11
- Drop support for Django 1.11, 2.1, 2.2 & 3.0
- Drop support for Python 2.7, 3.5, 3.6 & 3.7
- Shifted CI from travis/gitlab to github actions


0.8.0
-----

Switched back to django-fernet-fields for default salt, making it incompatible
with 0.7.4! But, compatible with django-fernet-fields, so that you can migrate
easily if you haven't already.

If, unfortunnately, you have already deployed this in production, you have two
options:

- re-encrypt your data to use django-fernet-fields instead of djfernet,
- or set settings.DJFERNET_PREFIX=djfernet to keep going

Sorry about this laborious releases.

Also, added EncryptedBinaryField.

0.7.4
-----

First release since fork. Unfortunnately, my sed
s/django-fernet-fields/djfernet/ caused a change in the salt, make it
impossible to decrypt existing data!!

Added settings.DJFERNET_PREFIX to set it to django-fernet-fields and make it
compatible again through a setting.

Thanks to @sevdog for the report.

0.6 (2019.05.10)
----------------

* Support Postgres 10
* Drop support for Django < 1.11, Python 3.3/3.4
* Add support for Django 1.11 through 2.2, Python 3.7

0.5 (2017.02.22)
----------------

* Support Django 1.10.

0.4 (2015.09.18)
----------------

* Add `isnull` lookup.


0.3 (2015.05.29)
----------------

* Remove DualField and HashField. The only cases where they are useful, they
  aren't secure.


0.2.1 (2015.05.28)
------------------

* Fix issue getting IntegerField validators.


0.2 (2015.05.28)
----------------

* Extract HashField for advanced lookup needs.


0.1 (2015.05.27)
----------------

* Initial working version.

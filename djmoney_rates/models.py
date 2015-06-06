from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.core.cache import cache


class CacheManager(models.Manager):
    def get(self, *args, **kwargs):
        prefix = '{0}:{1}:'.format(self.model._meta.app_label, self.model._meta.model_name)
        if 'source' in kwargs:
            kwargs['source_id'] = kwargs.pop('source').id
        keys = ':'.join([
            '{0}={1}'.format(k[0], k[1]) for k in sorted(kwargs.items(), key=lambda t: t[0])])

        rate = cache.get(prefix+keys)
        if not rate:
            rate = super(CacheManager, self).get(*args, **kwargs)
            cache.set(prefix+keys, rate)
        return rate


@python_2_unicode_compatible
class RateSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    last_update = models.DateTimeField(auto_now=True)
    base_currency = models.CharField(max_length=3)

    objects = CacheManager()

    def __str__(self):
        return _("%s rates in %s update %s") % (
            self.name, self.base_currency, self.last_update)


@python_2_unicode_compatible
class Rate(models.Model):
    source = models.ForeignKey(RateSource)
    currency = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=20, decimal_places=6)

    objects = CacheManager()

    class Meta:
        unique_together = ('source', 'currency')

    def __str__(self):
        return _("%s at %.6f") % (self.currency, self.value)

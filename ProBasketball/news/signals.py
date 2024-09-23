from django.db.models import Model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import unique_slugify


def autoslug_by(field: str):
    def wrapper(model: Model):
        # some sanity checks first
        error = f'The {model.__name__} model has no {field!r} field'
        assert hasattr(model, field), error

        is_field_unique = model._meta.get_field(field).unique

        @receiver(pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw: bool = False, **kwargs):
            source = getattr(instance, field)

            if not raw and not source: return

            value = model.__name__ if is_field_unique else source

            return unique_slugify(instance, value, inplace=True)

        return model

    return wrapper

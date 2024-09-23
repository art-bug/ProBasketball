from itertools import count
import re

from slugify import slugify


SLUG_SEPARATOR = '-'


def unique_slugify(instance, value: str, slug_field_name: str = 'slug',
                   slug_sep: str = SLUG_SEPARATOR,
                   inplace: bool = False,
                   queryset=None):
    '''
    Based on https://djangosnippets.org/snippets/690

    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    '''

    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)

    if slug_len:
        slug = slug[:slug_len]

    slug = _slug_combing(slug, slug_sep)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    queryset = queryset or instance.__class__._default_manager.all()
    queryset = queryset.exclude(pk=instance.pk) if instance.pk else queryset

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    counter = count(start=2)

    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = f'{slug_sep}{next(counter)}'

        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_combing(slug, slug_sep)

        slug = f'{slug}{end}'

    if inplace:
        return setattr(instance, slug_field.attname, slug)

    return slug


def _slug_combing(slug: str, sep: str = SLUG_SEPARATOR):
    '''
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    '''

    sep = sep or ''

    # Remove separator from the beginning and end of the slug.
    stripped = slug.strip(fr'{SLUG_SEPARATOR}{sep}')

    # Remove multiple instances and if an alternate separator is provided,
    # replace the default separator.
    pattern = f'[{SLUG_SEPARATOR}{re.escape(sep)}]+'

    return re.sub(pattern, sep, stripped)

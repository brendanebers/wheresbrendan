"""Helpful functions for working with models."""


def AsDict(obj, only=None, skip=None):
    """Return a dict of a row of data using attributes from the model class.

    Args:
        obj: The object to return as a dictionary.
        only: Optional list of fields that should be used in the dictionary.
        skip: Optional list of fields that should be skipped.
    """
    skip = list(skip) if skip else []
    return dict([
        (name, getattr(obj, name))
        for name in dir(obj.__class__) if _IsField(name, only, skip)])


def RowsAsDicts(rows, only=None, skip=None):
    """Return a list of dicts of data; see AsDict above."""
    return [AsDict(row, only=only, skip=skip) for row in rows]


def _IsField(name, only, skip):
    if only:
        return name in only
    invalid_fields = ['query', 'metadata', 'query_class'] + skip
    return name[0].islower() and name not in invalid_fields

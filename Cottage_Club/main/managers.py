from treebeard.al_tree import AL_NodeManager
from eav.managers import BaseEntityManager
from django.db import models
from django.contrib.contenttypes.models import ContentType


def _pop_data_from_kwargs(kwargs):
    ct_field = kwargs.pop('ct_field', 'content_type')
    fk_field = kwargs.pop('fk_field', 'object_id')
    return ct_field, fk_field


class CottageManager(AL_NodeManager, BaseEntityManager):
    pass


class GenericModelManager(models.Manager):
    """ Manager with for_model method.  """

    def __init__(self, *args, **kwargs):
        self.ct_field, self.fk_field = _pop_data_from_kwargs(kwargs)
        super(GenericModelManager, self).__init__(*args, **kwargs)

    def for_model(self, model, content_type=None):
        """ Returns all objects that are attached to given model """
        content_type = content_type or ContentType.objects.get_for_model(model)
        kwargs = {
            self.ct_field: content_type,
            self.fk_field: model.pk
        }
        objects = self.get_query_set().filter(**kwargs)
        return objects


class AttachedImageManager(GenericModelManager):
    """ Manager with helpful functions for attached images
    """
    def get_for_model(self, model):
        """ Returns all images that are attached to given model.
            Deprecated. Use `for_model` instead.
        """
        return self.for_model(model)

    def get_main_for(self, model):
        """
        Returns main image for given model
        """
        try:
            return self.for_model(model).get(is_main=True)
        except models.ObjectDoesNotExist:
            return None
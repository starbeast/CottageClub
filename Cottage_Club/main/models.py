# coding=utf-8
import os
import unidecode

from eav.models import BaseAttribute, BaseSchema, BaseChoice, BaseEntity

from tinymce.models import HTMLField

from treebeard.ns_tree import NS_Node
from treebeard.al_tree import AL_Node
from mptt.models import MPTTModel, TreeForeignKey

from django.core.files.storage import FileSystemStorage as OverwriteStorage

from autoslug.fields import AutoSlugField
from Cottage_Club.main.utils import slugify

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from Cottage_Club.main.injectors import GenericInjector
from Cottage_Club.main.signals import image_deleted, image_saved
from Cottage_Club.main.managers import CottageManager, AttachedImageManager, GenericModelManager

Max = models.Max
# Create your models here.


def slugify_attr_name(name):
    return unidecode.unidecode(slugify((name.replace('_', '-')).replace('-', '_')))


def get_entity_lookups(entity):
    ctype = ContentType.objects.get_for_model(entity)
    return {'entity_type': ctype, 'entity_id': entity.pk}


class Schema(BaseSchema):
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def _save_single_attr(self, entity, value=None, schema=None,
                          create_nulls=False, extra={}):
        schema = schema or self
        lookups = dict(get_entity_lookups(entity), schema=schema, **extra)
        try:
            attr = self.attrs.get(**lookups)
        except self.attrs.model.DoesNotExist:
            attr = self.attrs.model(**lookups)
        if create_nulls or value != attr.value:
            if schema.datatype == Schema.TYPE_BOOLEAN:
                if value is False and entity.is_parent:
                    pass
            attr.value = value
            for k, v in extra.items():
                setattr(attr, k, v)
            attr.save()


class MpttTest(MPTTModel):
    name = models.CharField(max_length=30)
    schemas = models.ManyToManyField(Schema, through='SchemaForMpttTest', related_name='mptts')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


class Category(NS_Node):
    name = models.CharField(max_length=30)
    is_separator = models.BooleanField(_("Is separator"), default=False)
    schemas = models.ManyToManyField(Schema, through='SchemaForCategory', related_name='categories')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Choice(BaseChoice):
    schema = models.ForeignKey(Schema, related_name='choices', limit_choices_to={'datatype__in': [BaseSchema.TYPE_MANY, BaseSchema.TYPE_ONE]})


class Attribute(BaseAttribute):
    schema = models.ForeignKey(Schema, related_name='attrs')
    choice = models.ForeignKey(Choice, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    is_separator = models.BooleanField(_('Will be a separator'), default=False)
    order = models.IntegerField(_('Order in the list'), default=0)

    def __unicode__(self):
        return self.schema.title or self.schema.name

    class Meta:
        verbose_name = _('Attribute value')
        verbose_name_plural = _('Attribute values')


class Cottage(BaseEntity, AL_Node):

    PARENT, CHILD = 'parent', 'child'
    STRUCTURE_CHOICES = (
        (PARENT, _('Parent object')),
        (CHILD, _('Inner object'))
    )
    objects = CottageManager()
    attrs = generic.GenericRelation(Attribute, object_id_field='entity_id',
                                    content_type_field='entity_type')
    category = models.ForeignKey(
        Category
        , blank=True
        , null=True
        , help_text=_("leave blank if this is not a parent object"))
    images = generic.GenericRelation('Image')
    structure = models.CharField(
        _("Object structure"), max_length=10, choices=STRUCTURE_CHOICES,
        default=PARENT)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        verbose_name=_("Parent object"))
    sib_order = models.PositiveIntegerField(default=0)
    title = models.CharField(_('Object title'),
                             max_length=255, blank=False)
    slug = AutoSlugField(max_length=250, populate_from='title', unique_with='category',
                         editable=True, blank=True, slugify=slugify_attr_name)
    minimal_price = models.IntegerField(default=0, blank=False, null=False)
    detailed_description = HTMLField(_('Detailed description'), null=True, blank=True)
    description = models.TextField(_('Description'), blank=True)

    is_recommended = models.BooleanField(default=False)
    is_banner = models.BooleanField(default=False)

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    def has_attributes(self):
        return bool(self.attrs.all())
        # if self.is_child:
        #     return self.parent.has_attributes()
        # ancestors = self.category.get_ancestors()
        # for ancestor in ancestors:
        #     if ancestor.schemas.exists():
        #         return True
        #     else:
        #         continue
        # return True if self.category.schemas.exists() else False

    def __unicode__(self):
        return self.title


    @property
    def cat(self):
        return self.category

    def clean(self):
        """
        Validate a product. Those are the rules:
        +---------------+--------------+--------------+
        |               | parent       | child        |
        +---------------+--------------+--------------+
        | title         | required     | optional     |
        +---------------+--------------+--------------+
        | parent        | forbidden    | required     |
        +---------------+--------------+--------------+
        Because the validation logic is quite complex, validation is delegated
        to the sub method appropriate for the product's structure.
        """
        getattr(self, '_clean_%s' % self.structure)()

    def _clean_standalone(self):
        """
        Validates a stand-alone product
        """
        if not self.title:
            raise ValidationError(_("Your product must have a title."))
        if self.parent_id:
            raise ValidationError(_("Only child products can have a parent."))

    def _clean_child(self):
        """
        Validates a child product
        """
        pass
        # use this validation somewhere else
        # if not self.parent_id:
        #     raise ValidationError(_("A child product needs a parent."))
        # if self.parent_id and not self.parent.is_parent:
        #     raise ValidationError(
        #         _("You can only assign child products to parent products."))

    def _clean_parent(self):
        """
        Validates a parent product.
        """
        self._clean_standalone()
    # Properties

    @property
    def is_parent(self):
        return self.structure == self.PARENT

    @property
    def is_child(self):
        return self.structure == self.CHILD

    def can_be_parent(self, give_reason=False):
        """
        Helps decide if a the product can be turned into a parent product.
        """
        reason = None
        if self.is_child:
            reason = _('The specified parent product is a child product.')
        is_valid = reason is None
        if give_reason:
            return is_valid, reason
        else:
            return is_valid

    @classmethod
    def get_schemata_for_model(cls):
        return Schema.objects.all()

    def get_schemata_for_instance(self, qs, predefined=False):
        """Returns schemata filtered by this item's component."""
        if self.is_parent:
            if self.cat:
                categories = [self.cat] + list(self.cat.get_ancestors())
                res = qs.filter(categories__in=categories)
                return qs.filter(categories__in=categories)
            else:
                return qs.none()
        else:
            if self.parent:
                return self.parent.get_schemata_for_instance(qs, True)
            else:
                return qs.none


def _upload_path_wrapper(self, filename):
    return self.get_upload_path(filename)


class DatePrices(models.Model):
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    price = models.IntegerField(default=0)
    cottage = models.ForeignKey(Cottage, related_name='prices', null=True, blank=True, verbose_name=_('Pricing'))


class GenericModelBase(models.Model):
    """
        Abstract base class for models that will be attached using
        generic relations.

        .. attribute:: object_id

            A PositiveIntegerField containing the primary key of the object the model
            is attached to.

        .. attribute:: content_type

            A ForeignKey to ContentType; this is the type of the object the model is
            attached to.

    """

    content_type = models.ForeignKey(ContentType)

    object_id = models.PositiveIntegerField()

    content_object = generic.GenericForeignKey()
    """ A GenericForeignKey attribute pointing to the object the comment is
       attached to. You can use this to get at the related object
       (i.e. my_model.content_object). Since this field is a
       GenericForeignKey, it’s actually syntactic sugar on top of two underlying
       attributes, described above.
    """

    objects = GenericModelManager()
    """
        Default manager. It is of type :class:~main.managers.GenericModelManager.
    """

    injector = GenericInjector()
    """
        :class:main.injectors.GenericInjector manager.
    """

    class Meta:
        abstract = True


class BaseImageModel(models.Model):
    """ Simple abstract Model class with image field.

        .. attribute:: image

            ``models.ImageField``
    """

    def get_upload_path(self, filename):
        """ Override this to customize upload path """
        raise NotImplementedError

    image = models.ImageField(_('Image'), upload_to=_upload_path_wrapper)

    class Meta:
        abstract = True


class ReplaceOldImageModel(BaseImageModel):
    """
        Abstract Model class with image field.
        If the file for image is re-uploaded, old file is deleted.
    """

    def _replace_old_image(self):
        """ Override this in subclass if you don't want
            image replacing or want to customize image replacing
        """
        try:
            old_obj = self.__class__.objects.get(pk=self.pk)
            if old_obj.image.path != self.image.path:
                path = old_obj.image.path
                OverwriteStorage().delete(path)
        except self.__class__.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if self.pk:
            self._replace_old_image()
        super(ReplaceOldImageModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class AbstractAttachedImage(ReplaceOldImageModel, GenericModelBase):
    """
        Abstract Image model that can be attached to any other Django model
        using generic relations.

        .. attribute:: is_main

            BooleanField. Whether the image is the main image for object.
            This field is set to False automatically for all images attached to
            same object if image with is_main=True is saved to ensure that there
            is only 1 main image for object.

        .. attribute:: order

            IntegerField to support ordered image sets.
            On creation it is set to max(id)+1.

    """

    caption = models.TextField(_('Caption'), null=True, blank=True)
    'TextField caption for image'

    is_main = models.BooleanField(_('Main image'), default=False)

    order = models.IntegerField(_('Order'), default=0)

    objects = AttachedImageManager()
    """Default manager of :class:~main.managers.AttachedImageManager
    type."""

    def next(self):
        """ Returns next image for same content_object and None if image is
        the last. """
        try:
            return self.__class__.objects.for_model(self.content_object,
                                                    self.content_type). \
                filter(order__lt=self.order).order_by('-order')[0]
        except IndexError:
            return None

    def previous(self):
        """ Returns previous image for same content_object and None if image
        is the first. """
        try:
            return self.__class__.objects.for_model(self.content_object,
                                                    self.content_type). \
                filter(order__gt=self.order).order_by('order')[0]
        except IndexError:
            return None

    def get_order_in_album(self, reversed_ordering=True):
        """ Returns image order number. It is calculated as (number+1) of images
        attached to the same content_object whose order is greater
        (if 'reverse_ordering' is True) or lesser (if 'reverse_ordering' is
        False) than image's order.
        """
        lookup = 'order__gt' if reversed_ordering else 'order__lt'
        return self.__class__.objects. \
                   for_model(self.content_object, self.content_type). \
                   filter(**{lookup: self.order}).count() + 1

    def _get_next_pk(self):
        max_pk = self.__class__.objects.aggregate(m=Max('pk'))['m'] or 0
        return max_pk + 1

    def get_file_name(self, filename):
        """ Returns file name (without path and extenstion)
            for uploaded image. Default is 'max(pk)+1'.
            Override this in subclass or assign another functions per-instance
            if you want different file names (ex: random string).
        """
        return str(self._get_next_pk())

    def get_upload_path(self, filename):
        """ Override this in proxy subclass to customize upload path.
            Default upload path is
            :file:`/media/images/<user.id>/<filename>.<ext>`
            or :file:`/media/images/common/<filename>.<ext>` if user is not set.

            ``<filename>`` is returned by
            :meth:`~generic_images.models.AbstractAttachedImage.get_file_name`
            method. By default it is probable id of new image (it is
            predicted as it is unknown at this stage).
        """
        user_folder = 'common'

        root, ext = os.path.splitext(filename)
        return os.path.join('media', 'images', user_folder,
                            self.get_file_name(filename) + ext)

    def save(self, *args, **kwargs):
        send_signal = getattr(self, 'send_signal', True)
        if self.is_main:
            related_images = self.__class__.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id
            )
            related_images.update(is_main=False)

        if not self.pk:
            if not self.order:
                self.order = self._get_next_pk()

        super(AbstractAttachedImage, self).save(*args, **kwargs)

        if send_signal:
            image_saved.send(sender=self.content_type.model_class(),
                             instance=self)

    def delete(self, *args, **kwargs):
        send_signal = getattr(self, 'send_signal', True)
        super(AbstractAttachedImage, self).delete(*args, **kwargs)
        if send_signal:
            image_deleted.send(sender=self.content_type.model_class(),
                               instance=self)

    def __unicode__(self):
        try:
            return u"AttachedImage #%d for [%s]" % (
                self.pk, self.content_object,)
        except:
            try:
                return u"AttachedImage #%d" % (self.pk)
            except TypeError:
                return u"new AttachedImage"

    class Meta:
        abstract = True


class ImageContainingModel(object):
    def image_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image

        :returns: str -- the image url

        """
        picture = filter(lambda f: isinstance(f, models.ImageField), self._meta.fields)[0]
        if picture and hasattr(picture, 'url'):
            return picture.url
        else:
            return settings.DEFAULT_IMAGE


class Image(models.Model, ImageContainingModel):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    caption = models.TextField(_('Caption'), null=True, blank=True)
    'TextField caption for image'

    is_main = models.BooleanField(_('Main image'), default=False)

    order = models.IntegerField(_('Order'), default=0)

    def image_tag(self):
        return u'<img src="%s" style="max-width: 120px" />' % self.image.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    image = models.ImageField(_('Image'), upload_to='cottage_images'
                              , storage=OverwriteStorage()
                              , default=settings.DEFAULT_IMAGE)


class SchemaForMpttTest(models.Model):
    schema = models.ForeignKey(Schema)
    mptttest = models.ForeignKey(MpttTest)
    will_be_a_filter = models.BooleanField(default=False)
    name_on_forms = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _('Attribute of MPTT')
        verbose_name_plural = _('Attributes of MPTT')
        unique_together = ['schema', 'mptttest']


class SchemaForCategory(models.Model):
    schema = models.ForeignKey(Schema)
    category = models.ForeignKey(Category)
    will_be_a_filter = models.BooleanField(default=False)
    name_on_forms = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _('Attribute of Category')
        verbose_name_plural = _('Attributes of Category')
        unique_together = ['schema', 'category']
from django.db import models
from eav.models import BaseAttribute, BaseSchema, BaseChoice, BaseEntity
from treebeard.ns_tree import NS_Node
from treebeard.al_tree import AL_Node
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from Cottage_Club.main.managers import CottageManager

# Create your models here.


class Schema(BaseSchema):
    pass

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'


class Category(NS_Node):
    name = models.CharField(max_length=30)
    schemas = models.ManyToManyField(Schema, through='SchemaForCategory', related_name='categories')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Choice(BaseChoice):
    pass


class Attribute(BaseAttribute):
    schema = models.ForeignKey(Schema)
    choice = models.ForeignKey(Choice)
    description = models.CharField(max_length=200, blank=True)
    pass


class SchemaForCategory(models.Model):
    schema = models.ForeignKey(Schema)
    category = models.ForeignKey(Category)
    will_be_a_filter = models.BooleanField(default=False)
    name_on_forms = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Attribute of Category'
        verbose_name_plural = 'Attributes of Category'
        unique_together = ['schema', 'category']


class Cottage(BaseEntity, AL_Node):

    STANDALONE, PARENT, CHILD = 'standalone', 'parent', 'child'
    STRUCTURE_CHOICES = (
        (STANDALONE, _('Stand-alone product')),
        (PARENT, _('Parent product')),
        (CHILD, _('Child product'))
    )

    objects = CottageManager
    category = models.ForeignKey(Category)
    images = generic.GenericRelation('Image')
    structure = models.CharField(
        _("Product structure"), max_length=10, choices=STRUCTURE_CHOICES,
        default=STANDALONE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        verbose_name=_("Parent product"),
        related_name='children_set',
        null=True,
        help_text=_("Only choose a parent product if you're creating a child "
                    "product.  For example if this is a size "
                    "4 of a particular t-shirt.  Leave blank if this is a "
                    "stand-alone product (i.e. there is only one version of"
                    " this product)."))

    title = models.CharField(_(u'Product title', u'Title'),
                             max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)

    is_recommended = models.BooleanField(default=False)
    is_banner = models.BooleanField(defaul=False)

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    def clean(self):
        """
        Validate a product. Those are the rules:
        +---------------+-------------+--------------+--------------+
        |               | stand alone | parent       | child        |
        +---------------+-------------+--------------+--------------+
        | title         | required    | required     | optional     |
        +---------------+-------------+--------------+--------------+
        | parent        | forbidden   | forbidden    | required     |
        +---------------+-------------+--------------+--------------+
        Because the validation logic is quite complex, validation is delegated
        to the sub method appropriate for the product's structure.
        """
        getattr(self, '_clean_%s' % self.structure)()
        if not self.is_parent:
            self.attr.validate_attributes()

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
        if not self.parent_id:
            raise ValidationError(_("A child product needs a parent."))
        if self.parent_id and not self.parent.is_parent:
            raise ValidationError(
                _("You can only assign child products to parent products."))

    def _clean_parent(self):
        """
        Validates a parent product.
        """
        self._clean_standalone()
    # Properties

    @property
    def is_standalone(self):
        return self.structure == self.STANDALONE

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

    def get_schemata_for_instance(self, qs):
        """Returns schemata filtered by this item's component."""
        categories = self.category.get_ancestors()
        return qs.filter(categories__in=categories)


class Image(models.Model):
    url = models.ImageField()
    entity_type = models.ForeignKey(ContentType)
    entity_id = models.PositiveIntegerField()
    entity = generic.GenericForeignKey(ct_field="entity_type", fk_field='entity_id')
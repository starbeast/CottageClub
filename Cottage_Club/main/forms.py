from eav.forms import BaseDynamicEntityForm
from eav.forms import BaseSchemaForm
from collections import OrderedDict
from Cottage_Club.main.models import Cottage, Schema, Image
from django.forms import ValidationError, ModelForm, CharField
from django.utils.translation import ugettext_lazy as _
from copy import deepcopy


def image_form_factory(lang='en', debug=False):
    """ Returns ModelForm class to be used in admin.
        'lang' is the language for GearsUploader (can be 'en' and 'ru' at the
        moment).
    """

    class _AttachedImageAdminForm(ModelForm):

        caption = CharField(label=_('Caption'), required=False)

        class Meta:
            model = Image
    return _AttachedImageAdminForm


class DynamicEntityForm(BaseDynamicEntityForm):
    def __init__(self, data=None, *args, **kwargs):
        self.dynamic_fields = OrderedDict()
        super(DynamicEntityForm, self).__init__(data, *args, **kwargs)

    def _build_dynamic_fields(self):
        self.fields = deepcopy(self.base_fields)

        # do not display dynamic fields if some fields are yet defined
        if not self.check_eav_allowed():
            return

        for schema in self.instance.get_schemata():

            defaults = {
                'label':     schema.title.capitalize(),
                'required':  schema.required,
                'help_text': schema.help_text,
            }

            datatype = schema.datatype
            if datatype == schema.TYPE_MANY:
                choices = getattr(self.instance, schema.name)
                defaults.update({'queryset': schema.get_choices(),
                                 'initial': [x.pk for x in choices]})
            elif datatype == schema.TYPE_ONE:
                choice = getattr(self.instance, schema.name)
                defaults.update({'queryset': schema.get_choices(),
                                 'initial': choice.pk if choice else None,
                                 # if schema is required remove --------- from ui
                                 'empty_label' : None if schema.required else u"---------"})

            extra = self.FIELD_EXTRA.get(datatype, {})
            if hasattr(extra, '__call__'):
                extra = extra(schema)
            defaults.update(extra)

            MappedField = self.FIELD_CLASSES[datatype]
            field = MappedField(**defaults)
            self.fields[schema.name] = field
            self.dynamic_fields[schema.name] = field

            # fill initial data (if attribute was already defined)
            value = getattr(self.instance, schema.name)
            if value and not datatype in (schema.TYPE_ONE, schema.TYPE_MANY):    # choices are already done above
                self.initial[schema.name] = value


class CottageDynamicForm(DynamicEntityForm):
    model = Cottage


class SchemaForm(BaseSchemaForm):
    class Meta:
        model = Schema

    def clean_name(self):
        name = self.cleaned_data['name']
        reserved_names = Schema.objects.filter(name=name).exclude(pk=self.instance.pk)
        if reserved_names.exists():
            raise ValidationError(_('Attribute name must not clash with reserved names'
                                    ' ("%s")') % '", "'.join(list(reserved_names)))
        return super(SchemaForm, self).clean_name()
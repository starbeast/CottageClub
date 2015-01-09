from eav.forms import BaseDynamicEntityForm
from eav.forms import BaseSchemaForm
from collections import OrderedDict
from Cottage_Club.main.models import Cottage, Schema, Image, Choice, Category, DatePrices
from django.forms import ValidationError, ModelForm, CharField, widgets, TextInput, ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from copy import deepcopy
from django.utils.encoding import smart_text


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


class DatePriceForm(ModelForm):
    class Meta:
        model = DatePrices


class DynamicEntityForm(BaseDynamicEntityForm):
    def __init__(self, data=None, *args, **kwargs):
        self.dynamic_fields = OrderedDict()
        super(DynamicEntityForm, self).__init__(data, *args, **kwargs)

    def _build_dynamic_fields(self):
        self.fields = deepcopy(self.base_fields)

        # do not display dynamic fields if some fields are yet defined
        if not self.check_eav_allowed():
            return

        iterator, empty = self.instance.get_schemata(), False

        for schema in iterator:

            defaults = {
                'label':     schema.title.capitalize(),
                'required':  schema.required,
                'help_text': schema.help_text,
            }

            datatype = schema.datatype
            if datatype == schema.TYPE_MANY:
                if not empty:
                    choices = getattr(self.instance, schema.name)
                    defaults.update({'queryset': schema.get_choices(),
                                     'initial': [x.pk for x in choices]})
                else:
                    defaults.update({'queryset', schema.get_choices()})
            elif datatype == schema.TYPE_ONE:
                if not empty:
                    choice = getattr(self.instance, schema.name)
                    defaults.update({'queryset': schema.get_choices(),
                                     'initial': choice.pk if choice else None,
                                     # if schema is required remove --------- from ui
                                     'empty_label' : None if schema.required else u"---------"})
                else:
                    defaults.update({'queryset': schema.get_choices(),
                                     # if schema is required remove --------- from ui
                                     'empty_label': None if schema.required else u"---------"})
            extra = self.FIELD_EXTRA.get(datatype, {})
            if hasattr(extra, '__call__'):
                extra = extra(schema)
            defaults.update(extra)

            mapped_field = self.FIELD_CLASSES[datatype]
            field = mapped_field(**defaults)
            self.fields[schema.name] = field
            self.dynamic_fields[schema.name] = field

            # fill initial data (if attribute was already defined)
            value = getattr(self.instance, schema.name)
            if value and not datatype in (schema.TYPE_ONE, schema.TYPE_MANY):    # choices are already done above
                self.initial[schema.name] = value


class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.title


class CustomCategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj:
            categories = []
            text = "%s" % obj.name
            if not obj.is_separator:
                for ancestor in obj.get_ancestors().reverse():
                    categories.append(ancestor.name)
                    if ancestor.is_separator:
                        break
                if categories:
                    separator = categories[-1]
                    categories = u", ".join(map(lambda x: x, categories[:-1]))
                    text += (_(' in ') + categories if categories else '') + '(' + separator + ')'
            return smart_text(text)


class CottageDynamicForm(DynamicEntityForm):
    model = Cottage
    category = CustomCategoryModelChoiceField(queryset=Category.objects.all())

    def is_valid(self):
        isvalid = super(CottageDynamicForm, self).is_valid()
        return isvalid


class MyChoiceAdminForm(ModelForm):
    schema = CustomModelChoiceField(queryset=Schema.objects.filter(datatype__in=[Schema.TYPE_MANY, Schema.TYPE_ONE]))

    class Meta:
        model = Choice


class CottageDynamicChildForm(DynamicEntityForm):
    initial_fields = {'structure': Cottage.CHILD}
    structure = CharField(
        widget=TextInput(attrs={'readonly':'readonly'})
    )

    def clean(self):
        cleaned_data = super(CottageDynamicChildForm, self).clean()
        title = cleaned_data.get("title")

        if not title:
            raise ValidationError("Title is required.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        for key, val in self.initial_fields.iteritems():
            initial[key] = initial.get(key, None) or val
        kwargs['initial'] = initial
        super(CottageDynamicChildForm, self).__init__(*args, **kwargs)


class CottageDynamicCategoryForm(CottageDynamicChildForm):
    initial_fields = {'structure': Cottage.PARENT}


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
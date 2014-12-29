from django.contrib import admin
from django.utils.functional import curry
from django.contrib.contenttypes.generic import GenericTabularInline
from treebeard.admin import TreeAdmin
from django.forms import formsets
from treebeard.forms import movenodeform_factory
from eav.admin import BaseEntityAdmin, BaseEntityInline, BaseSchemaAdmin, BaseEntityInlineFormSet
from Cottage_Club.main.forms import CottageDynamicForm, SchemaForm, image_form_factory
from Cottage_Club.main.models import Category, Cottage, SchemaForCategory, Schema, Choice, Image


ImageAdminForm = image_form_factory()


class CottageBaseFormSet(BaseEntityInlineFormSet):
    def __init__(self, *args, **kwargs):
        """
        Grabs the curried initial values and stores them into a 'private'
        variable. Note: the use of self.__initial is important, using
        self.initial or self._initial will be erased by a parent class
        """
        self.__initial = kwargs.pop('initial', [])
        super(CottageBaseFormSet, self).__init__(*args, **kwargs)

    def total_form_count(self):
        return len(self.__initial) + self.extra

    def _construct_forms(self):
        return formsets.BaseFormSet._construct_forms(self)

    def _construct_form(self, i, **kwargs):
        if self.__initial:
            try:
                kwargs['initial'] = self.__initial[i]
            except IndexError:
                pass
        return formsets.BaseFormSet._construct_form(self, i, **kwargs)

CottageFormSet = formsets.formset_factory(CottageDynamicForm, formset=CottageBaseFormSet)


def images_inline_factory(lang='en', max_width='', debug=False):
    """  Returns InlineModelAdmin for attached images.
        'lang' is the language for GearsUploader (can be 'en' and 'ru' at the
        moment). 'max_width' is default resize width parameter to be set in
        widget.
    """

    class _AttachedImagesInline(GenericTabularInline):
        model = Image
        form = image_form_factory(lang, debug)
        template = 'generic_images/attached_images_inline.html'
        max_w = max_width

    return _AttachedImagesInline


class ImagesInline(GenericTabularInline):
    model = Image
    readonly_fields = ('image_tag', )
    extra = 0
    ct_field_name = 'content_type'
    id_field_name = 'object_id'


class CottageAdminInline(BaseEntityInline, admin.StackedInline):
    model = Cottage
    form = CottageDynamicForm
    formset = CottageFormSet
    exclude = ('structure',)
    readonly_fields = ('parent', )
    extra = 0

    def get_fields(self, request, obj=None):
        if self.fields:
            return self.fields
        formset = self.get_formset(request, obj, fields=None)
        fk_name = self.fk_name or formset.fk.name
        kw = {fk_name: obj} if obj else {}
        instance = self.model(**kw)
        form = formset.form(request.POST, instance=instance)
        return list(formset.form.base_fields)\
               + (list(form.dynamic_fields) if hasattr(form, 'dynamic_fields') else [])\
               + list(self.get_readonly_fields(request, obj))

    def get_fieldsets(self, request, obj=None):
        if self.fieldsets:
            return self.fieldsets
        return [(None, {'fields': self.get_fields(request, obj)})]


class CottageAdminInlineCottage(CottageAdminInline):
    readonly_fields = ('category', 'structure')
    exclude = []

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if request.method == "GET":
            initial.append({
                'structure': Cottage.CHILD,
            })
        formset = super(CottageAdminInlineCottage, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset


class InnerCottageAdminInline(CottageAdminInline):
    pass


class SchemaInline(admin.StackedInline):
    model = Schema
    form = SchemaForm
    extra = 0


class SchemaForCategoryInline(admin.StackedInline):
    model = Category.schemas.through
    extra = 0


class CottageAdmin(BaseEntityAdmin, TreeAdmin):
    form = CottageDynamicForm
    inlines = [ImagesInline, CottageAdminInlineCottage]
    exclude = ('sib_order', )

    def save_formset(self, request, form, formset, change):
        if change:
            return super(CottageAdmin, self).save_formset(request, form, formset, True)
        else:
            if form.is_valid() and formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.structure = Cottage.CHILD
                    instance.category = instance.parent.category
                    instance.save()
                formset.save_m2m()

    class Media:
        js = ('js/admin/CottageAdmin.js',)
    

class CategoryAdmin(TreeAdmin):
    # pass
    form = movenodeform_factory(Category)
    inlines = (CottageAdminInline, SchemaForCategoryInline)


class SchemaAdmin(BaseSchemaAdmin):
    form = SchemaForm
    inlines = (SchemaForCategoryInline, )

# admin.site.unregister(AttachedImagesInline)
admin.site.register(Cottage, CottageAdmin)
admin.site.register(Schema, SchemaAdmin)
admin.site.register(Choice)
admin.site.register(Category, CategoryAdmin)
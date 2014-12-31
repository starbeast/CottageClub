from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from treebeard.admin import TreeAdmin
from django.utils.translation import ugettext_lazy as _
from django.forms import formsets
from django.forms.models import BaseInlineFormSet
from django.utils.safestring import mark_safe
from treebeard.forms import movenodeform_factory
from eav.admin import BaseEntityAdmin, BaseSchemaAdmin, BaseEntityInlineFormSet, BaseEntityInline
from Cottage_Club.main.forms import CottageDynamicCategoryForm, CottageDynamicChildForm, CottageDynamicForm, SchemaForm, image_form_factory, MyChoiceAdminForm
from Cottage_Club.main.models import Category, Cottage, Schema, Choice, Image, Attribute, MpttTest
from mptt.admin import MPTTModelAdmin, MPTTAdminForm
from mptt.forms import TreeNodeChoiceField


ImageAdminForm = image_form_factory()


class SchemaForMpttTestInline(admin.StackedInline):
    model = MpttTest.schemas.through
    extra = 0


class MPTTAdminMixin(object):
    form = MPTTAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        from mptt.models import MPTTModel, TreeForeignKey
        if issubclass(db_field.rel.to, MPTTModel) \
                and not isinstance(db_field, TreeForeignKey) \
                and not db_field.name in self.raw_id_fields:
            defaults = dict(form_class=TreeNodeChoiceField, queryset=db_field.rel.to.objects.all(), required=False)
            defaults.update(kwargs)
            kwargs = defaults
        return super(MPTTAdminMixin, self).formfield_for_foreignkey(db_field,
                                                                    request,
                                                                    **kwargs)


class MPTTTabularInlineAdmin(MPTTAdminMixin, admin.TabularInline):
    model = MpttTest
    extra = 0
    pass


class CustomizedMpttAdmin(MPTTModelAdmin):
    inlines = [MPTTTabularInlineAdmin, SchemaForMpttTestInline]


class ImagesInline(GenericTabularInline):
    model = Image
    readonly_fields = ('image_tag', )
    extra = 0
    ct_field_name = 'content_type'
    id_field_name = 'object_id'


class CottageFormSet(BaseEntityInlineFormSet):
    pass


class CottageAdminInline(admin.StackedInline):
    model = Cottage
    form = CottageDynamicCategoryForm
    exclude = ('sib_order', 'is_banner', 'is_recommended')
    readonly_fields = ('parent', )
    formset = CottageFormSet
    extra = 0

    def get_fields(self, request, obj=None):
        if self.fields:
            return self.fields
        form = self.get_formset(request, obj, fields=None).form
        return list(form.base_fields) + list(self.get_readonly_fields(request, obj))

    def get_fieldsets(self, request, obj=None):
        declared_fieldsets = self.declared_fieldsets
        if declared_fieldsets:
            return declared_fieldsets

        if self.fieldsets:
            return self.fieldsets
        values = self.get_fields(request, obj)
        return [(None, {'fields': values})]


class CottageAdminInlineCottage(CottageAdminInline):
    form = CottageDynamicChildForm
    readonly_fields = ('category',)


class AttributeInline(GenericTabularInline):
    model = Attribute
    extra = 0
    fields = ('description', 'is_separator', 'order')
    ct_field = 'entity_type'
    ct_fk_field = 'entity_id'

    def has_add_permission(self, request):
        return False


class SchemaInline(admin.StackedInline):
    model = Schema
    form = SchemaForm
    extra = 0


class SchemaForCategoryInline(admin.StackedInline):
    model = Category.schemas.through
    extra = 0


class CottageAdmin(TreeAdmin):
    form = CottageDynamicForm
    inlines = (ImagesInline, CottageAdminInlineCottage, AttributeInline)
    change_form_template = "admin/cottage_change_form.html"
    eav_fieldsets = None
    exclude = ('sib_order', )

    def render_change_form(self, request, context, **kwargs):
        """
        Wrapper for ModelAdmin.render_change_form. Replaces standard static
        AdminForm with an EAV-friendly one. The point is that our form generates
        fields dynamically and fieldsets must be inferred from a prepared and
        validated form instance, not just the form class. Django does not seem
        to provide hooks for this purpose, so we simply wrap the view and
        substitute some data.
        """
        form = context['adminform'].form
        formset = context['inline_admin_formsets']

        all_fields = form.fields.keys()
        model_fields = form.base_fields.keys()
        eav_fields = filter(lambda x: x not in model_fields, all_fields)

        if self.eav_fieldsets:
            fieldsets_eav = self.eav_fieldsets + (('Attributes', {'classes': ('collapse',), 'fields': tuple(eav_fields)}),)
            fieldsets = fieldsets_eav
        else:
            # or infer correct data from the form
            fieldsets = [(None, {'fields': all_fields})]

        adminform = admin.helpers.AdminForm(form, fieldsets,
                                            self.prepopulated_fields)
        inline_media = []
        if formset:
            if len(formset) > 1:
                for fset in formset:
                    if inline_media:
                        inline_media += fset.media
                    else:
                        inline_media = fset.media
            else:
                inline_media = formset[0].media

        media = mark_safe(self.media + adminform.media + inline_media)
        context.update(adminform=adminform, media=media)

        super_meth = super(CottageAdmin, self).render_change_form
        return super_meth(request, context, **kwargs)

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, AttributeInline) and (obj is None or not obj.has_attributes()):
                continue
            yield inline.get_formset(request, obj)

    def save_formset(self, request, form, formset, change):
        if not isinstance(formset, CottageFormSet):
            super(CottageAdmin, self).save_formset(request, form, formset, change)
        else:
            if formset.is_valid():
                for inner_form in (formset.extra_forms + formset.initial_forms):
                    if inner_form.is_valid():
                        if not inner_form.instance.category:
                            inner_form.instance.category = form.instance.category
                            inner_form.changed_data.append('category')
            super(CottageAdmin, self).save_formset(request, form, formset, change)

    class Media:
        js = ('js/admin/CottageAdmin.js',)
    

class CategoryAdmin(TreeAdmin):
    # pass
    form = movenodeform_factory(Category)
    inlines = (CottageAdminInline, SchemaForCategoryInline)


class SchemaAdmin(BaseSchemaAdmin):
    form = SchemaForm
    exclude = ['required', 'filtered']
    list_display = ('title', 'name', 'datatype', 'help_text')
    inlines = (SchemaForCategoryInline, )


class ChoiceAdmin(admin.ModelAdmin):
    form = MyChoiceAdminForm
    list_display = ('title', 'schema_name')

    def schema_name(self, obj):
        return ("%s" % obj.schema.title).capitalize()
    schema_name.short_description = Schema._meta.verbose_name


admin.site.register(Cottage, CottageAdmin)
admin.site.register(Schema, SchemaAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Category, CategoryAdmin)
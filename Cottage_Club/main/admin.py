from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from treebeard.admin import TreeAdmin
from django.forms import formsets
from django.utils.safestring import mark_safe
from treebeard.forms import movenodeform_factory
from eav.admin import BaseEntityAdmin, BaseSchemaAdmin, BaseEntityInlineFormSet, BaseEntityInline
from Cottage_Club.main.forms import CottageDynamicForm, CottageDynamicChildForm, SchemaForm, image_form_factory
from Cottage_Club.main.models import Category, Cottage, Schema, Choice, Image, Attribute


ImageAdminForm = image_form_factory()


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
    exclude = ('sib_order', )
    readonly_fields = ('category',)
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
    exclude = ['sib_order']


class AttributeInline(GenericTabularInline):
    model = Attribute
    extra = 0
    fields = ('description', )
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
    inlines = (ImagesInline, CottageAdminInline, AttributeInline)

    eav_fieldsets = None

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

# admin.site.unregister(AttachedImagesInline)
admin.site.register(Cottage, CottageAdmin)
# admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Schema, SchemaAdmin)
admin.site.register(Choice)
admin.site.register(Category, CategoryAdmin)
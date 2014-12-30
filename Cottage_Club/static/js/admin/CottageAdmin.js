(function($) {
    var get_only_parents_ajax = window.admin_urls['get_only_parents_ajax'];
    var get_category_for_parent = window.admin_urls['get_category_for_parent'];
    var prepare_fields = function(par, cat) {
        var parent = $('select[name="' + par + '"]');
        var parentHtml = parent.html();
        var childrenGroupSelector = '#children-group';
        var childrenGroup = $(childrenGroupSelector);
        var handler = $._data(childrenGroup.find('.add-row a').get(0), 'events')['click'][0]['handler'];
        var childrenGroupInitial = $($('<div/>').append(childrenGroup.clone()).html()).css('display', 'none');
        var addAnother = parent.siblings('.add-another');
        var addAnotherClone = addAnother.clone();
        var category = $('select[name="' + cat + '"]');
        var categoryHtml = category.html();
        var addAnotherCat = category.siblings('.add-another');
        var addAnotherCatClone = addAnotherCat.clone();
        var value = null;
        var structure = $('select[name="structure"]');
        var changeCategory = function(value) {
            $.ajax({
                type: 'GET',
                format: 'json',
                url: get_category_for_parent,
                data: { 'id': value },
                success: function(data) {
                    var opt = category.val(data.value).find('option').first().html(data.name).attr({'value': data.value, 'selected': 'selected'});
                    category.find("option").not(opt).remove();
                },
                error: function(data) {
                    console.log('error');
                }
            });
        };
        $(parent).on('change', function() {
            var val = $(this).val();
            if(val && structure.val() == 'child') {
                changeCategory(val);
            }
        });
        structure.on('change', function() {
            console.log('change');
            var val = $(this).val();
            if(val != value) {
                if(val == 'parent') {
                    $(childrenGroupSelector).replaceWith(childrenGroup);
                    childrenGroup.find('.add-row a').click(handler);
                    category.html(categoryHtml);
                    category.val(category.find('option').first().attr('value'));
                    addAnotherCatClone.insertAfter(category);
                    addAnotherCat = addAnotherCatClone;
                    addAnotherCatClone = addAnotherCatClone.clone();
                    parent.html(parentHtml);
                    parent.val("").find('option[value!=""]').remove();
                    addAnother.remove();
                } else {
                    $(childrenGroupSelector).replaceWith(childrenGroupInitial);
                    parent.html(parentHtml);
                    parent.find('option[value=""]').remove();
                    parent.val(parent.find('option').first().attr('value'));
                    addAnotherClone.insertAfter(parent);
                    addAnother = addAnotherClone;
                    addAnotherClone = addAnotherClone.clone();
                    category.html(categoryHtml);
                    category.val("").find('option[value!=""]').remove();
                    if(parent) {
                        changeCategory(parent.val());
                    }
                    addAnotherCat.remove();
                }
                value = val;
            }
        });
        var val =  structure.val();
        if(val == 'parent') {
            if(category.val()) {
                category.find('option[value="' + category.val() + '"]').siblings().remove();
                structure.find('option[value="child"]').remove();
                addAnotherCat.remove();
            }
            parent.val("").find('option[value!=""]').remove();
            addAnother.remove();
        } else {
            childrenGroup.css('display', 'none');
            if(parent.val()) {
                structure.find('option[value="parent"]').remove();
                parent.find('option[value="' + parent.val() + '"]').siblings().remove();
                addAnotherCat.remove();
                addAnother.remove();
            }
            category.val("").find('option[value!=""]').remove();
            addAnotherCat.remove();
            parent.find('option[value=""]').remove();
            changeCategory(parent.val());
        }
    };
    $(document).ready(function() {
        var parent = $('select[name="parent"]');
        if(parent.length) {
            $.ajax({
                type: 'GET',
                format: 'json',
                url: get_only_parents_ajax,
                success: function(data) {
                    data = JSON.parse(data);
                    var value = parent.val();
                    var options = parent.find('option');
                    var formattedData = $.map(data, function(elem, ind) {
                        return elem['pk'];
                    });
                    var parentHtml = $.grep(options, function(elem, ind) {
                        var value = parseInt($(elem).attr('value'));
                        return formattedData.indexOf(value) != -1;
                    });
                    var cln = parent.find('option[value=""]').clone();
                    parent.find('option').not(parentHtml).remove();
                    parent.prepend(cln);
                    prepare_fields('parent', 'category');
                }
            });
        }
    });
})(django.jQuery);
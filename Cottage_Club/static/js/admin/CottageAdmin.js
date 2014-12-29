(function($) {
    var url = '/admin/ajax/get_all_parents';
    var prepare_fields = function(par, cat) {
        var parent = $('select[name="' + par + '"]');
        var parentHtml = parent.html();
        var addAnother = parent.siblings('.add-another');
        var addAnotherClone = addAnother.clone();
        var category = $('select[name="' + cat + '"]');
        var categoryHtml = category.html();
        var addAnotherCat = category.siblings('.add-another');
        var addAnotherCatClone = addAnotherCat.clone();
        var value = null;
        $('select[name="structure"]').on('change', function() {
            console.log('change');
            var val = $(this).val();
            if(val != value) {
                if(val == 'parent') {
                    category.html(categoryHtml);
                    category.val(category.find('option').first().attr('value'));
                    addAnotherCatClone.insertAfter(category);
                    addAnotherCat = addAnotherCatClone;
                    addAnotherCatClone = addAnotherCatClone.clone();
                    parent.html(parentHtml);
                    parent.val("").find('option[value!=""]').remove();
                    addAnother.remove();
                } else {
                    parent.html(parentHtml);
                    parent.find('option[value=""]').remove();
                    parent.val(parent.find('option').first().attr('value'));
                    addAnotherClone.insertAfter(parent);
                    addAnother = addAnotherClone;
                    addAnotherClone = addAnotherClone.clone();
                    category.html(categoryHtml);
                    category.val("").find('option[value!=""]').remove();
                    addAnotherCat.remove();
                }
                value = val;
            }
        });
        var val =  $('select[name="structure"]').val();
        if(val == 'parent') {
            parent.val("").find('option[value!=""]').remove();
            addAnother.remove();
        } else {
            category.val("").find('option[value!=""]').remove();
            addAnotherCat.remove();
            parent.find('option[value=""]').remove();
        }
    };
    $(document).ready(function() {
        var parent = $('select[name="parent"]');
        if(parent.length) {
            $.ajax({
                type: 'GET',
                format: 'json',
                url: url,
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
                    parent.find('option').not(parentHtml).remove();
                    prepare_fields('parent', 'category');
                }
            });
        }
    });
})(django.jQuery);
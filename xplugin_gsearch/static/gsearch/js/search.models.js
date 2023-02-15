$(function () {
    $(".switcher-control input[name='all']").change(function (){
        $("input.gsearch-models.lityfilter:checkbox").trigger('change'); //update states
    })
    $("input.gsearch-models:checkbox").change(function () {
        // synchronize reverse filter state
        var $el = $(this),
            related = $el.data("related"),
            is_checked = $el.is(":checked"),
            classHandler = (is_checked ? "add" : "remove") + "Class",
            $obj = $("input.gsearch-models[name=filter_name_" + $el.val() + "]")
                .filter(related);
        $obj.prop("checked", is_checked);
        $obj.parent()[classHandler]('active');
    })
    $("#gsearch_form").submit(function () {
        var $form = $(this),
            $hidden = $("<input>").attr("type", "hidden");
        $form.append($hidden.clone().attr("name", "shr").val(1));
        $form.data("checked_input_filters", {});
        $("input.gsearch-models").each(function () {
            var $el = $(this),
                $checked_filters = $form.data("checked_input_filters"),
                $obj;
            if ($el.is(":checked") && !$checked_filters[$el.val()]) {
                $obj = $hidden.clone().attr("name", "mdl").val($el.val());
                $checked_filters[$el.val()] = $obj;
                $form.append($obj);
            }
        });
    });
});
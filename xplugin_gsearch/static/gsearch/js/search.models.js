$(function () {
    $("#gsearch_form").submit(function () {
        var $form = $(this),
            $hidden = $("<input>").attr("type", "hidden");
        $('input.gsearch-models').each(function () {
            var $el = $(this),
                $obj;
            if ($el.is(":checked")) {
                $obj = $hidden.clone().attr("name", "models").val($el.val());
                $form.append($obj);
            }
        });
    });
});
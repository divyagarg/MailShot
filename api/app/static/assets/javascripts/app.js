$(function () {
    $(".btn-toggle").click(function () {
        // toggle button ui
        $(this)
            .toggleClass('btn-toggle-onstate')
            .toggleClass('btn-toggle-offstate')
            .find('.btn-toggle-option')
            .toggleClass('btn-toggle-active');

        // toggle checkbox
        var $checkbox = $(this).find('input[type=checkbox]')
        var newStatus = !$checkbox.prop("checked")
        $checkbox.prop("checked", newStatus)
        $checkbox.attr("checked", newStatus)
    });
});

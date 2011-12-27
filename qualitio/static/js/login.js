$(function() {
    $('input[type=submit], .button').button();

    $("label").inFieldLabels();
    $("input").attr("autocomplete","off");

    var $password = $("#id_password2, label[for=id_password2]");

    $password.toggle(
        $(".user-type input:checked").val() == "1"
    );
    
    $(".user-type input").change(function() {
        $password.toggle(
            $(".user-type input:checked").val() == "1"
        );
    });
})

$(window).resize(function(){
  $("label").inFieldLabels();
});

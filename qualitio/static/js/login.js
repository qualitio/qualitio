$(function() {
    $('input[type=submit], .button').button();

    $("label").inFieldLabels();
    $("input").attr("autocomplete","off");

/* Commented,  fixed of visibility password confirmation on registration page for new user
   new problem, on page of creation organization for returned user visible password confirmation
   ( to improve in the future ) 

    var $password = $("#id_password2, label[for=id_password2]");

    $password.toggle(
        $(".user-type input:checked").val() == "1"
    );
    
    $(".user-type input").change(function() {
        $password.toggle(
            $(".user-type input:checked").val() == "1"
        );
    });
*/
})


$(window).resize(function(){
  $("label").inFieldLabels();
});

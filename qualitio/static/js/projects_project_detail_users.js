$(function() {
  $('.fieldpills a.delete').button({
    icons: {
      primary: "ui-icon-circle-close"
    },
    text: false
  });
  $('#project_users input[type=submit]').button();

  $('.fieldpills .delete').click(function() {
    $.post($(this).attr('href'), function(data) {
      $("#tabs").tabs("load", 0);
    });
    return false;
  });

  $('#project_users').ajaxForm({
    success: function(response) {
      if(response.success) {
        $("#tabs").tabs("load", 0);
      } else {
        $('#project_users .error').show()
          .html(response.data[0][1]);
      }
    },
    beforeSubmit: function() {
      $('#project_users .error').hide();
    }
  });

});

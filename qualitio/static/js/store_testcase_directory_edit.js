$(document).ready(function() {
  $('#testcasedirectory_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $("h1").text("test case directory: " + $('#id_name').val());
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "testcasedirectory", "testcasedirectory", response.data.current_id);
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });
});

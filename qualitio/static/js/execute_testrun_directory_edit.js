$(document).ready(function() {
  $('#testrundirectory_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $("h1").text("test run directory: " + $('#id_name').val());
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "testrundirectory", "testrundirectory", response.data.current_id);
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });
});

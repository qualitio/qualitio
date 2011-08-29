$(document).ready(function() {
  $('select[name="parent"]').chosen();
  $('select[name="dependencies"]').chosen();

  $('#requirement_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $("h1").text("requirement: " + $('#id_name').val());
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "requirement", "requirement", response.data.current_id);
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });
});

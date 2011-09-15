$(function() {
  $('#organization_form').ajaxForm({
    success: function(response) {
      $.shortcuts.hideErrors();
      $.notification.hide();
      if ( ! response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data);
      } else {
        $.notification.notice(response.message);
      }
    }
  });
});

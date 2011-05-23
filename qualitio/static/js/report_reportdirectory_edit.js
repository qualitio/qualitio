$(function() {
  $('#reportdirectory_form').ajaxForm({ 
    beforeSubmit: $.shortcuts.hideErrors,
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "reportdirectory");
      }
    },
  });
});

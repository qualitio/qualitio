$(document).ready(function(){
  $('a[href="/account/profile/"]').addClass('active');

  $('#organization_member_profile_form').ajaxForm({
    success: function(response){
      if (! response.success) {
	$.notification.error(response.message);
	$.shortcuts.showErrors(response.data)
      } else {
	$.notification.notice(response.message);
	document.location.reload();
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
      $.notification.hide();
    }
  });
});

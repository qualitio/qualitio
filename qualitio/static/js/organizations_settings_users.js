$(function() {
  $('.delete-button').checkboxButton();

  $('#organization_users_form, #organization_new_member_form').ajaxForm({
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

  $('.add-new-member').click(function() {
    $('.new-user-form').show();
    $('[name="new-user-form-visible"]').val('true');
    $('.add-new-member').hide();
    $('.add-new-member-cancel').show();
  });

  $('.add-new-member-cancel').click(function() {
    $('.new-user-form').hide();
    $('[name="new-user-form-visible"]').val('false');
    $('.add-new-member').show();
    $('.add-new-member-cancel').hide();
    $.shortcuts.hideErrors();
    $.notification.hide();
  });

  $('.add-new-member-cancel').button().hide();
});

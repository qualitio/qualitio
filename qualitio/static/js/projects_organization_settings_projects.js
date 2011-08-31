$(function() {
  $('#organization_projects_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });


  $( "#projects_list" ).height($('.application-view-content.panel').height() - 50);
  $( "#projects_list" ).accordion({
    fillSpace: true,
  });

  $('.add.button').click( function() {
    var $settings_block = $(this).parents('.settings-block');

    var $formset = $settings_block.find('.formset');
    var $formset_TOTAL_FORMS = $formset.find('[id$=TOTAL_FORMS]');
    var TOTAL_FORMS = parseInt($formset_TOTAL_FORMS.val());
    $formset_TOTAL_FORMS.val(TOTAL_FORMS+1);

    var empty_form_html = $settings_block.find('.empty-form')
      .clone()
      .html()
      .replace(/__prefix__/g, TOTAL_FORMS);

    $(empty_form_html).appendTo($formset).show();
  });
});


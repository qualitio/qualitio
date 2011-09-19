(function($) {
  $.accordion = {
    previousActiveTabKey: '__previous_accordion_active_tab',

    parseTabIndex: function(text) {
      var match = text.match(/project-accordion-tab-(\d+)/);
      if (match.length === 2) {
	return parseInt(match[1], 10);
      }
      return null;
    },

    popPreviousActiveTab: function() {
      var previous = $.cookie($.accordion.previousActiveTabKey);
      if (previous !== null) {
	$.cookie($.accordion.previousActiveTabKey, null);
      }
      return previous === null ? previous : parseInt(previous, 10);
    },

    saveActiveTab: function() {
      var active = $('#projects_list').accordion('option', 'active');
      $.cookie($.accordion.previousActiveTabKey, active);
      return active;
    },

    trySetPreviousTab: function() {
      var previous = $.accordion.popPreviousActiveTab();
      if (previous !== null) {
	$('#projects_list').accordion('option', 'active', parseInt(previous, 10));
      }
      return previous;
    }
  };
})(jQuery);


$(function() {
  $('.organization_projects_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);

	var projects_tab_id = 2
	$('#tabs').tabs('load', projects_tab_id);
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });

  var deleteClickCallback = function($this, event) {
    var field = $this.parents('.field-settings');
    if(field.hasClass('removed')) {
      field.removeClass('removed');
    } else {
      $this.css('pointer-events', 'auto');
      field.addClass('removed');
    }
  };

  var colorPickerOptions = {
    onSubmit: function(hsb, hex, rgb, el){
      $(el).val(hex);
      $(el).css('background', '#' + hex);
      $(el).ColorPickerHide();
    },
    onBeforeShow: function () {
      $(this).ColorPickerSetColor(this.value);
      $(this).css('background', '#' + this.value);
    }
  };

  $('.delete-button').checkboxButton({callback: deleteClickCallback});
  $('.agree-button').checkboxButton();
  $('[name$="color"]').each(function(){
    $(this).css('background', '#' + $(this).val());
  })
  $('[name$="color"]').addClass('color-picker');
  $('[name$="color"]').ColorPicker(colorPickerOptions);

  $( "#projects_list" ).height($('.application-view-content.panel').height() - 50);
  $( "#projects_list" ).accordion({
    fillSpace: true,
    change: function(event, ui) {
      $.accordion.saveActiveTab($(ui.newContent).attr('id'));
    }
  });
  $.accordion.trySetPreviousTab();

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

    var $elem = $(empty_form_html).appendTo($formset).show();
    $('.delete-button', $elem).checkboxButton({callback: deleteClickCallback});
    $('.agree-button', $elem).checkboxButton();
    $('[name$="color"]').ColorPicker(colorPickerOptions);
  });
});


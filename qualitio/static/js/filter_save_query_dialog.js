/* Simple small dialog box implemented using jquery.blockUI.js
 * plugin.
 * Box looks like this:
 * ============================
 * | <info - or - errors>     |
 * | .. text field .......... |
 * | Save              Cancel |
 * ============================
 */


var saveQueryFormData = function() {
  var data = _.map($('div.blockUI #save-query-form-box input'), function(item){
    var item = $(item);
    return {
      name: item.attr('name'),
      value: item.attr('value')
    };
  });
  data.push({
    name: "csrfmiddlewaretoken",
    value: $('input[name="csrfmiddlewaretoken"]').val()
  });
  return data;
};


var filterFormData = function() {
  return _.select($('.filter-form').formToArray(), function(item) {
    return ! /control-/.test(item.name);
  });
};

(function($) {

  var onCancelEvent = function() {
    $('.blockUI.blockOverlay').unbind('click');
    $.unblockUI();
    $.shortcuts.hideErrors();
    $('#save-query-form-box input').val('');
    $('#save-query-form-box .info').show();
  };

  var onSaveQueryClick = function() {
    var box = $('#save-query-form-box');
    var self = $(this);
    var offset = self.offset();
    $.blockUI({
      message: box,
      css: {
	cursor: 'default',
	top: offset.top + self.height(),
	left: offset.left,
	width: '400px',
	height: '80px'
      }
    });
    $('div.blockUI #save-query-form-box input[name="savequery-query"]').val($.param(filterFormData()));
    $('input', $(box)).click();
    $('.blockUI.blockOverlay').click(onCancelEvent);
    return false;
  };

  var onSaveFormClick = function() {
    $.post('/project/' + PROJECT_SLUG + '/' + APP_NAME + '/savefilter/', saveQueryFormData(), function(data) {
      if ( ! data.success) {
	$('#save-query-form-box .info').hide();
	$.shortcuts.hideErrors();
	$.shortcuts.showErrors(data.errors);
      } else {
	$.notification.notice('Query saved');
	onCancelEvent();
      }
    });
    return false;
  };

  $.saveQueryDialog = function() {
    $('#save-button').click(onSaveQueryClick);
    $('#save-form-button').click(onSaveFormClick);
    $('#cancel-form-button').click(onCancelEvent);
  };

})(jQuery);

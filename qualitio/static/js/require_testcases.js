/* This file assumes that URLS variable is defined
 * somewere in templates. URLS should contains:
 * - URLS.connected_testcases
 * - URLS.connect_testcases
 * - URLS.available_testcases
 * - URLS.disconnect_testcases
 */

(function($) {
  $.fn.idsList = function() {
    var result = [];
    $(this).each(function(index, item){
      result.push($(item).attr('id').split('-')[1]);
    });
    return result;
  };

  $.refreshTable = function(tableInstance) {
    tableInstance.fnClearTable(0);
    tableInstance.fnDraw();
  };
})(jQuery);


$(document).ready(function() {
  var defaults = {
    "sScrollY": "200px",
    "bPaginate": true,
    "bInfo": true,
    "sDom": 'iprt<"bottom clearfix"lf><"clear">',
    "bProcessing": true,
    "bServerSide": true,
    "sPaginationType": "full_numbers"
  };

  var connected_testcases = $(".connected-testcases table.display").dataTable($.extend(defaults, {
    "aoColumnDefs": [
      {"bSortable": false, "sWidth": "4px", "aTargets": [0]},
      {"bSearchable": false, "aTargets": [0, 1, 5]},
      {"bSearchable": true, "aTargets": [2, 3, 4]}
    ],
    "sAjaxSource": URLS.connected_testcases
  }));

  var available_testcases = $(".available-testcases table.display").dataTable($.extend(defaults, {
    "aoColumnDefs": [
      {"bSortable": false, "sWidth": "4px", "aTargets": [0]},
      {"bSearchable": false, "aTargets": [0, 1, 5]},
      {"bSearchable": true, "aTargets": [2, 3, 4]}
    ],
    "sAjaxSource": URLS.available_testcases
  }));

  $("#remove-testcases-button").click(function() {
    $.post(URLS.disconnect_testcases, {
      testcases: $('.connected-testcases input[name="connected_testcase"]:checked').idsList(),
      csrfmiddlewaretoken: $('form input[name="csrfmiddlewaretoken"]').val()
    }, function(response) {
      $.notification[response.success ? 'notice' : 'error'](response.message);
      if (response.success) {
	$.refreshTable(available_testcases);
	$.refreshTable(connected_testcases);
      }
    });
  });

  $("#add-testcases-button").click( function() {
    $.post(URLS.connect_testcases, {
      testcases: $('.available-testcases input[name="available_testcase"]:checked').idsList(),
      csrfmiddlewaretoken: $('form input[name="csrfmiddlewaretoken"]').val()
    }, function(response) {
      $.notification[response.success ? 'notice' : 'error'](response.message);
      if (response.success) {
	$.refreshTable(available_testcases);
	$.refreshTable(connected_testcases);
      }
    });
  });

  // items selection
  $(".connected-testcases table.display th.checkbox:first").itemsSelector({
      selector: '.connected-testcases table.display td [type="checkbox"]'
  });
  $(".available-testcases table.display th.checkbox:first").itemsSelector({
      selector: '.available-testcases table.display td [type="checkbox"]'
  });
  $(".dataTables_scrollHead").css('overflow', 'visible');
});

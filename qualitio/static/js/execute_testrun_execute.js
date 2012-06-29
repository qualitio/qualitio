$(function() {
  var selectedTestCaseRun = (function() {
    var cookieName = "execute_selected_testcaserun_id";

    return {
      exists: function() {
	var previousllySelected = $.cookie(cookieName);
	return previousllySelected !== null;
      },

      save: function(){
	var selected = $("table.display tbody tr.selected");
	if (selected.length === 1) {
	  $.cookie(cookieName, selected.attr("id"));
	}
      },

      restore: function(){
	var previousllySelected = $.cookie(cookieName);
	if (previousllySelected !== null) {
	  $("#" + previousllySelected).click();
	}
	$.cookie(cookieName, null);
      }
    }
  })();

  var testCaseRunTable = $("table.display").dataTable({
    "sScrollY": "200px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aaSorting": [
      [1, 'asc']
    ],
    "aoColumnDefs": [
      {"bSortable": false, "aTargets": [0] },
      {"sWidth": "4px", "aTargets": [0,1] },
      {"sWidth": "33px", "aTargets": [2] }
    ]
  });

  // let's sign empty "tr" elements with "dataTables_empty_row" class.
  // That because we do not want to add "hover" to "tr" with
  // "No data available in table" banner.
  $("#testcaserun-list tbody tr td.dataTables_empty").parent().each(function(){
    $(this).addClass("dataTables_empty_row");
  });

  $("#testcaserun-list tbody tr:not(.dataTables_empty_row)").hover(
    function() { $(this).addClass("hover"); },
    function() { $(this).removeClass("hover"); }
  );

  // We will toggle checkbox in the first table-td element,
  // if the element or the checkbox were clicked.
  var shouldToggleCheckbox = function(clickedElement) {
    var result = false;
    $('#testcaserun-list tbody tr').each(function(index, trRow){
      var firstTd = $('td:first', $(trRow))[0];
      var checkbox = $('td:first input[type="checkbox"]', $(trRow))[0];
      result = (clickedElement === firstTd) || (clickedElement === checkbox);
    });
    return result;
  }

  $("#testcaserun-list tbody tr:not(.dataTables_empty_row)").click(function(event) {
    if (shouldToggleCheckbox(event.target)) {
      var checkbox = $('td:first input[type="checkbox"]', $(this));
      if (checkbox[0] !== event.target)
	checkbox.attr('checked', ! checkbox.attr('checked'));
    } else {
      // remove selection from other selected row
      $("#testcaserun-list tbody tr").removeClass('selected');

      $(this).addClass('selected');
      var testcaserun_id = $(this).attr("id").split("_")[1];
      $("#testcaserun-details").load( $(this).attr("href") );
    }
  });

  // items selection
  $("table.display th.checkbox:first").itemsSelector({
      selector: "table.display td .modify"
  });
  $(".dataTables_scrollHead").css('overflow', 'visible');


  $('.action-form').hide();
  $('.actions-form #id_action').change(function(){
    $('.action-url').removeClass('current');
    $('.action-form').hide().removeClass('current');
    $('.action-url[name="' + $(this).val() + '"]').addClass('current');
    $('.action-form[name="' + $(this).val() + '"]').show().addClass('current');
  });

  $('input[name="action-submit"]').click(function(){
    var url = $('.action-url.current').val();
    var data = _.reduce($('input.table-item:checked', testCaseRunTable.fnGetNodes()), function(memo, item) {
      memo[$(item).attr('name')] = 'on';
      return memo;
    }, {});
    data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
    $('input, select, textarea', $('.action-form.current')).each(function(){
      data[$(this).attr('name')] = $(this).fieldValue()[0];
    });

    if (url !== undefined) {
      $.ajax({
    	'type': 'post',
    	'dataType': 'json',
    	'url': url,
    	'data': data,
    	'success': function(data, textStatus){
    	  if (data.success) {
	    	selectedTestCaseRun.save();
    	 	$('#notification').jnotifyAddMessage({
    	      text: data.message,
    	      type: 'success'
    	    }); 
    	    $.onrefresh.reset();
	    Backbone.history.loadUrl(document.location.hash);
    	  } else {
    	    $.shortcuts.hideErrors();
    	    
    	    if (data.message)	
    	      $('#notification').jnotifyAddMessage({
    		text: data.message,
    		type: 'error'
    	      }); 
    	    $.shortcuts.showErrors(data.data); 
    	  }
    	},
    	
    	'error':function(jqXHR, exception){
    		
    		$('#notification').jnotifyAddMessage({
            text: jqXHR.statusText,
            permanent: false,
            type: "error"
         }); 
    	}
      });

    } 
    return false;
  });

  if (selectedTestCaseRun.exists())
    selectedTestCaseRun.restore();
});

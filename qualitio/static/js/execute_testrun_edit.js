function show_response(response, statusText, xhr, $form)  { 
  if(!response.success) {
    $(response.data).each(function(i, element) {
      $("#"+element[0]+"_wrapper").addClass("ui-state-error");
      $("#"+element[0]+"_wrapper .error").append(element[1]);
    });        
    $('#notification').jnotifyAddMessage({
      text: response.message,
      permanent: false,
      type: "error"
    });
  } else {
    $('#notification').jnotifyAddMessage({
      text: response.message,
      permanent: false,
      disappearTime: 2000
    });
    hash.node = response.data.current_id; // for new created objects go to details view 
    hash.view = "details" 
    hash.update();
    $('#application-tree').jstree('refresh', "#"+response.data.parent_id+"_testrundirectory", response.data);
    
    $('#application-tree').bind("refresh.jstree", function (event, data) {
      $("#application-tree").jstree("open_node", "#"+data.args[1].parent_id+"_testrundirectory", function() {
        $("#application-tree").jstree("deselect_node", "#"+data.args[1].parent_id+"_testrundirectory");
        $("#application-tree").jstree("select_node", "#"+data.args[1].current_id+"_testrun")
      });
    });
  }
}

function clear_errors(arr, $form, options) { 
  $('.field-wrapper').removeClass('ui-state-error');
  $('.field-wrapper .error').text("");
}


$(function() {
  
  var connected_testcases = $(".display.connected-testcases").dataTable({
    "sScrollY": "230px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0],
        "sWidth": "4px", "aTargets": [0]}
    ]
  });
  
  var available_testcases = $(".display.available-testcases").dataTable({
    "sScrollY": "230px",
    "bPaginate": false,
    "sDom": 'rt<"bottom clearfix"lfp><"clear">',
    "aoColumnDefs": [
      { "bSortable": false, "aTargets": [0],
        "sWidth": "4px", "aTargets": [0]}
    ]
  });
  
  $('#testrun_form').ajaxForm({ 
    success: show_response,
    beforeSubmit: clear_errors,
    data: $.extend({},
                   $('input', available_testcases.fnGetNodes()).serializeJSON(), 
                   $('input', connected_testcases.fnGetNodes()).serializeJSON())
  });
  
});

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
    $('#application-tree').jstree('refresh',-1);
  }
}

function clear_errors(arr, $form, options) { 
  $('.field-wrapper').removeClass('ui-state-error');
  $('.field-wrapper .error').text("");
}

$(function() {
  $('#testrun_form').ajaxForm({ 
    success: show_response,
    beforeSubmit: clear_errors
  });
});

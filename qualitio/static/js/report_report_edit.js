function show_response(response, statusText, xhr, $form)  { 
  if(!response.success) {
    $(response.data).each(function(i, element) {
      $("#"+element[0]+"_wrapper").addClass("ui-state-error");
      $("#"+element[0]+"_wrapper .error").append(element[1]);
    });        
    
    $.notification.error(response.message);
  } else {
    $.notification.notice(response.message);

    $('#application-tree').jstree('refresh', "#"+response.data.parent_id+"_reportdirectory", response.data);

    $('#application-tree').bind("refresh.jstree", function (event, data) {
      $("#application-tree").jstree("open_node", "#"+data.args[1].parent_id+"_reportdirectory", function() {
        $("#application-tree").jstree("select_node", "#"+data.args[1].current_id+"_report", true);
      });
    });
  }
}

function clear_errors(arr, $form, options) { 
  $('.field-wrapper').removeClass('ui-state-error');
  $('.field-wrapper .error').text("");
}

$(function() {
  $('#report_form').ajaxForm({ 
    success: show_response,
    beforeSubmit: clear_errors
  });
  

  if( $('#template').height() < $('#context').height() ) {
    $('#template').height( $('#context').height() );
  } else {
    $('#context').height( $('#context').height() );
  }
  
  $('#editor').height( $('#template').height() - 29);
  
  var editor = ace.edit("editor");
  var Mode = require("ace/mode/html").Mode;
  editor.getSession().setMode(new Mode());
  editor.renderer.setShowGutter(false);
  editor.renderer.setHScrollBarAlwaysVisible(false);
  editor.renderer.setPadding(0);
  editor.renderer.setShowPrintMargin(false);
  editor.getSession().setValue($('#id_template').val());
  editor.getSession().on('change', function() {
    $('#id_template').val( editor.getSession().getValue() );
  });

});

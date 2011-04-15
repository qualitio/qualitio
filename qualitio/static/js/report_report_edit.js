setupEditor = function(id_editor) {
  var editor = ace.edit(id_editor);
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
}


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
  
  
  if(  $('#template').height() < $('#context').height() ) {
    $('#template').height( $('#context').height() );
  } else {
    $('#context').height( $('#template').height() );
  }
  $('#editor').height( $('#template').height() - 29);

  
  setupEditor("editor");

  
  $(".context-element .delete").live("click", function(){
    context_element = $(this).parents('.context-element')
    delete_checkbox = context_element.find("input[name$=DELETE]")
    if ( delete_checkbox.is(":checked") ) {
      delete_checkbox.attr("checked", false);
      context_element.removeClass("removed");
    } else {
      delete_checkbox.attr("checked", true);
      context_element.addClass("removed");
    }
  });


  $(".add-context-element").click(function(){
    new_context_element = $(".context-element.empty-form").clone().html()
      .replace(/__prefix__/g, $('.context-element:visible').length);

    $(".context-element:last").after( '<div class="context-element">' + new_context_element + "</div>");
    
    $('#id_context-TOTAL_FORMS').attr("value", $('.context-element:visible').length);

    $('#template').height( $('#context').height() );
    $('#editor').height( $('#template').height() - 29);
    
    setupEditor("editor");
  });
});

setupEditor = function() {
  $('#template').height( $('#context').height() );
  $('#id_editor').height( $('#template').height() - 37);

  var editor = ace.edit("id_editor");
  var Mode = require("ace/mode/html").Mode;
  editor.getSession().setMode(new Mode());
  editor.renderer.setHScrollBarAlwaysVisible(false);
  editor.renderer.setPadding(0);
  editor.renderer.setShowPrintMargin(false);
  editor.getSession().setValue($('#id_template').val());
  editor.getSession().on('change', function() {
    $('#id_template').val( editor.getSession().getValue() );
  });
}

setupLink = function(link) {
  if(link) {
    $("#id_link").val(document.location.protocol +"//"
                      + document.location.host + "/"
                      + "report/external/"
                      + link);
  }
}

$(function() {
  $('#report_form').ajaxForm({ 
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "reportdirectory");
        setupLink(response.data.link);
        
        $('#application-tree').bind("refresh.jstree", function (event, data) {
          $("#application-tree").jstree("open_node", "#"+data.args[1].parent_id+"_reportdirectory", function() {
            $("#application-tree").jstree("select_node", "#"+data.args[1].current_id+"_reportdirectory");
            $("#application-tree").jstree("deselect_node", "#"+data.args[1].parent_id+"_report");
            document.location.hash = '#report/'+ data.args[1].current_id +"/edit/";
          });
        });

        
      }
      setupEditor();
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
      setupEditor();
    }
  });
  
  setupEditor();
  setupLink($("#id_link").val());
  
  $(".context-element .delete").die(); 
  $(".context-element .delete").live("click", function(){
    context_element = $(this).parents('.context-element')
    delete_checkbox = context_element.find("input[name$=DELETE]")
    if ( delete_checkbox.is(":checked") ) {
      delete_checkbox.removeAttr("checked");
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
    
    setupEditor();
  });
});

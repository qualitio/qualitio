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
  setupEditor();
  setupLink($("#id_link").val());

  // make sure the editor will be refreshed on tree / window size changes
  $(window).resize(setupEditor);
  $.onTreeResize(setupEditor);

  $(".context-element .delete-button").die();
  $(".context-element .delete-button").live("click", function(event){
    var context_element = $(this).parents('.context-element');
    if (context_element.hasClass('removed')) {
      context_element.removeClass('removed');
    } else {
      $(this).css('pointer-events', 'auto');
      context_element.addClass('removed');
    }

    var checkbox = context_element.find("input[name$=DELETE]")
    if (checkbox.length > 0 && event.target !== checkbox[0]) {
      checkbox.attr('checked', ! checkbox.is(":checked"));
    }
  });

  $(".add-context-element").click(function(){
    new_context_element = $(".context-element.empty-form").clone().html()
      .replace(/__prefix__/g, $('.context-element:visible').length);

    $(".context-element:last").after( '<div class="context-element">' + new_context_element + "</div>");

    $('#id_context-TOTAL_FORMS').attr("value", $('.context-element:visible').length);

    setupEditor();
  });

  $('#report_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $("h1").text("report: " + $('#id_name').val());
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "reportdirectory", "report", response.data.current_id);
	Backbone.history.loadUrl(document.location.hash);
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });

});

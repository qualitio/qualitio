$(function() {
  last_textarea = null;
  last_textarea_pointer = null;

  $('textarea').focusout( function() {
    last_textarea = this;
  });

  $('.add-translation').click( function() {
    $(last_textarea).text($(this).text());
  });

  $('.add-this-attachment').click( function() {
    $(last_textarea).text("#"+$(this).text());
  });

  $( "#dialog" ).dialog( "destroy" );

  $( "#dialog-attachmets" ).dialog({
    resizable: false,
    autoOpen: false,
    minHeight: 240,
    minWidth: 800,
    modal: true,
    position: ['center',100],
    buttons: { 
      Cancel: function() {
        $( this ).dialog( "close" )
      }
    }
  });

  $( "#dialog-translations" ).dialog({
    resizable: false,
    autoOpen: false,
    minHeight: 240,
    minWidth: 800,
    modal: true,
    position: ['center',100],
    buttons: { 
      Cancel: function() {
        $( this ).dialog( "close" )
      }
    }
  });

  $('input[type=checkbox][name$=DELETE]').live('click', function() {
    step = $(this).parents('.step');
    if(step.hasClass('removed')) {
      step.removeClass('removed');
    } else {
      $(this).css('pointer-events', 'auto');
      step.addClass('removed');
    }
  });
  
  // TODO: again remove double load
  $('.add-step').die('click');
  $('.add-step').live('click', function() {
    new_step = $('.step.template').clone();
    step_count = $('.step:visible').length;

    if( $(this).attr("id") == "add-step-0" ) {
      $(this).after(new_step.removeClass("template")); 
    } else { 
      $(this).parents('.step').after(new_step.removeClass("template")); 
    }

    $('.step:visible').each( function(i) {
      $(this).find("[name^=steps]").each(function() {
        element_id = $(this).attr("id").replace(/(.+\-)(__prefix__)(\-.+)/ig,"$1"+step_count+"$3");
        element_name = $(this).attr("name").replace(/(.+\-)(__prefix__)(\-.+)/ig,"$1"+step_count+"$3");
        $(this).attr("id", element_id);
        $(this).attr("name", element_name);
      });

      title = $(this).find("h2").text().replace(/^Step +([0-9]+)/i, "Step "+(i+1));
      $(this).children("h2").text(title);
      $(this).find('input[name$=sequence]').attr('value', i);
    });
    $('#id_steps-TOTAL_FORMS').attr("value", parseInt($('#id_steps-TOTAL_FORMS').attr("value"))+1);
  });

  $('.add-attachment').click( function() {
    $( "#dialog-attachmets" ).dialog('open');
  });

  $('.add-translation').click( function() {
    $( "#dialog-translations" ).dialog('open');
  });

  $('#testcase_form').ajaxForm({
    success: function(response){
      if ( ! response.success) {
        $.notification.error(response.message);
	$.shortcuts.showErrors(response.data);
      } else {
	$.notification.notice(response.message);
	$('#application-tree').jstree('refresh', "#"+response.data.parent_id+"_testcasedirectory", response.data);

	$('#application-tree').bind("refresh.jstree", function (event, data) {
          $("#application-tree").jstree("open_node", "#"+data.args[1].parent_id+"_testcasedirectory", function() {
            $("#application-tree").jstree("deselect_node", "#"+data.args[1].parent_id+"_testcasedirectory");
            $("#application-tree").jstree("select_node", "#"+data.args[1].current_id+"_testcase")
            document.location.hash = '#testcase/'+ data.args[1].current_id +"/edit/";
          });
	});
      }
    },
    beforeSubmit: function(){
      $.shortcuts.hideErrors();
    }
  });
});

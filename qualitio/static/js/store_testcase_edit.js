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

  // TODO related with page reloading, fix page reloading to happen once 
  $('input[type=checkbox][name$=DELETE]').die('click'); 
  $('input[type=checkbox][name$=DELETE]').live('click', function() {
    step = $(this).parents('.step');
    if(step.hasClass('removed')) {
      step.removeClass('removed');
    } else {
      $(this).css('pointer-events', 'auto');
      step.addClass('removed');
    }
  });

  // TODO related with page reloading, fix page reloading to happen once 
  $('.add-step').die('click'); 
  $('.add-step').live('click', function() {
    initial_form = parseInt($('#id_testcasestep_set-INITIAL_FORMS').attr("value"));

    new_step = $('.step.template').clone();
    
    new_step.find("[name^=testcasestep_set]").each( function() { 
      element_id = $(this).attr("id").replace(/id_testcasestep_set\-(__prefix__)/, "id_testcasestep_set-"+(initial_form));
      element_name = $(this).attr("name").replace(/testcasestep_set\-(__prefix__)/, "testcasestep_set-"+(initial_form));
      $(this).attr("id", element_id);
      $(this).attr("name", element_name);
    });

    new_step.find(".field-wrapper").each( function() {
      element_name = $(this).attr("id").replace(/(__prefix__)/, initial_form);
      $(this).attr("id", element_name);
    });

    if( $(this).attr("id") == "add-step-0" ) {
      $(this).after(new_step.removeClass("template")); 
    } else { 
      $(this).parents('.step').after(new_step.removeClass("template")); 
    }

    $('.step:visible').each( function(i) {
      title = $(this).find("h2").text().replace(/^Step +([0-9]+)/i, "Step "+(i+1));
      $(this).children("h2").text(title);
      $(this).find('input[name$=sequence]').attr('value', i);
    });
    $('#id_testcasestep_set-TOTAL_FORMS').attr("value", parseInt($('#id_testcasestep_set-TOTAL_FORMS').attr("value"))+1);
  });

  $('.add-attachment').click( function() {
    $( "#dialog-attachmets" ).dialog('open');
  });

  $('.add-translation').click( function() {
    $( "#dialog-translations" ).dialog('open');
  });
  
  function success(response, statusText, xhr, $form)  { 
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
  
  $('#testcase_form').ajaxForm({ 
    success: success,
    beforeSubmit: clear_errors
  });
});

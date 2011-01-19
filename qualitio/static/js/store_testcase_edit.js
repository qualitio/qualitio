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

  $('.add-step').live('click', function() {
    new_step = $('.step.template').clone();
    step_count = $('.step:visible').length;

    if( $(this).attr("id") == "add-step-0" ) {
      $(this).after(new_step.removeClass("template")); 
    } else { 
      $(this).parents('.step').after(new_step.removeClass("template")); 
    }

    $('.step:visible').each( function(i) {
      $(this).find("[name^=testcasestep_set]").each(function() {
        element_id = $(this).attr("id").replace(/(.+\-)(__prefix__)(\-.+)/ig,"$1"+step_count+"$3");
        element_name = $(this).attr("name").replace(/(.+\-)(__prefix__)(\-.+)/ig,"$1"+step_count+"$3");
        $(this).attr("id", element_id);
        $(this).attr("name", element_name);
      });

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
        filed_wrapper = $("[name="+element[0]+"]").parent(".field-wrapper");
        filed_wrapper.addClass("ui-state-error");
        filed_wrapper.find(".error").append(element[1]);
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

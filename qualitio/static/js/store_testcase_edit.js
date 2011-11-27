$(function() {
  var getFormsCount = function() {
    return parseInt($('#id_steps-TOTAL_FORMS').val(), 10);
  };

  var addStep = function(container) {
    /* container is the HTML element where new element should be placed after
     */
    $(container).after($('.step.template').clone().removeClass("template"));
    $('#id_steps-TOTAL_FORMS').val(getFormsCount() + 1);
    var nextFormNum = getFormsCount() - 1;

    $('.step:visible').each(function(i) {
      var step = $(this);
      var title = step.find("h2").text().replace(/^Step +([0-9]+)/i, "Step " + (i + 1));

      step.children("h2").text(title);
      step.find('input[name$=sequence]').val(i);
      step.find("[name^=steps]").each(function() {
	var input = $(this);
	input.attr({
	  "id": input.attr("id").replace(/(.+\-)(__prefix__)(\-.+)/ig,"$1" + nextFormNum + "$3"),
	  "name": input.attr("name").replace(/(.+\-)(__prefix__)(\-.+)/ig,"$1" + nextFormNum + "$3")
	});
      });
    });
  }

  var last_textarea = null;
  var last_textarea_pointer = null;

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

  $('.step .delete-button').die('click');
  $('.step .delete-button').live('click', function(event) {
    var step = $(this).parents('.step');
    if(step.hasClass('removed')) {
      step.removeClass('removed');
    } else {
      $(this).css('pointer-events', 'auto');
      step.addClass('removed');
    }

    // Check the button was clicked not the checkbox then
    // select checkbox. If the checkbox was clicked it's ok.
    var checkbox = $('input[type=checkbox][name$=DELETE]', $(this));
    if (checkbox.length > 0 && event.target !== checkbox[0]) {
      checkbox.attr('checked', ! checkbox.attr('checked'));
    }
  });

  $('.add-step').die('click');
  $('.add-step').live('click', function() {
    if ($(this).attr("id") === "add-step-0") {
      addStep($(this));
    } else {
      addStep($(this).parents('.step'));
    }
  });

  $('.add-attachment').click( function() {
    $( "#dialog-attachmets" ).dialog('open');
  });

  $('.add-translation').click( function() {
    $( "#dialog-translations" ).dialog('open');
  });

  $('#testcase_form').ajaxForm({
    success: function(response){
      if (!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data);
      } else {
        $("h1").text("test case: " + $('#id_name').val());
        $.notification.notice(response.message);
        $.shortcuts.reloadTree(response.data, "testcasedirectory",
                               "testcase", response.data.current_id);
	Backbone.history.loadUrl(document.location.hash);
      }
    },
    beforeSubmit: function(){
      $.shortcuts.hideErrors();
    }
  });

  $('select[name="parent"]').chosen();
  $('select[name="requirement"]').chosen();
});

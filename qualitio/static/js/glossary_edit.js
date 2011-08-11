$(function() {
  $('#word_form').ajaxForm({
    success: function(response) {
      if(!response.success) {
        $.notification.error(response.message);
        $.shortcuts.showErrors(response.data)
      } else {
        $.notification.notice(response.message);
        $("h1").text("word: "+response.data.name);
        $('#application-tree').load("/project/" + PROJECT_SLUG + "/glossary/ajax/word/list/", function() {
	  $(".word-search input").livefilter({selector:'#application-tree a'});
	});
        document.location.href = "#word/"+response.data.id+"/edit/";
      }
    },
    beforeSubmit: function() {
      $.shortcuts.hideErrors();
    }
  });

});

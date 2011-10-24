(function($){

  var onCancelEvent = function() {
    $('.blockUI.blockOverlay').unbind('click');
    $.unblockUI();
    $('#queries').remove();
    return false;
  };

  var renderQueries = function(queries) {
    var html = '';
    html += '<div class="items">';
    if (queries.length === 0) {
      html += '<div class="item">';
      html += '<i> no saved queries </i>';
      html += '</div>';
    } else {
      $.each(queries, function(index, item) {
	html += '<div class="item">';
	html += '<a href="' + item.url + '" class="link">' + item.name + '</a>';
	html += '<div style="clear:both;"></div>';
	html += '</div>';
      });
    }
    html += '</div>';
    return html;
  };

  var onSavedQueriesClick = function() {
    $.getJSON('/project/' + PROJECT_SLUG + '/' + APP_NAME + '/savedqueries/', {}, function(data) {
      var size = {
	width: 600,
	height: (35 * (data.queries.length + 1)) + 30,
      };

      var position = {
	top: $('#application-menu').offset().top + 30,
	left: ($('#application-menu').width() / 2) - (size.width / 2)
      };

      var queries = $('<div id="queries"><h2>Saved queries</h2></div>');
      $.blockUI({
	message: queries,
	css: {
	  cursor: 'default',
	  top:  position.top + 'px',
	  left: position.left + 'px',
	  width: size.width + 'px',
	  height: size.height + 'px'
	}
      });
      queries.append(renderQueries(data.queries));
      $('.blockUI.blockOverlay').click(onCancelEvent);
    });
    return false;
  };

  $.savedQueriesDialog = function() {
    $('#saved-queries-button').click(onSavedQueriesClick);
  };

})(jQuery);

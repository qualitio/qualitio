var tree_ratio = 0;
var view_ratio = 0;

(function($){
  var onTreeResizeCallbacks = [];
  
  $.onTreeResize = function(func){
    onTreeResizeCallbacks.push(func);
  }

  function triggerTreeResize(){
    $.each(onTreeResizeCallbacks, function(index, callback){
      callback();
    });
  }

  $.fn.resize_tree = function() {
    $(this).parent().resizable({
      handles: 'e',
      maxWidth: document.width/2,
      ghost: true,
      stop: function(event, ui) {
	$('#application-view').parent().width(document.body.clientWidth - $(this).width());
	tree_ratio = $('#application-tree').parent().width() / $(window).width();
	view_ratio = $('#application-view').parent().width() / $(window).width();
	triggerTreeResize();
      }
    });
  }
})(jQuery);

$(document).ready(function() {
  $('#application-tree').resize_tree();
});

$(window).resize(function() {
  $('#application-tree').parent().width( $(window).width() * tree_ratio - 1);
  $('#application-view').parent().width( $(window).width() * view_ratio - 1);
  $('#application-tree').resize_tree();
});

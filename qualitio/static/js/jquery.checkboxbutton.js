/* jQuery checkbox button - works just like build-in "button"
 * plugin for checkboxed but it keeps checkbox visible and clickable.
 *
 * Usage:
 * you ^^need^^ to put checkbox in some kind of container (eg, div)
 *
 * ...
 * <div class="button"><input type="checkbox" /></div>
 * ...
 *
 * $('.button').checkboxButton({
 *    callback: function($this, event){},         // this is default
 *    checkboxSelector: 'input[type="checkbox"]'  // this is default
 * })
 */
(function($){
  $.fn.checkboxButton = function(settings){
    var $this = $(this);
    var opts = $.extend({
      'callback': function($this, event){},
      'checkboxSelector': 'input[type=checkbox]'
    }, settings);

    return $(this).each(function(index, item){
      $(item).click(function(event) {
	opts.callback($(this), item);

	// Check the button was clicked not the checkbox then
	// select checkbox. If the checkbox was clicked it's ok.
	var checkbox = $(opts.checkboxSelector, $(this));
	if (checkbox.length > 0 && event.target !== checkbox[0]) {
	  checkbox.attr('checked', ! checkbox.attr('checked'));
	}
      });
    });
  };
})(jQuery);

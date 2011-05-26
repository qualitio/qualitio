(function($){
    var Switcher = (function(selector){
	return {
	    all: function(){ $(selector).attr('checked', true); },
	    invert: function(){
		$(selector).each(function(){
		    $(this).attr('checked', ! $(this).attr('checked'));
		});
	    },
	    none: function(){ $(selector).attr('checked', false); }
	}
    });

    var render = {
	menu: function(menu){
	    var html = '';
	    html += '<div class="menu" style="' + menu.style + '">';
	    $.each(menu.items, function(index, item){
		html += render.menuItem(item);
	    });
	    html += '</div>';
	    return html;
	},
	menuItem: function(meta){
	    var html = '';
	    html += '<div class="item" style="' + meta.style + '" name="' + meta.name + '">';
	    html += meta.text;
	    html += '</div>';
	    return html;
	},
	prettyButton: function(){
	    var html = '';
	    html += '<div class="select-btn ui-state-default" style="padding-left:3px;">';
	    html += '<span class="ui-icon ui-icon-triangle-1-s"></span>';
	    html += '<div style="clear:both;"></div>';
	    html += '</div>';
	    return html;
	}
    };

    $.fn.itemsSelector = function(options){
	var opts = $.extend({
	    menuStyle: 'display:none;position:absolute;padding:1px;background: #fff;border: 1px solid #ccc;z-index: 100;',
	    menuItemStyle: 'padding:0px 5px 0px 5px;border:1px solid #fff;cursor: pointer;',
	    menuItemHoverStyle: 'padding:0px 5px 0px 5px;background: #ccc;border: 1px solid #aaa;',
	    selector: null
	}, options);

	return $(this).each(function(index, selectorContainer){
	    $(selectorContainer).append(render.prettyButton());
	    $(selectorContainer).append(render.menu({
		'style': opts.menuStyle,
		'items': [
		    {'style': opts.menuItemStyle, 'name': 'all', 'text': 'All'},
		    {'style': opts.menuItemStyle, 'name': 'none', 'text': 'None'},
		    {'style': opts.menuItemStyle, 'name': 'invert', 'text': 'Invert'},
		]
	    }));
	    var switcher = Switcher(opts.selector);
	    var menu = $('.menu', $(selectorContainer));
	    var selectButton = $('.select-btn', $(selectorContainer));

	    function onActivate(event, ui){
		menu.show();
		menu.position({
		    my: "left top",
		    at: "left bottom",
		    of: selectButton,
		    offset: "0 -1",
		    collision: "fit"
		});
		selectButton.addClass('ui-state-focus');
		selectButton.unbind('click');
		selectButton.click(onDeactivate);
	    }

	    function onDeactivate(event, ui){
		menu.hide();
		selectButton.removeClass('ui-state-focus');
		selectButton.unbind('click');
		selectButton.click(onActivate);
	    }

	    selectButton.click(onActivate);

	    $('.item', menu).click(function(){
		onDeactivate();
		switcher[$(this).attr('name')]();
	    });

	    $('.item', menu).hover(
		function(){$(this).attr('style', opts.menuItemHoverStyle);},
		function(){$(this).attr('style', opts.menuItemStyle);}
	    );
	});
    };
})(jQuery);

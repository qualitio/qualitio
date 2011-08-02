var sortParamConverter = function(column_names){
    // mapping between jQuery Data Table and django sort direction notation
    var directions = {
	asc: '',
	desc: '-'
    };
    var column_names = column_names;
    return {
	// eg: -id => [id_col_index, "desc"] or id => [id_col_index, "asc"]
	// output format is determined by jQuery data table plugin
	fromDjango: function(txt){
	    var sort_dir = txt.match(/^-/) ? 'desc' : 'asc';
	    var starting_position = sort_dir === 'desc' ? 1 : 0;
	    var sort_column = txt.slice(starting_position);
	    var sort_column_index = column_names.indexOf(sort_column);
	    return [sort_column_index, sort_dir];
	},

	// eg: sorting_asc, name => name or sorting_desc, name => -name
	toDjango: function(txt, name) {
	    var sorting_dir = txt.split('_')[1];
	    if (sorting_dir === undefined) {
		sorting_dir = 'asc';
	    }
	    return directions[sorting_dir] + name;
	}
    };
}(COLUMN_NAMES); // COLUMN_NAMES should be provided in template

// returns new state for the current one
var tableHeaderClassCycle = function(){
    var stateToNextState = {
	'sorting': 'sorting_asc',
	'sorting_asc': 'sorting_desc',
	'sorting_desc': 'sorting_asc'
    }
    var defaultState = 'sorting_asc'; // in case of undefined
    return {
	next: function(currentState){
	    var nextState = stateToNextState[currentState];
	    if (nextState === undefined) {
		nextState = defaultState;
	    }
	    return nextState;
	}
    }
}();

// 'id' is a-href link rendered on server side
var parseIntFromLink = function(html){
    return parseInt($('a', html).text(), 10);
}

jQuery.fn.dataTableExt.oSort['int-in-link-asc'] = function(x, y) {
    var x = parseIntFromLink(x), y = parseIntFromLink(y);
    return ((x < y) ?  1 : ((x > y) ? -1 : 0));
};
jQuery.fn.dataTableExt.oSort['int-in-link-desc'] = function(x, y) {
    var x = parseIntFromLink(x), y = parseIntFromLink(y);
    return ((x < y) ?  1 : ((x > y) ? -1 : 0));
};

$(document).ready(function() {
    $('input[type="submit"], .button').button();
    $('.control-select').change(function(){
	$('.filter-form').submit();
    });

    $('input[name$="from_date"], input[name$="to_date"], input[name$="date"]').datepicker({
	showWeek: true,
	dateFormat: DATE_FORMAT
    });

    $('.remove-filter-button').click(function(){
	$('input[type="checkbox"]', $(this)).attr('checked', true);
	$('.filter-form').submit();
    });

    $('#id_onpage').change(function(){
	$('.filter-form').submit();
    });

    var filterTable = $("table.display").dataTable({
	"bPaginate": false,
	"bFilter": false,
	"bInfo": false,
	"aaSorting": [sortParamConverter.fromDjango(
	    $('.filter-form input[name="sort"]').val()
	)],
	"bAutoWidth": false,
	"aoColumnDefs": [
	    { "sWidth": "10px", "asSorting":[], "aTargets": [0] },
	    { "sWidth": "10px", "sType": "int-in-link", "aTargets": [ 1 ] },
            { "sWidth": '300px', "aTargets": [2, 3]}
	]
    });

    // prevent default bahaviour of sorting
    $('table.display thead th').unbind('click');

    // adding just a part of previous behaviour
    $('table.display thead th:not([name="checkbox"])').click(function(){
	$(this).attr('class', tableHeaderClassCycle.next($(this).attr('class')));
    });

    $('table.display thead th:not([name="checkbox"])').click(function(){
	$('.filter-form input[name="sort"]').val(sortParamConverter.toDjango(
	    $(this).attr('class'),
	    $(this).attr('name')
	));
	$('.filter-form').submit();
    });

    // make sure to be NOT TAKE 'table-item:checked' elements into account
    $('.filter-form').submit(function(){
	$('input.table-item:checked').attr('checked', false);
    });

    // actions
    $('input.table-item').parent().click(function(event){
	if (event.target === this) {
	    var checkbox = $('input[type="checkbox"]', $(this));
	    checkbox.attr('checked', !checkbox.attr('checked'));
	}
    });

    $('.action-form').hide();
    $('.actions-form #id_action').change(function(){
	$('.action-url').removeClass('current');
	$('.action-form').hide().removeClass('current');
	$('.action-url[name="' + $(this).val() + '"]').addClass('current');
	$('.action-form[name="' + $(this).val() + '"]').show().addClass('current');
    });

    $('input[name="action-submit"]').click(function(){
	var url = $('.action-url.current').val();
	var data = _.reduce($('input.table-item:checked', filterTable.fnGetNodes()), function(memo, item){
	    memo[$(item).attr('name')] = 'on';
	    return memo;
	}, {});
	data['csrfmiddlewaretoken'] = $('input[name="csrfmiddlewaretoken"]').val();
	$('input, select, textarea', $('.action-form.current')).each(function(){
	    data[$(this).attr('name')] = $(this).fieldValue()[0];
	});

	if (url !== undefined) {
	    $.ajax({
		'type': 'post',
		'dataType': 'json',
		'url': url,
		'data': data,
		'success': function(data, textStatus){
		    if (data.success) {
			$('#notification').jnotifyAddMessage({
			    text: 'Action done!',
			    type: 'success'
			});
			$.onrefresh.reset();
			window.location = window.location;
		    } else {
			$('#notification').jnotifyAddMessage({
			    text: data.message,
			    type: 'error'
			});
			$.shortcuts.showErrors(data.data);
		    }
		}
	    });
	}

	return false;
    });

    $('table.display th[name="checkbox"]').itemsSelector({
	selector: '.table-item'
    });

    $.onrefresh.bind(function() {
	$('.actions-form #id_action').val("");
    });
});

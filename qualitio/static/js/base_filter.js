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


$(document).ready(function() {
    $('input[type="submit"], .button').button();
    $('.control-select').change(function(){
	$('.filter-form').submit();
    });

    $('input[name$="from_date"], input[name$="to_date"]').datepicker({
	showWeek: true ,
	dateFormat: DATE_FORMAT
    });

    $('.remove-button').click(function(){
	$('input[type="checkbox"]', $(this)).attr('checked', true);
	$('.filter-form').submit();
    });

    $('#id_onpage').change(function(){
	$('.filter-form').submit();
    });

    $("table.display").dataTable({
	"bPaginate": false,
	"bFilter": false,
	"sWidth": "4px", "aTargets": [0],
	"aoColumnDefs": [ { "sWidth": "4px", "aTargets": [0,1] } ],
	"bInfo": false,
	"aaSorting": [sortParamConverter.fromDjango(
	    $('.filter-form input[name="sort"]').val()
	)],
        "aoColumns" : [
            { sWidth: '5px'  },
            { sWidth: '300px' },
            { sWidth: '300px' },
            { sWidth: '120px' }
        ]
    });

    // prevent default bahaviour of sorting
    $('table.display thead th').unbind('click');

    // adding just a part of previous behaviour
    $('table.display thead th').click(function(){
	$(this).attr('class', tableHeaderClassCycle.next($(this).attr('class')));
    });

    $('table.display thead th').click(function(){
	$('.filter-form input[name="sort"]').val(sortParamConverter.toDjango(
	    $(this).attr('class'),
	    $(this).attr('name')
	));
	$('.filter-form').submit();
    });
});

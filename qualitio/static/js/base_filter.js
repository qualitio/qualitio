$(document).ready(function() {
    $('input[type="submit"], .button').button();
    $('.control-select').change(function(){
	$('.filter-form').submit();
    });

    $('input[name$="from_date"], input[name$="to_date"]').datepicker({
	showWeek: true,
	dateFormat: DATE_FORMAT
    });

    $('.remove-button').click(function(){
	$('input[type="checkbox"]', $(this)).attr('checked', true);
	$('.filter-form').submit();
    });

    $('input.table-item').parent().click(function(event){
	if (event.target === this) {
	    var checkbox = $('input[type="checkbox"]', $(this));
	    checkbox.attr('checked', !checkbox.attr('checked'));
	}
    });

    $("table.display").dataTable({
	"bPaginate": false,
	"bFilter": false,
	"sScrollY": "450px",
	"bScrollCollapse": true,
	"sWidth": "4px", "aTargets": [0],
	"aoColumnDefs": [ { "sWidth": "4px", "aTargets": [0,1] } ]
    });
});

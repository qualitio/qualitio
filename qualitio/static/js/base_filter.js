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

    $("table.display").dataTable({
	"bPaginate": false,
	"bFilter": false,
	"sWidth": "4px", "aTargets": [0],
	"aoColumnDefs": [ { "sWidth": "4px", "aTargets": [0,1] } ],
	"bInfo": false
    });

    $('#id_onpage').change(function(){
	$('form').submit();
    });
});

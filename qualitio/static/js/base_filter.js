$(document).ready(function() {
    $('input[type="submit"], .button').button();
    $('.control-select').change(function(){
	$('.filter-form').submit();
    });
    $('input[name$="from_date"], input[name$="to_date"]').datepicker({
	showWeek: true ,
	dateFormat: DATE_FORMAT
    });
});

$(document).ready(function() {
    var filterTable = $("table.display").dataTable({
	"bPaginate": false,
	"bFilter": false,
	"sScrollY": "450px",
	"bScrollCollapse": true,
	"sWidth": "4px", "aTargets": [0],
	"aoColumnDefs": [ { "sWidth": "4px", "aTargets": [0,1] } ]
    });

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

	console.log(url);
	console.log(typeof url);
	console.log(data);

	if (url !== undefined) {
	    $.get({
		'url': 'http://127.0.0.1:8000/filter/action/execute/require/delete/',
		'dataType': 'json',
		'data': data,
		'success': function(data, textStatus){
		    if (data.success) {
			alert("Done!");
		    } else {
			alert("It's fucked!");
		    }
		}
	    });
	}

	return false;
    });
});

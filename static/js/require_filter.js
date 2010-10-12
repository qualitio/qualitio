$(function() {
    $('.action-list').change(function() {
	$('.action-parameters').hide();
	action_name = $('.action-list option:selected').attr('value');
	$('#action-'+action_name).show();
    });
});
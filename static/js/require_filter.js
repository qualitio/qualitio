$(function() {
    $('.action-list').change(function() {
	$('.action-parameters').hide();
	action_name = $('.action-list option:selected').attr('value');
	$('#action-'+action_name).show();
    });
    $( "#dialog" ).dialog( "destroy" );

    $( "#dialog-confirm" ).dialog({
	resizable: false,
	autoOpen: false,
	minHeight: 240,
	minWidth: 800,
	modal: true,
	position: ['center',100],
	buttons: {
	    "Replace elements": function() {
		$( this ).dialog( "close" );
	    },
	    Cancel: function() {
		$( this ).dialog( "close" );
	    }
	}
    });

    $('#action-replace input[type=submit]').click( function() {
    	$( "#dialog-confirm" ).dialog('open');
    });


});
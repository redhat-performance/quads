jQuery(document).ready(function($) {
	$( '#the-list #contact-bank-plugin-disable-link' ).click(function(e) {
		e.preventDefault();

		var reason = $( '#contact-bank-feedback-content .contact-bank-reason' ),
			deactivateLink = $( this ).attr( 'href' );

	    $( "#contact-bank-feedback-content" ).dialog({
	    	title: 'Quick Feedback Form',
	    	dialogClass: 'contact-bank-feedback-form',
	      	resizable: false,
	      	minWidth: 430,
	      	minHeight: 300,
	      	modal: true,
	      	buttons: {
	      		'go' : {
		        	text: 'Continue',
        			icons: { primary: "dashicons dashicons-update" },
		        	id: 'contact-bank-feedback-dialog-continue',
					class: 'button',
		        	click: function() {
		        		var dialog = $(this),
		        			go = $('#contact-bank-feedback-dialog-continue'),
		          			form = dialog.find('form').serializeArray(),
							result = {};
						$.each( form, function() {
							if ( '' !== this.value )
						    	result[ this.name ] = this.value;
						});
							if ( ! jQuery.isEmptyObject( result ) ) {
								result.action = 'post_user_feedback_contact_bank';
									$.ajax({
											url: post_feedback.admin_ajax,
											type: 'POST',
											data: result,
											error: function(){},
											success: function(msg){},
											beforeSend: function() {
												go.addClass('contact-bank-ajax-progress');
											},
											complete: function() {
												go.removeClass('contact-bank-ajax-progress');
													dialog.dialog( "close" );
													location.href = deactivateLink;
											}
									});
							}
		        	},
	      		},
	      		'cancel' : {
		        	text: 'Cancel',
		        	id: 'contact-bank-feedback-cancel',
		        	class: 'button button-primary',
		        	click: function() {
		          		$( this ).dialog( "close" );
		        	}
	      		},
	      		'skip' : {
		        	text: 'Skip',
		        	id: 'contact-bank-feedback-dialog-skip',
		        	click: function() {
		          		$( this ).dialog( "close" );
		          		location.href = deactivateLink;
		        	}
	      		},
	      	}
	    });
	});
});

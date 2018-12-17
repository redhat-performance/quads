<?php
/**
 * Comments Template
 * The area of the page that contains comments and the comment form.
 *
 * @link https://developer.wordpress.org/themes/functionality/comments/
 *
 * @package WordPress
 * @subpackage Krusze
 */
?>

<?php do_action('krusze_comments_before'); ?>

<div id="comments" class="comments-area">

	<?php do_action('krusze_comments_top'); ?>
	
	<?php 
	// If the current post is protected by a password.
	if ( post_password_required() ) : ?>
	<p class="no-password"><?php _e( 'Protected Comments: Please enter your password to view comments.', 'krusze' ); ?></p>
</div><!-- .comments-area -->
<?php 
return; 
endif; ?>

<?php if ( have_comments() ) : ?>
	<h3 id="comments-title">
		<?php 
			printf( _n( 'One Response to %2$s', '%1$s Responses to %2$s', get_comments_number(), 'krusze' ), 
				number_format_i18n( get_comments_number()), '<em>' . get_the_title() . '</em>' ); 
		?>
	</h3>
	
	<?php krusze_comment_nav(); ?>
	
	<ol class="comment-list">
		<?php	
			wp_list_comments( array(
				'avatar_size' => 56,
			) );
		?>
	</ol><!-- .comment-list -->

	<?php krusze_comment_nav(); ?>
	
<?php else : // if there are no comments
	
		// if comments are closed
		if ( ! comments_open() && get_comments_number() && post_type_supports( get_post_type(), 'comments' ) ) :
	?>
		
		<p class="no-comments"><?php _e( 'Comments are closed.', 'krusze' ); ?></p>
	
	<?php endif; // end comments_open() ?>

<?php endif; // end have_comments() ?>

	<?php 
	$comments_args = array(
		// redefine your own textarea (the comment body)
		'comment_field' => '<p class="comment-form-comment"><label for="comment">' . __( 'Comment', 'krusze' ) . ' <span class="required">*</span></label><textarea id="comment" name="comment" cols="45" rows="8" aria-required="true"></textarea></p>',
	);
	comment_form($comments_args); ?>
	
	<?php do_action('krusze_comments_bottom'); ?>
	
</div><!-- .comments-area -->

<?php do_action('krusze_comments_after'); ?>
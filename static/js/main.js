
// Navbar burger

$('.navbar-burger').click(function() {
  const $el = $(this);
  $el.toggleClass('is-active');
  $('#' + $el.data('target')).toggleClass('is-active');
});

// Notification popups

$('.notification > .delete').click(function() {
  $(this).parent().remove();
});

$('.notification')
.delay(4000)
.fadeOut(500, function() {
  $(this).remove();
});



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

// File uploads

$('.file-input').change(function(e){
  var file = e.target;
  if (file.files.length > 0) {
    $(file).next().next().text(file.files[0].name);
  }
});

// Tags switcher
var tagsSwitcherHandler = function(tag) {
  return function() {
    $(this).addClass('is-primary').siblings().removeClass('is-primary');
    $('#posts__ul > .all_posts').hide();
    $('#posts__ul > .' + tag).show();
  }
};

$('#tags__ul > a').each(function(index) {
  $('#' + $(this).attr('id')).on('click', tagsSwitcherHandler($(this).attr('id')));
});
// $('#show').on('click', function () {
//   $('.center').show()
//   $(this).hide()
// })

// $('#close').on('click', function () {
//   $('.center').hide()
//   $('#show').show()
// })

function openMessage(postid) {
  id = '#message' + postid
  //   $('.center').show()
  $(id).show()
}
function closeMessage(postid) {
  id = '#message' + postid
  $(id).hide()
}

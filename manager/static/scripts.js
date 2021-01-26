function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$('document').ready(function(){
    $('.add-comment').on('submit', function(event){
        var book_slug = $(this).attr('id')
        event.preventDefault();
        console.log(this)
        $.ajax({
            url: "/shop/add_comment_ajax/",
            headers: { "X-CSRFToken": csrftoken},
            data : {"book_slug": book_slug,
                    'new_comment': $('#comment-text').val()},
            method: 'POST',
            success: function(json) {
                console.log(json.text);
                $('#comment-text').val('');
                $('#bookdetailview').prepend('<h3 class="mb-0">' + json.text + '</h3>');
            }
        })
    });

    $('.like-comment').on('click', function(){
        let id=$(this).attr('id');
        let current_id = id.split('-')[1];
        console.log(current_id  )
        $.ajax({
            url: `/shop/add_like2comment_ajax/${ current_id }`,
            headers: { "X-CSRFToken": csrftoken},
            method: "PUT",
            success: function(data) {
                $(`#${id}`).html(`Likes: ${data['likes']}`);
            }
        })
    });
    $('.add-book-rate').on('click', function(){
        var id=$(this).attr('id');
        console.log(this)
        $.ajax({
            url: "/shop/add_rate2book_ajax",
            data: {"book_slug": id.split('_')[3],
                   "rate": id.split('_')[4]},
            method: "GET",
            success: function(data) {
                let book_slug = id.split('_')[3]
                $(`#book_rate${book_slug}`).html(`Rate: ${data['rate']}`)
                console.log(data['rate'])
                for (let i = 1; i < 6; i++) {
                        if (i <= data['rate']){
                            $(`#book${book_slug}-${i}`).attr('class', 'rate fa fa-star checked')
                        }else{
                            $(`#book${book_slug}-${i}`).attr('class', 'rate fa fa-star')}
                }
            }
        })
    });
     $('.delete-comment').on('click', function(){
        var id=$(this).attr('id');
        let comment_id = id.split('-')[2];
        $.ajax({
            url: `/shop/delete_comment_ajax/${comment_id}`,
            headers: { "X-CSRFToken": csrftoken},
            method: "DELETE",
            success: function(data) {
                $(`#${id}`).remove();
            }
        })
     });
     $('.delete-book').on('click', function(){
        var id=$(this).attr('id');
        $.ajax({
            url: "/shop/delete_book_ajax",
            data: {"book_slug": id.split('_')[2]},
            method: "GET",
            success: function(data) {
                $(`#${id}`).remove();
            }
        })
     });

});

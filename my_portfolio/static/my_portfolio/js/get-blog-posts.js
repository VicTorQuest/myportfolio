$(document).ready(function() {
    $.ajax({
        type: 'GET',
        url: '/get-blog-posts/',
        success: function(response) {
            setTimeout(function(){
                $('#blogLoader').fadeOut()
                for (var post in response.all_posts) {
                    $('#posts').append(`<a href='${response.all_posts[post].url}' target='_blank' class='post-links'><div class='card--article-preview'><div class='article-preview__body'><h3 style='line-height: 0;'>📝</h3><div class='post'><strong>${response.all_posts[post].title}</strong><br><small>${new Date(response.all_posts[post].created_at).toLocaleDateString('en-US')}</small></div></div><i class='bi bi-arrow-right'></i></div></a>`)
                }
            }, 5000)
            
            
            
        },
        error: function(response) {
            setTimeout(() => {
                $('#blogLoader').fadeOut()
                $('#posts').append(`<p>Failed to load blog posts</p>`)
            }, 5000);
           
        }
    })
})
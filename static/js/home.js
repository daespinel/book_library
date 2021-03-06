// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    // Return the API
    return {
        'read': function () {
            let ajax_options = {
                type: 'GET',
                url: '/api/books',
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        'delete': function (book_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `/api/book/${book_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            return $.ajax(ajax_options)
        },
        'readOne': function(book_id){
            let ajax_options = {

            };
            return
        }
    };
}());


// Create the view instance
ns.view = (function () {
    'use strict';

    var $table = $(".blog table");

    // Return the API
    return {
        build_table: function (data) {
            let source = $('#blog-table-template').html(),
                template = Handlebars.compile(source),
                html;

            // Create the HTML from the template and notes
            html = template({ books: data });

            // Append the rows to the table tbody
            $table.append(html);
        },
        error: function (msg) {
            $.notify({message: msg},{type: 'danger'}, {delay:8000},{onClosed: this.redirecting()});
        },
        notifaction: function (msg) {
            $.notify({message: msg},{type: 'success'},{delay:8000},{onClosed: this.redirecting()});
        },
        redirecting: function () {
            setTimeout(() => {
                window.location = '/';
            }, 9000);
        }

    };
}());

// Create the controller instance
ns.controller = (function (m, v) {
    'use strict';
    let model = m,
        view = v;

    // Get the note data from the model after the controller is done initializing
    setTimeout(function () {

        // Attach event handlers to the promise returned by model.read()
        model.read()
            .done(function (data) {
                view.build_table(data);
            })
            .fail(function (xhr, textStatus, errorThrown) {
                error_handler(xhr, textStatus, errorThrown);
            });
    }, 100);

    $(document).on('click', '#tablebooks tbody tr td button.book_delete',function (e) {
        let $target = $(e.target).parent().parent(),
            book_id = $target.data('book_id');
        console.log(book_id)
        

        if(confirm("Are you sure to delete the book?")){
            model.delete(book_id)
        .done(function(data){
            notification_handler(data);
        })
        .fail(function (xhr, textStatus, errorThrown) {
            error_handler(xhr, textStatus, errorThrown);
        });    
        };    
    });

    $(document).on('click', '#tablerebooks tbody tr td button.book_update',function (e) {
        let $target = $(e.target).parent().parent(),
            book_id = $target.data('book_id');
        read_name()
        .done(function (data) {
            console.log(data)
            window.location = `/book/${book_id}`;
        })
        
            
    });

    // generic error handler
    function error_handler(xhr, textStatus, errorThrown) {
        let error_msg = `${textStatus}: ${errorThrown} - ${xhr.responseJSON.detail}`;
        view.error(error_msg);
        console.log(error_msg);
    }

    function notification_handler(notificationThrown) {
        let msg = `${notificationThrown}`;
        view.notifaction(msg);
    }

}(ns.model, ns.view));
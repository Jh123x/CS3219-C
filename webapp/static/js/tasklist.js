function req(method, id, csrf_token) {
    $.ajax(
        {
            type: method,
            url: "/todo",
            data: "id=" + id + "&csrf_token=" + csrf_token,
            success: function (msg) {
                location.reload();
            },
        }
    );
}
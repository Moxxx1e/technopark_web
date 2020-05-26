function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/*
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

const csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("click_like").click(function (event) {
    console.log(event)
    console.log(event.target.getAttribute("qid"))
     $.ajax({
        url: 'vote',
         data: {
            flag: 1,
            qid: event.target.getAttribute("qid"),
            user: event.target.getAttribute("user"),
        },
        type: 'POST',
         success: function (data) {
            alert(data.qid)
         },
         failure: function (data) {
            alert('Got an error dude')
         }
    });
});
*/
jQuery.fn.extend({
    disable: function (state) {
        return this.each(function () {
            var $this = $(this);
            $this.toggleClass('disabled', state);
        });
    }
});

let rate = (qid, flag) => {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'post',
        url: 'http://127.0.0.1:8000/vote/',
        data: {
            flag: flag,
            qid: qid,
            csrfmiddlewaretoken: csrftoken,
        },
    }).done((response) => {
        let element = document.querySelector(`#question-rating-${qid}`);
        console.log(response.rating);
        console.log(response.vote);
        like_button_name = '#like_' + qid;
        dislike_button_name = '#dislike_' + qid;
        if (response.vote === 1) {
            $(like_button_name).attr("disabled", true);
            $(dislike_button_name).attr("disabled", false);
        }
        else {
            $(dislike_button_name).attr("disabled", true);
            $(like_button_name).attr("disabled", false);
        }
        element.textContent = `${response.rating}`;
    }).fail((err) => {
        console.log(err);
    });
};


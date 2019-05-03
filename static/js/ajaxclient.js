function sendAction(pos) {
    var data = {
        "user_name": "webapp",
        "token": "test",
        "team_domain": "test",
        "channel_name": "test",
        "timestamp": "test",
        "trigger_word": "test",
        "text": pos
    };
    //var strdata = "user_name=webapp&token=test&team_domain=test&channel_name=test&timestamp=test&trigger_word=test&text=" + pos
    $.ajax({
        url: "http://localhost:8000/w2vhook",
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: "json",
        processData: false,
        success: function(data) {
            let result = data['text'];
            if (typeof(result) == 'string') {
                $("#result").html("<p style='color:orange;text-align:left;'>" + result + "</p>");
                return;
            }
            let table = makeTable(result);

            $("#result").html(table);
            let chk = $('#chkbox:checked').val();
            if (chk) {
                $("#pre_history").append("<h3>Log</<h3><hr>");
                $("#history").append(table + "<BR>");
            };
        },
        error: function(data) { $("#result").html(data); }
    });
};

function makeTable(data) {
    let pos = $('#positive').val();
    let word = "<tr>";
    let prob = "<tr>";
    let table = "<table class=\"table table-bordered table-hover table-responsive table-striped\"><tbody>";
    for (let i = 0; i < data.length; i++) {
        word += "<td>" + data[i][0] + "</td>";
        prob += "<td>" + Math.round(data[i][1] * 10000) / 100 + "</td>";
    };
    table = "<p style='text-align: center; font-weight: 600;'><BR>" + pos + "</p>" + table + word + "</tr>" + prob + "</tr>" + "</tr>" + "</tbody></table>"
    return table
};

$('#subbtn').on('click', function(event) {
    let pos = $('#positive').val();
    sendAction(pos);
    $("#result").html("<p style='text-align: center;'>Searching...</p>");
    $('#subbtn').addClass("animated rubberBand");
    setTimeout(function() {
        $('#subbtn').removeClass("animated rubberBand");
    }, 1000)
});

function arrangeDataTable(data) {
    var table = document.getElementById("myTable");
    for (let i = 0; i < data.length; i++) {
        var numVotes = 0
        for (let x in data[i]["OptionVote"]) {
            var vote = data[i]["OptionVote"][x];
            numVotes += vote;
        }
        var row = table.insertRow(i + 1);
        row.className += "data";
        var slNum = row.insertCell(0);
        var qstText = row.insertCell(1);
        var totalVotes = row.insertCell(2);
        var tags = row.insertCell(3);
        var qId = data[i]["Question_Id"];
        var hyperLink = `<a href="pollDetail/${qId}/" name="${qId}">`;
        slNum.innerHTML = i + 1;
        qstText.innerHTML = hyperLink + data[i]["Question"] + "</a>";
        totalVotes.innerHTML = numVotes;
        tags.innerHTML = data[i]["Tags"];
    }
}

function TableData() {
    $.get('getPoll/',  // url
        function (data, textStatus, jqXHR) {
            arrangeDataTable(data);
        });
}

function checkboxData() {
    $.get('tags/',  // url
        function (data, textStatus, jqXHR) {
            // console.log(data["Tags"][0]);
            for (let i = 0; i < data["Tags"].length; i++) {
                var checkbox = document.createElement("INPUT");
                var inLine = document.createElement("p");
                inLine.setAttribute("class", "inLinePara");
                checkbox.setAttribute("type", "checkbox");
                checkbox.setAttribute("value", data["Tags"][i]);
                checkbox.setAttribute("class", "filterCheckboxes");
                checkbox.setAttribute("name", "filterCheckboxes");
                // Id can be given as question id
                checkbox.setAttribute("id", data["Tags"][i]);
                var lbl = document.createElement('label');
                lbl.setAttribute('for', data["Tags"][i]);
                lbl.appendChild(document.createTextNode(" " + data["Tags"][i]));
                inLine.appendChild(checkbox)
                inLine.appendChild(lbl)
                checkboxContainer.appendChild(inLine);
            }

        });
}

function filterData() {
    // Getting the selected tags

    var favorite = [];
    $.each($("input[name='filterCheckboxes']:checked"), function () {
        favorite.push($(this).val());
    });
    var selectedTags = favorite.join(",");
    var sendUrl = "/filterPoll" + "?tags=" + selectedTags;

    $.get(sendUrl, function (data, status) {
        // console.log(data[1]["Question"]);
        var table = document.getElementById("myTable");
        if (favorite.length > 0) {
            $("#myTable").find("tr:gt(0)").remove();
            arrangeDataTable(data);
        }
        else {
            window.location.reload();
        }


    });





}
 
function createPoll(){
    location.href='createPoll/'

}


window.onload = TableData();
window.onload = checkboxData();
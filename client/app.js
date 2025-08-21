function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for (let i = 0; i < uiBathrooms.length; i++) {
        if (uiBathrooms[i].checked) return parseInt(uiBathrooms[i].value);
    }
    return -1;
}

function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for (let i = 0; i < uiBHK.length; i++) {
        if (uiBHK[i].checked) return parseInt(uiBHK[i].value);
    }
    return -1;
}

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");

    var sqft = parseFloat(document.getElementById("uiSqft").value);
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations").value;
    var estPrice = document.getElementById("uiEstimatedPrice");

    $.ajax({
        url: "http://127.0.0.1:5000/predict_home_price",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            total_sqft: sqft,
            bhk: bhk,
            bath: bathrooms,
            location: location
        }),
        success: function(data) {
            console.log("Prediction response:", data);
            estPrice.innerHTML = "<h2>" + data.estimated_price + " Lakh</h2>";
        },
        error: function(xhr, status, error) {
            console.error("Request failed:", status, error);
            estPrice.innerHTML = "<h2>Request Failed</h2>";
        }
    });
}

function onPageLoad() {
    console.log("document loaded");

    $.get("http://127.0.0.1:5000/get_location_names", function(data) {
        console.log("Got location names:", data);
        if (data) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for (let i = 0; i < locations.length; i++) {
                var opt = new Option(locations[i], locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });
}

window.onload = onPageLoad;

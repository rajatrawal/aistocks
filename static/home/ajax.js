
function calculatePercentage(newPrice, oldPrice) {
    let num = ((newPrice - oldPrice) / oldPrice) * 100;
    num = num.toFixed(2);
    return num;
}
function calculateColor(value) {
    if (value > 0) {
        return 'green';
    }
    else {
        return 'red';
    }
}
function showTomorrowPredicton(data) {
    let predictTomorrow = document.getElementsByClassName('predict_tomorrow')[0];
    if (data != 'false') {
        data = JSON.parse(data);
        let newPrice = data[0];
        let change = calculatePercentage(newPrice, stockPrice);
        let predColor = calculateColor(change);
        predictTomorrow.innerHTML = `
                        Price Of <span class='primary'> ${stockName} </span> For ${data[2]} Will Be <span class='${predColor}'>${stockSymbol} ${newPrice} ${change}% </span>.
                    `;
    }
    else {
        predictTomorrow.innerHTML = "Sorry Forecating Can't Be Done For This Symbol.";
    }
    predictTomorrow.classList.remove('placeholder-glow');
}

function ajaxRequest(url, input, func) {
    $.ajax(
        {
            type: "GET",
            url: url,
            data: {
                stockName: input
            },
            success: function (data) {
                func(data);
            }
        })
}
function normalAjaxRequest(url,  func) {
    $.ajax(
        {
            type: "GET",
            url: url,

            success: function (data) {
                func(data);
            }
        })
}


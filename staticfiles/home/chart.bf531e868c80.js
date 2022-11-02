// revenueAnualChart

function loadAllChart(data) {
    let parse_data = JSON.parse(data);
    data = parse_data[0];
    financialData = parse_data[1];
    const anuallyNetProfit = data['anuallyNetProfit'];
    const quarterlyNetProfit = data['quarterlyNetProfit'];
    const anuallyNetAssets = data['anuallyNetAssets'];
    const anuallyNetLiab = data['anuallyNetLiab'];
    const quarterlyRevenue = data['quarterlyRevenue'];
    const quarterlyColumns = data['quarterlyColumns'];
    const anuallyColumns = data['anuallyColumns'];
    const anuallyRevenue = data['anuallyRevenue'];
    const anuallyCash = data['anuallyCash'];
    const anuallyGoodwill = data['anuallyGoodwill'];
    const anuallyIncomeStatement = financialData['anuallyIncomeStatement'];
    const anuallyBalanceSheet = financialData['anuallyBalanceSheet'];
    const anuallyCashFlow = financialData['anuallyCashFlow'];
    const quarterlyIncomeStatement = financialData['quarterlyIncomeStatement'];
    createTable(anuallyIncomeStatement, 'anuallyIncomeStatement');
    createTable(anuallyBalanceSheet, 'anuallyBalanceSheet');
    createTable(anuallyCashFlow, 'anuallyCashFlow');
    createTable(quarterlyIncomeStatement, 'quarterlyIncomeStatement');


    createChart('revenueAnualChart', anuallyRevenue, anuallyColumns, 'Total Revenue');
    createChart('quarterlyAnualChart', quarterlyRevenue, quarterlyColumns, 'Total Revenue');
    createChart('profitAnualChart', anuallyNetProfit, anuallyColumns, 'Net Profit');
    createChart('profitQuarterlyChart', quarterlyNetProfit, quarterlyColumns, 'Net Profit');
    createChart('anualAssetChart', anuallyNetAssets, anuallyColumns, 'Assets');
    createChart('anualLiabChart', anuallyNetLiab, anuallyColumns, 'Liab.');
    createChart('anualCashChart', anuallyCash, anuallyColumns, 'Cash');
    createChart('anualGoodwillChart', anuallyGoodwill, anuallyColumns, 'Goodwill');

}



function createTable(data, tableDivId) {
    var tableDiv = document.getElementById(tableDivId);
    var keys = Object.keys(data);
    var tableSize = Object.keys(data['Breakdown']).length;
    var table = document.createElement('table');
    table.className = 'table table-striped';
    var tbodyEle = document.createElement('tbody');
    var tHeadEle = document.createElement('thead');
    var tHeadEleStr = '';
    if (tableDivId != 'quarterlyIncomeStatement') {
        for (let i = keys.length - 1; i >= 0; i--) {
            tHeadEleStr += ` <th scope="col">${keys[i]}</th>`;
        }
        for (let j = 0; j < tableSize; j++) {
            trEle = document.createElement('tr');
            var trEleStr = ``;
            for (let i = keys.length - 1; i >= 0; i--) {
                innerKeys = Object.keys(data[keys[i]]);
                valueOfKey = data[keys[i]][innerKeys[j]];
                if (keys[i] == 'Breakdown') {
                    trEleStr += `<th scope='row'>${titleWords(valueOfKey)}</th>`;

                }
                else {
                    trEleStr += `<td>${valueOfKey / 10000000}</td>`;
                }
                trEle.innerHTML = trEleStr;
                tbodyEle.appendChild(trEle);
            }
        }
    }
    else {
        for (let i = 0; i < keys.length; i++) {
            tHeadEleStr += ` <th scope="col">${keys[i]}</th>`;
        }
        for (let j = 0; j < tableSize; j++) {
            trEle = document.createElement('tr');
            var trEleStr = ``;
            for (let i = 0; i < keys.length; i++) {
                innerKeys = Object.keys(data[keys[i]]);
                valueOfKey = data[keys[i]][innerKeys[j]];
                if (keys[i] == 'Breakdown') {
                    trEleStr += `<th scope='row'>${titleWords(valueOfKey)}</th>`;

                }
                else {
                    trEleStr += `<td>${valueOfKey / 10000000}</td>`;
                }
                trEle.innerHTML = trEleStr;
                tbodyEle.appendChild(trEle);
            }
        }
    }
    tHeadEle.innerHTML = tHeadEleStr;
    table.appendChild(tHeadEle);
    table.appendChild(tbodyEle);
    tableDiv.appendChild(table);
}

function titleWords(words) {
    str = ''
    for (i of words) {
        if (i === i.toUpperCase()) {
            str += ' ' + i;
        }
        else {
            str += i;
        }
    }
    str = str[0].toUpperCase() + str.substring(1);
    return str;
}
function createChart(chartId, data, labels, label_name) {
    ctx = document.getElementById(chartId).getContext('2d');
    dataset = {
        labels: labels,
        datasets: [{
            label: label_name,
            data: data,
            backgroundColor: [
                '#8a2be2',
            ],
        }]
    }
    let delayed;
    config = {
        type: 'bar',
        data: dataset,
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },

            plugins: {
                subtitle: {
                    display: true,
                    text: 'Values in cr.'
                }
            },
            animation: {
                onComplete: () => {
                    delayed = true;
                },
                delay: (context) => {
                    let delay = 0;
                    if (context.type === 'data' && context.mode === 'default' && !delayed) {
                        delay = context.dataIndex * 300 + context.datasetIndex * 100;
                    }
                    return delay;
                },
            },
        }
    };
    myChart = new Chart(ctx, config);
}

ajaxRequest("/getFinancialData", symbolNameNs, loadAllChart);

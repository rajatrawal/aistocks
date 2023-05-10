function loadMarqueeTagAjaxData(data) {
    let marqueeTagAjaxData = JSON.parse(data);
    let marqueeTagStrData = ``;
    let marqueeTag = document.getElementById('marquee_tag')
    for (let stock of marqueeTagAjaxData) {
        marqueeTagStrData += `

        <span class='me-4 '>
    <span class='fw-bold me-1 marquee_tag_symbol'><a href='/getTicker/${stock['Symbol']}'
            class='symbol_name_a'>${stock['Symbol']}</a> </span>
    <span class='fw-bold  me-1'>${stock['Price (Intraday)']}</span>
    <span class='${stock['color']}'>${stock['% Change']}%</span>
    <span class=' symbol_sign'>
        `;
        if (stock['color'] === 'green') {
            marqueeTagStrData += `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green"
            class="bi bi-caret-up-square-fill" viewBox="0 0 16 16">
            <path
                d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm4 9h8a.5.5 0 0 0 .374-.832l-4-4.5a.5.5 0 0 0-.748 0l-4 4.5A.5.5 0 0 0 4 11z" />
        </svg>
        </span>
        </span>
            `;
        }
        else {
            marqueeTagStrData += `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red"
    class="bi bi-caret-down-square-fill" viewBox="0 0 16 16">
    <path
        d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm4 4a.5.5 0 0 0-.374.832l4 4.5a.5.5 0 0 0 .748 0l4-4.5A.5.5 0 0 0 12 6H4z" />
        </svg>
    </span>
    </span>

            `;
        }
    }
    marqueeTag.innerHTML = marqueeTagStrData;

}
function loadIndexAjaxData(data) {
    highlightData = JSON.parse(data);
    let counter = 1;
    let highlightDivTagStrData = ``;
    let highlightDataDiv = document.querySelector('.highlight_data_div')
    for (let key in highlightData) {

        highlightDivTagStrData += `
        <div class="col-md-4">
        <div class=" index_div p-1">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title cardTitlePrice fw-bold"><a href="/getTicker/${highlightData[key]['symbol']}"
                            class="symbol_name_a">${highlightData[key]['shortName']}</a></h5>
                    <div class="h3  ${highlightData[key]['color']} fw-bold mt-2 mb-2">
                        ${highlightData[key]['regularMarketPrice']} <span
                            class="cardPriceChangeSpan h6 ms-1 fw-bold ${highlightData[key]['color']}">
                            ${highlightData[key]['regularMarketChange']} </span>
                        <span
                            class="cardPricePercentSpan fw-bold h6 ms-1 ${highlightData[key]['color']}">${highlightData[key]['regularMarketChangePercent']}%</span>
                    </div>
                    <div>
                        <div class="fw-bold"><span class="text-muted ">Todays High:
                            </span><span>${highlightData[key]['regularMarketDayHigh']}</span></div>
                        <div class="fw-bold"><span class="text-muted ">Todays Low:
                            </span><span>${highlightData[key]['regularMarketDayLow']}</span></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
        `;
        if (counter === 3) {
            highlightDivTagStrData += `
            </div>
    <div class="row mt-1  ms-2 me-2">
            `;
        }
    }
    highlightDataDiv.innerHTML = highlightDivTagStrData;
}
function getSecondaryIndexAjaxData(data) {
    let tableData = JSON.parse(data);
    let tableParentDiv = document.querySelector(".table_parent_div");
    let tableParentDivStr = ``;
    let tableBodyDiv;
    for (let table in tableData) {
        tableParentDivStr = tableParentDiv.innerHTML;
        tableParentDivStr += `
<div class="mt-4 mb-4  ms-3 d-flex justify-content-between">
    <div class='h3 fw-bold text-capitalize'>
        ${table}
    </div>
    <div>
        <a href="table/${table}" class='me-2'>See All</a>
    </div>
</div>
<table class="table table-striped">
    <thead>
        <tr>
            <th scope="col">Symbol</th>
            <th scope="col">Price</th>
            <th scope="col">Change</th>
            <th scope="col">Change %</th>
        </tr>
    </thead>
    <tbody id = 'tableData_${table}'>
    </tbody>
</table>
        `;
    tableParentDiv.innerHTML = tableParentDivStr;
    tableParentDivStr = ``;
    tableBodyDiv = document.getElementById(`tableData_${table}`);
    tableBodyDivStr = ``;
    counter = 0;
    for(stock in tableData[table]){
        
        if(counter < 11){
            let value = tableData[table][stock];
            tableParentDivStr += `
            <tr>
            <td><a href='/getTicker/${value['Symbol']}' class='primary_link'>${value['Symbol']}</a> </td>
                <td>${value['Price (Intraday)']}</td>
                <td class="${value['color']}">${value['Change']}</td>
                <td class="${value['color']}">${value['% Change']} %</td>
                </tr>
            `;
            counter++;
        }
        else{
            break;
        }
    }
    tableBodyDiv.innerHTML = tableParentDivStr;
    counter = 0;
    tableBodyDivStr = ``;
  
    }
}
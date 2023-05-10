var typed4 = new Typed('#searchInput', {
    strings: ['Search As "RELIANCE" ', ' Search As "AAPL" ', ' Search As "AMD" ', ' Search As "NVDA" ', ' Search As "HDFC" ', ' Search As "SNAP" ', ' Search As "META" ', ' Search As "GOOG" ', ' Search As "ASIANPAINT" ', ' Search As "AMZN" ', 'Search For Your Favarite Stock'],
    typeSpeed: 100,
    backSpeed: 50,
    attr: 'placeholder',
    bindInputFocusEvents: true,
    loop: true
});
function addClickEvent(eventClassName, targetClassName, utilityClassName) {
    $(`.${eventClassName}`).click(() => {
        account_box = document.querySelector(`.${targetClassName}`);
        if (account_box.classList.contains(utilityClassName)) {
            account_box.classList.remove(utilityClassName);
        }
        else {
            account_box.classList.add(utilityClassName);

        }
    })
}
// addClickEvent('thumb_name','account_box','click_account');
addClickEvent('menu_span', 'navbar-collapse', 'navbar-collapse_transition');



window.onload = () => {
    fetch("/static/home/stocks.json")
        .then(response => {
            return response.json();
        })
        .then(jsondata => {
            symbolData = jsondata;
        })


    let searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keypress', (e) => {
        if (e.keyCode === 13 || e.which === 13) {
            e.preventDefault();
            return false;
        }
    })
    searchInput.addEventListener('input', (e) => {
        let searchResultDiv = document.getElementsByClassName('search_result_div')[0];
        let eValue = e.target.value;
        if (eValue.length != 0) {
            reg = new RegExp(eValue, 'i');
            let resultArray = [];
            for (let i of symbolData) {
                let symbol = i['symbol'];
                let name = i['name'];
                let re1 = reg.test(symbol);
                let re2 = reg.test(name);
                if (re1 == true || re2 == true) {
                    resultArray.push({ "symbol": symbol, "name": name, "exchange": i['exchange'].toUpperCase() });
                }
            }
            let count = 0;
            let ul = document.getElementsByClassName('search_result_div_ul')[0];
            let resultStr = '';
            for (i of resultArray) {
                if (count < 14) {
                    resultStr += `
            <a href="/getStock/${i['symbol']}" class=>
        <li class='search_result_list row'>
        <span class="symbol_name col-4">${i['symbol']}</span> <span class='col-6'> ${i['name']}</span><span class='col-2 nse_span'>${i['exchange']}</span>
        </li>
        </a>
            `
                    count++;
                }
                else {
                    break;
                }
            };
            if (resultStr.length == 0) {
                resultStr = `<h5 class='m-2'> No Results Found </h5>`;
            }
            searchResultDiv.style.display = 'block';
            ul.innerHTML = resultStr;
        }
        else {
            searchResultDiv.style.display = 'none';

        }


    })
}





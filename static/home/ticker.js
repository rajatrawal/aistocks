function showCompanyCategory(data) {
    data = JSON.parse(data);

    if (data != 'false') {
        let topInfoRight = document.getElementsByClassName('top_info_right')[0];
        if (data['sector'] != undefined) {

            topInfoRight.innerText = data['sector'];
        }
        str1 = '';

        for (j in data) {
            key = titleWords(titleWords(j));
            str1 += `<tr><th scope="row">${key}</th><td>${data[j]}</td></tr>`;
        }
        companyInfoTableBody.innerHTML = str1;
    };
};
function showDividendTable(data) {
    data = JSON.parse(data);
    str1 = '';
    if (data != 'false') {
        for (j in data) {
            key = titleWords(titleWords(j));
            str1 += `<tr><th scope="row">${key}</th><td>${data[j]}</td></tr>`;
        };
        dividendTableBody.innerHTML = str1;
    }
};

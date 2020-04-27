const matchesList = document.getElementById('matchesList');
const searchBar = document.getElementById('searchBar');

let bestMatches = [];

searchBar.addEventListener('keyup', (e) => {
    const searchStr = e.target.value.toLowerCase();
    if(searchStr.length > 0) {
        loadStats(searchStr);
    }
    else {
        loadStats();
    }
    // console.log(searchStr);
});

const loadStats = async (kw = 'a') => {
    try {
        const api_link = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' + kw + '&apikey=0W6T3C4CI21913T8';
        const res = await fetch(api_link);
        const Stats = await res.json();
        const bestMatches = Stats['bestMatches'];
        if(bestMatches.length > 0) {
        	matchesList.innerHTML = "";
            displayStats(bestMatches);
        }
        else {
            matchesList.innerHTML = `<p>No Results</p>`;
        }
    } catch (err) {
        console.error(err);
    }
};

const displayStats = (matches) => {
    var table = document.createElement('TABLE');
    var row = table.insertRow(0);
    headers = ['Symbol','Name','Region',''];
    for (var i = 0; i < headers.length; i++) {
        var headerCell = document.createElement("TH");
        headerCell.innerHTML = headers[i];
        row.appendChild(headerCell);
    }
    for(let i = 0;i < matches.length; ++i) {
        var row = table.insertRow(i+1);
        var symbol = row.insertCell(0);
        var name = row.insertCell(1);
        var region = row.insertCell(2);
        var link = row.insertCell(3);
        tag = `<a href = "/analysis/${matches[i]['1. symbol']}/${matches[i]['2. name']}">Go To Analysis</a>`;
        symbol.innerHTML = matches[i]['1. symbol'];
        name.innerHTML = matches[i]['2. name'];
        region.innerHTML = matches[i]['4. region']
        link.innerHTML = tag;
    }
    table.className = 'table text-center table-striped table-bordered';
    matchesList.appendChild(table);
}

loadStats('a');
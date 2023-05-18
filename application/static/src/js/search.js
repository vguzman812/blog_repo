document.getElementById('search-input').addEventListener('input', function (e) {
    const searchQuery = e.target.value;
    if (searchQuery.length > 2) {
        fetch(`/search/${searchQuery}`)
            .then(response => response.json())
            .then(results => {
                const searchResultsContainer = document.querySelector('.search-results');
                searchResultsContainer.innerHTML = '';
                if (results.length > 0) {
                    searchResultsContainer.classList.remove('d-none');
                    searchResultsContainer.classList.add('d-block', 'overflow-auto');
                    results.forEach(result => {
                        const resultItem = document.createElement('a');
                        resultItem.href = result.url;
                        resultItem.classList.add('dropdown-item', 'text-wrap');
                        resultItem.textContent = result.title
                        searchResultsContainer.appendChild(resultItem);
                        const rule = document.createElement('hr')
                        rule.classList.add('dropdown-divider')
                        searchResultsContainer.appendChild(rule)
                    });
                } else {
                    searchResultsContainer.classList.remove('d-block');
                    searchResultsContainer.classList.add('d-none');
                }
            });
    } else {
        const searchResultsContainer = document.querySelector('.search-results');
        searchResultsContainer.classList.remove('d-block');
        searchResultsContainer.classList.add('d-none');
    }
});

document.getElementById('search-form').addEventListener('submit', function (e) {
    e.preventDefault();
});
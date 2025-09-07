let chart; // To hold the chart instance

async function fetchFinancialData(symbol) {
    try {
        const response = await fetch(`/api/financial-info/${symbol}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching financial data for ${symbol}:`, error);
        return [];
    }
}

function getRandomColor() {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return {
        background: `rgba(${r}, ${g}, ${b}, 0.2)`,
        border: `rgba(${r}, ${g}, ${b}, 1)`
    };
}

async function updateChart() {
    const symbolsInput = document.getElementById('symbolsInput');
    const symbols = symbolsInput.value.split(',').map(s => s.trim()).filter(s => s);

    if (symbols.length === 0) {
        alert('Please enter at least one symbol.');
        return;
    }

    const financialDataPromises = symbols.map(symbol => fetchFinancialData(symbol));
    const allFinancialData = await Promise.all(financialDataPromises);

    const allDates = new Set();
    allFinancialData.forEach(data => {
        if (data) {
            data.forEach(item => allDates.add(item.Date));
        }
    });
    const labels = Array.from(allDates).sort();

    const datasets = allFinancialData.map((data, index) => {
        const symbol = symbols[index];
        const epsData = labels.map(date => {
            const dataPoint = data ? data.find(item => item.Date === date) : null;
            return dataPoint ? dataPoint.EPS : null;
        });
        const colors = getRandomColor();
        return {
            label: `${symbol} EPS`,
            data: epsData,
            backgroundColor: colors.background,
            borderColor: colors.border,
            borderWidth: 1
        };
    }).filter(dataset => dataset.data.some(d => d !== null));

    if (datasets.length === 0) {
        console.log("No data to display for the selected symbols.");
        if (chart) {
            chart.destroy();
        }
        return;
    }

    const ctx = document.getElementById('financialChart');
    if (chart) {
        chart.destroy();
    }
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'EPS (Earnings Per Share)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'EPS Comparison'
                }
            }
        }
    });
}

// Event listener for the Compare button
document.getElementById('compareButton').addEventListener('click', updateChart);

// Initial chart creation on page load
window.onload = updateChart;
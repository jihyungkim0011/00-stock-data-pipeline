let stockChart;

async function fetchStockData(symbol, startDate, endDate) {
    let url = `/stocks/${symbol}`;
    const params = new URLSearchParams();
    if (startDate) {
        params.append('start_date', startDate);
    }
    if (endDate) {
        params.append('end_date', endDate);
    }
    if (params.toString()) {
        url += `?${params.toString()}`;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching stock data for ${symbol}:`, error);
        return [];
    }
}

async function updateChart() {
    const symbol = document.getElementById('symbolInput').value.trim();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    if (!symbol) {
        alert('Please enter a stock symbol.');
        return;
    }

    const stockData = await fetchStockData(symbol, startDate, endDate);

    if (stockData.length === 0) {
        console.log("No data to display for the selected symbol.");
        if (stockChart) {
            stockChart.destroy();
        }
        return;
    }

    const labels = stockData.map(item => item.Date);
    const closingPrices = stockData.map(item => item.Close);
    const volumes = stockData.map(item => item.Volume);

    const ctx = document.getElementById('stockChart');
    if (stockChart) {
        stockChart.destroy();
    }

    stockChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    type: 'line',
                    label: 'Close Price',
                    data: closingPrices,
                    borderColor: 'rgb(75, 192, 192)',
                    yAxisID: 'y-axis-price',
                },
                {
                    type: 'bar',
                    label: 'Volume',
                    data: volumes,
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    yAxisID: 'y-axis-volume',
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                'y-axis-price': {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Price'
                    }
                },
                'y-axis-volume': {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Volume'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: `Stock Price and Volume for ${symbol.toUpperCase()}`
                }
            }
        }
    });
}

document.getElementById('viewButton').addEventListener('click', updateChart);

window.onload = updateChart;

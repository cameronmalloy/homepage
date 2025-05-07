// Global variables
let chart;
let currentPage = 1;
let totalPages = 1;
let currentGraphId = null;

// DOM elements
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const exampleButton = document.getElementById('example-button');
const welcomeContent = document.getElementById('welcome-content');
const graphContent = document.getElementById('graph-content');
const prevButton = document.getElementById('prev-btn');
const nextButton = document.getElementById('next-btn');

// Event listeners
searchButton.addEventListener('click', handleSearch);
exampleButton.addEventListener('click', loadExampleGraph);
prevButton.addEventListener('click', navigatePrevious);
nextButton.addEventListener('click', navigateNext);

// Handle search action
function handleSearch() {
    const query = searchInput.value.trim();
    
    if (query) {
        // Assuming the query is a graph ID
        loadGraph(query);
    } else {
        alert('Please enter a graph ID to search');
    }
}

// Load example graph
function loadExampleGraph() {
    fetch('/graph/example')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to create example graph');
            }
            return response.text();
        })
        .then(html => {
            // Extract graph ID from the response (this is a workaround since we're expecting JSON but the endpoint returns HTML)
            const match = html.match(/graph_id=['"]([^'"]+)['"]/);
            if (match && match[1]) {
                loadGraph(match[1]);
                // Update the search input with the graph ID
                searchInput.value = match[1];
            } else {
                throw new Error('Could not extract graph ID from response');
            }
        })
        .catch(error => {
            console.error('Error creating example graph:', error);
            alert('Failed to create example graph. Please try again.');
        });
}

// Load graph by ID
function loadGraph(graphId) {
    currentGraphId = graphId;
    currentPage = 1;
    
    // Show graph content, hide welcome
    welcomeContent.style.display = 'none';
    graphContent.style.display = 'block';
    
    // Load the first page of data
    loadPage(1);
}

// Load specific page of graph data
function loadPage(page) {
    if (!currentGraphId) return;
    
    fetch(`/graph/api/data/${currentGraphId}/${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load graph data');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Update page info
                currentPage = page;
                totalPages = data.total_pages;
                document.getElementById('page-indicator').textContent = `Page ${currentPage} of ${totalPages}`;
                
                // Update navigation buttons
                prevButton.disabled = (currentPage <= 1);
                nextButton.disabled = (currentPage >= totalPages);
                
                // Update title
                document.getElementById('graph-title').textContent = data.title;
                
                // Prepare data for Chart.js
                const chartData = {
                    labels: data.data.map(point => point.x),
                    datasets: [{
                        label: data.y_axis_label,
                        data: data.data.map(point => point.y),
                        borderColor: data.config.line_color,
                        backgroundColor: data.config.point_color,
                        borderWidth: data.config.line_width,
                        pointRadius: data.config.point_size,
                        tension: 0.3,
                        pointHoverRadius: data.config.point_size * 1.5
                    }]
                };
                
                // Create or update chart
                if (chart) {
                    chart.data = chartData;
                    chart.options.plugins.title.text = data.title;
                    chart.options.scales.y.title.text = data.y_axis_label;
                    chart.options.scales.x.title.text = data.x_axis_label;
                    chart.update();
                } else {
                    const ctx = document.getElementById('chart').getContext('2d');
                    
                    // Set canvas height
                    ctx.canvas.height = data.config.height;
                    
                    chart = new Chart(ctx, {
                        type: 'line',
                        data: chartData,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                title: {
                                    display: false,
                                    text: data.title,
                                    font: {
                                        size: 16
                                    }
                                },
                                tooltip: {
                                    callbacks: {
                                        label: function(context) {
                                            const point = data.data[context.dataIndex];
                                            return point.label;
                                        }
                                    }
                                }
                            },
                            scales: {
                                y: {
                                    title: {
                                        display: true,
                                        text: data.y_axis_label
                                    }
                                },
                                x: {
                                    title: {
                                        display: true,
                                        text: data.x_axis_label
                                    }
                                }
                            }
                        }
                    });
                }
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error loading graph data:', error);
            alert('Failed to load graph data. Please try again.');
        });
}

// Navigate to previous page
function navigatePrevious() {
    if (currentPage > 1) {
        loadPage(currentPage - 1);
    }
}

// Navigate to next page
function navigateNext() {
    if (currentPage < totalPages) {
        loadPage(currentPage + 1);
    }
}

// Add keyboard event listener for search
searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        handleSearch();
    }
});
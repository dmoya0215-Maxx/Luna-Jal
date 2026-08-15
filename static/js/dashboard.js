// Dashboard Initialization
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeCharts();
    setupResponsive();
});

// ============================================
// SIDEBAR FUNCTIONALITY
// ============================================

function initializeSidebar() {
    // Support both IDs used in templates: 'sidebarToggle' and 'toggleSidebar'
    const sidebarToggle = document.getElementById('sidebarToggle') || document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    // Mobile menu toggle
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('active');
            sidebarToggle.setAttribute('aria-expanded', sidebar.classList.contains('open'));
        });
    }

    // Close sidebar when clicking on nav links (mobile)
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 992 && sidebar) {
                sidebar.classList.remove('open');
                if (overlay) overlay.classList.remove('active');
            }

            // Update active state for visual feedback
            navLinks.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// ============================================
// CHARTS INITIALIZATION
// ============================================

function initializeCharts() {
    // Chart.js configuration
    Chart.defaults.color = '#b0b8ff';
    Chart.defaults.borderColor = 'rgba(100, 200, 255, 0.1)';
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";

    // Line Chart
    if (document.getElementById('lineChart')) {
        createLineChart();
    }

    // Doughnut Charts
    if (document.getElementById('doughnutChart1')) {
        createDoughnutChart('doughnutChart1', 'Expenses');
        createDoughnutChart('doughnutChart2', 'Revenue');
    }

    // Area Chart
    if (document.getElementById('areaChart')) {
        createAreaChart();
    }

    // Bar Chart
    if (document.getElementById('barChart')) {
        createBarChart();
    }
}

// Line Chart
function createLineChart() {
    const ctx = document.getElementById('lineChart').getContext('2d');
    
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(100, 200, 255, 0.3)');
    gradient.addColorStop(1, 'rgba(100, 200, 255, 0.01)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            datasets: [
                {
                    label: 'Activity',
                    data: [30, 45, 38, 52, 48, 60, 55, 70],
                    borderColor: '#64c8ff',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#64c8ff',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointHoverBackgroundColor: '#ff006e',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 30, 50, 0.9)',
                    titleColor: '#64c8ff',
                    bodyColor: '#fff',
                    borderColor: '#64c8ff',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return 'Value: ' + context.parsed.y;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        drawBorder: false,
                        color: 'rgba(100, 200, 255, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                }
            }
        }
    });
}

// Doughnut Chart
function createDoughnutChart(canvasId, label) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const colors = canvasId === 'doughnutChart1' 
        ? ['#64c8ff', '#ff006e', '#b640e0']
        : ['#00d4ff', '#ff1493', '#9d4edd'];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Category A', 'Category B', 'Category C'],
            datasets: [{
                data: [35, 40, 25],
                backgroundColor: colors,
                borderColor: 'rgba(20, 30, 50, 0.8)',
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: { size: 12 },
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 30, 50, 0.9)',
                    titleColor: colors[0],
                    bodyColor: '#fff',
                    borderColor: colors[0],
                    borderWidth: 1,
                    padding: 10,
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            }
        }
    });
}

// Area Chart
function createAreaChart() {
    const ctx = document.getElementById('areaChart').getContext('2d');
    
    const gradient1 = ctx.createLinearGradient(0, 0, 0, 300);
    gradient1.addColorStop(0, 'rgba(100, 200, 255, 0.3)');
    gradient1.addColorStop(1, 'rgba(100, 200, 255, 0.01)');

    const gradient2 = ctx.createLinearGradient(0, 0, 0, 300);
    gradient2.addColorStop(0, 'rgba(255, 0, 110, 0.2)');
    gradient2.addColorStop(1, 'rgba(255, 0, 110, 0.01)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
            datasets: [
                {
                    label: 'Trend A',
                    data: [25, 35, 30, 40, 45, 50],
                    borderColor: '#64c8ff',
                    backgroundColor: gradient1,
                    fill: true,
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#64c8ff'
                },
                {
                    label: 'Trend B',
                    data: [15, 20, 28, 25, 35, 40],
                    borderColor: '#ff006e',
                    backgroundColor: gradient2,
                    fill: true,
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#ff006e'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 30, 50, 0.9)',
                    bodyColor: '#fff',
                    borderColor: '#64c8ff',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(100, 200, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value + 'k';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                }
            }
        }
    });
}

// Bar Chart
function createBarChart() {
    const ctx = document.getElementById('barChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'Morning',
                    data: [20, 25, 30, 28, 35, 22, 25],
                    backgroundColor: '#64c8ff',
                    borderRadius: 8,
                    borderSkipped: false,
                    barPercentage: 0.8,
                    categoryPercentage: 0.7,
                },
                {
                    label: 'Evening',
                    data: [15, 20, 25, 30, 28, 18, 22],
                    backgroundColor: '#ff006e',
                    borderRadius: 8,
                    borderSkipped: false,
                    barPercentage: 0.8,
                    categoryPercentage: 0.7,
                },
                {
                    label: 'Night',
                    data: [10, 15, 12, 18, 20, 15, 12],
                    backgroundColor: '#b640e0',
                    borderRadius: 8,
                    borderSkipped: false,
                    barPercentage: 0.8,
                    categoryPercentage: 0.7,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'x',
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 30, 50, 0.9)',
                    bodyColor: '#fff',
                    borderColor: '#64c8ff',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + ' items';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 50,
                    grid: {
                        color: 'rgba(100, 200, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: function(value) {
                            return value;
                        }
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                }
            }
        }
    });
}

// ============================================
// RESPONSIVE DESIGN HANDLING
// ============================================

function setupResponsive() {
    let isDesktop = window.innerWidth > 992;

    window.addEventListener('resize', function() {
        const newIsDesktop = window.innerWidth > 992;
        
        if (isDesktop !== newIsDesktop) {
            isDesktop = newIsDesktop;
            const sidebar = document.querySelector('.sidebar');
            
            if (isDesktop) {
                sidebar.classList.remove('open');
            }
        }
    });

    // Smooth scroll for navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Prevent default link behavior
            if (!this.href || this.href === '#') {
                e.preventDefault();
            }
        });
    });
}

// ============================================
// INTERACTIVE FEATURES
// ============================================

// Add click animation to stat cards
document.addEventListener('DOMContentLoaded', function() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.animation = 'pulse 0.6s ease';
            
            setTimeout(() => {
                this.style.animation = '';
            }, 600);
        });
    });
});

// Add utility for mobile touch events
if (window.matchMedia('(hover: none)').matches) {
    // Mobile device - add touch feedback
    document.addEventListener('touchstart', function() {}, false);
}

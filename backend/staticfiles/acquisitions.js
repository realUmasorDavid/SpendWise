document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('acquisitions').getContext('2d');
    
    // Dummy data - replace with your actual categories/values
    const dummyData = {
        labels: ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping'],
        datasets: [{
            data: [1200, 500, 300, 400, 250],
            backgroundColor: [
                '#4F46E5', // indigo
                '#10B981', // emerald
                '#EF4444', // red
                '#F59E0B', // amber
                '#8B5CF6', // purple
            ],
            borderWidth: 0
        }]
    };

    new Chart(ctx, {
        type: 'doughnut', // Change to 'bar', 'pie', etc. as needed
        data: dummyData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `$${context.raw.toLocaleString()}`;
                        }
                    }
                }
            }
        }
    });
});
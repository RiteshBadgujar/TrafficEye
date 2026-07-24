/* ======================================
   TrafficEye Dashboard Charts
====================================== */

document.addEventListener("DOMContentLoaded", function () {

    // ======================================
    // Monthly Violations Bar Chart
    // ======================================

    const monthlyCanvas = document.getElementById("monthlyChart");

    if (monthlyCanvas && typeof monthlyStats !== "undefined") {

        new Chart(monthlyCanvas, {

            type: "bar",

            data: {

                labels: monthlyStats.map(item => item.month),

                datasets: [{

                    label: "Traffic Violations",

                    data: monthlyStats.map(item => item.count),

                    backgroundColor: "#0d6efd",

                    borderRadius: 6

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {

                            precision: 0

                        }

                    }

                }

            }

        });

    }

    // ======================================
    // Paid vs Pending Pie Chart
    // ======================================

    const statusCanvas = document.getElementById("statusChart");

    if (statusCanvas && typeof paymentStats !== "undefined") {

        new Chart(statusCanvas, {

            type: "pie",

            data: {

                labels: ["Paid", "Pending"],

                datasets: [{

                    data: [

                        paymentStats.Paid,

                        paymentStats.Pending

                    ],

                    backgroundColor: [

                        "#198754",

                        "#ffc107"

                    ]

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false

            }

        });

    }

    // ======================================
    // Violation Types Doughnut Chart
    // ======================================

    const typeCanvas = document.getElementById("violationChart");

    if (typeCanvas && typeof violationTypes !== "undefined") {

        new Chart(typeCanvas, {

            type: "doughnut",

            data: {

                labels: violationTypes.map(item => item.type),

                datasets: [{

                    data: violationTypes.map(item => item.count),

                    backgroundColor: [

                        "#0d6efd",
                        "#198754",
                        "#dc3545",
                        "#ffc107",
                        "#6f42c1",
                        "#20c997",
                        "#fd7e14",
                        "#0dcaf0",
                        "#6c757d"

                    ]

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false

            }

        });

    }

});
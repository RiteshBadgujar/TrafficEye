/* ======================================
   TrafficEye Dashboard Charts
====================================== */

document.addEventListener("DOMContentLoaded", function () {

    fetch("/chart-data/")
        .then(response => response.json())
        .then(data => {

            // ===============================
            // Monthly Violations Bar Chart
            // ===============================

            const monthlyChart = document.getElementById("monthlyChart");

            if (monthlyChart) {

                new Chart(monthlyChart, {

                    type: "bar",

                    data: {

                        labels: [
                            "Jan",
                            "Feb",
                            "Mar",
                            "Apr",
                            "May",
                            "Jun",
                            "Jul",
                            "Aug",
                            "Sep",
                            "Oct",
                            "Nov",
                            "Dec"
                        ],

                        datasets: [{

                            label: "Traffic Violations",

                            data: data.monthly,

                            backgroundColor: "#0d6efd"

                        }]

                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false

                    }

                });

            }

            // ===============================
            // Paid vs Pending Pie Chart
            // ===============================

            const statusChart = document.getElementById("statusChart");

            if (statusChart) {

                new Chart(statusChart, {

                    type: "pie",

                    data: {

                        labels: ["Paid", "Pending"],

                        datasets: [{

                            data: [

                                data.paid,

                                data.pending

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

            // ===============================
            // Violation Types Doughnut Chart
            // ===============================

            const violationChart = document.getElementById("violationChart");

            if (violationChart) {

                new Chart(violationChart, {

                    type: "doughnut",

                    data: {

                        labels: data.categories.labels,

                        datasets: [{

                            data: data.categories.values,

                            backgroundColor: [

                                "#0d6efd",

                                "#198754",

                                "#dc3545",

                                "#ffc107",

                                "#6f42c1",

                                "#20c997",

                                "#fd7e14"

                            ]

                        }]

                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false

                    }

                });

            }

            // ===============================
            // Yearly Line Chart
            // ===============================

            const yearlyChart = document.getElementById("yearlyChart");

            if (yearlyChart) {

                new Chart(yearlyChart, {

                    type: "line",

                    data: {

                        labels: data.yearly.labels,

                        datasets: [{

                            label: "Violations",

                            data: data.yearly.values,

                            borderColor: "#dc3545",

                            backgroundColor: "rgba(220,53,69,0.2)",

                            fill: true,

                            tension: 0.4

                        }]

                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false

                    }

                });

            }

        })
        .catch(error => {

            console.error("Error loading chart data:", error);

        });

});
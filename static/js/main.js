// =====================================
// 🔍 MAIN SCAN FUNCTION
// =====================================

async function scanURL() {

    const urlInput = document.getElementById("urlInput");
    const url = urlInput.value.trim();

    if (!url) {
        alert("Please enter a URL");
        return;
    }

    const scanBtn = document.querySelector(".scan-btn");
    if (scanBtn) scanBtn.innerText = "Scanning...";

    try {

        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("results").style.display = "block";

        // =====================================
        // 🔥 STATUS LOGIC (0/1 → Text Convert)
        // =====================================

        let hybridScore = Number(data.hybrid_score);
        let predictionValue = data.prediction;

        let statusText = "";
        let statusColor = "";

        if (predictionValue === "Secure") {
            statusText = "✅ Secure";
            statusColor = "green";
        } else if (predictionValue === "Suspicious") {
            statusText = "⚠ Suspicious";
            statusColor = "orange";
        } else if (predictionValue === "Phishing") {
            statusText = "🚨 Phishing";
            statusColor = "red";
        } else {
            // fallback
            statusText = predictionValue;
            statusColor = "black";
        }

        const predictionElement = document.getElementById("prediction");
        predictionElement.innerText = statusText;
        predictionElement.style.color = statusColor;

        // =====================================
        // TEXT VALUES
        // =====================================

        document.getElementById("riskScore").innerText =
            Number(data.risk_score).toFixed(2);

        document.getElementById("lstmScore").innerText =
            Number(data.lstm_score).toFixed(2);

        document.getElementById("hybridScore").innerText =
            hybridScore;

        document.getElementById("sslStatus").innerText = data.ssl_status;
        document.getElementById("domainAge").innerText = data.domain_age;
        document.getElementById("virusTotal").innerText =
            data.virustotal?.malicious ?? "0";

        document.getElementById("googleSafe").innerText =
            data.google_safe_browsing?.status ?? "Unknown";

        // =====================================
        // HYBRID SCORE COLOR
        // =====================================

        const hybridSpan = document.getElementById("hybridScore");

        if (hybridScore > 70) {
            hybridSpan.style.color = "red";
        } else if (hybridScore > 40) {
            hybridSpan.style.color = "orange";
        } else {
            hybridSpan.style.color = "green";
        }

        // =====================================
        // PROGRESS BAR
        // =====================================

        const riskBar = document.getElementById("riskBar");

        riskBar.style.width = hybridScore + "%";
        riskBar.innerText = hybridScore + "%";

        if (hybridScore > 70) {
            riskBar.className = "progress-bar bg-danger";
        } else if (hybridScore > 40) {
            riskBar.className = "progress-bar bg-warning";
        } else {
            riskBar.className = "progress-bar bg-success";
        }


        // =====================================
        // CHARTS
        // =====================================

        createCharts(data);

    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Check console.");
    } finally {
        if (scanBtn) scanBtn.innerText = "🚀 Scan URL";
    }
}


// =====================================
// 📊 CHART FUNCTION
// =====================================

function createCharts(data) {

    const gaugeCtx = document.getElementById("riskGauge")?.getContext("2d");
    if (gaugeCtx) {

        if (window.riskChart) window.riskChart.destroy();

        window.riskChart = new Chart(gaugeCtx, {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [data.risk_score, 100 - data.risk_score],
                    backgroundColor: ["red", "#e9ecef"],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: "80%",
                plugins: { tooltip: { enabled: false } }
            }
        });
    }
  
    }


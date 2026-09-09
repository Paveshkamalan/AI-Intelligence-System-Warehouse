const API = "http://127.0.0.1:8000";


// ============================================================
// UPDATE CLOCK
// ============================================================

function updateClock() {

    const now = new Date();

    document.getElementById("currentTime").textContent =
        now.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        });
}

setInterval(updateClock, 1000);
updateClock();
loadCCTV();
loadCCTVResults();
let finishedCameras = 0;

// ============================================================
// FETCH STATUS
// ============================================================

async function fetchStatus() {

    try {

        const response = await fetch(`${API}/api/status`);

        const data = await response.json();

        document.getElementById("workers").textContent =
            data.workers;

        document.getElementById("highRisk").textContent =
            data.high;

        document.getElementById("predictedHazards").textContent =
            data.predicted_hazards;

        document.getElementById("totalEvents").textContent =
            data.total_events;

        document.getElementById("critical").textContent =
            data.critical;

        document.getElementById("high").textContent =
            data.high;

        document.getElementById("medium").textContent =
            data.medium;

        document.getElementById("low").textContent =
            data.low;


        updateRiskBars(data);

        updateHighestRisk(data.highest_risk_worker);

    }

    catch (error) {

        console.error(
            "Status API error:",
            error
        );

    }
}


// ============================================================
// RISK BARS
// ============================================================

function updateRiskBars(data) {

    const total = data.workers || 1;

    document.getElementById("criticalBar").style.width =
        `${(data.critical / total) * 100}%`;

    document.getElementById("highBar").style.width =
        `${(data.high / total) * 100}%`;

    document.getElementById("mediumBar").style.width =
        `${(data.medium / total) * 100}%`;

    document.getElementById("lowBar").style.width =
        `${(data.low / total) * 100}%`;
}


// ============================================================
// HIGHEST RISK WORKER
// ============================================================

function updateHighestRisk(worker) {

    if (!worker) {

        document.getElementById("highestWorker").textContent =
            "No workers detected";

        document.getElementById("highestZone").textContent =
            "Zone: --";

        document.getElementById("highestScore").textContent =
            "0/100";

        return;
    }

    document.getElementById("highestWorker").textContent =
        `Worker ID ${worker.track_id}`;

    document.getElementById("highestZone").textContent =
        `Zone: ${worker.zone}`;

    document.getElementById("highestScore").textContent =
        `${worker.score}/100`;

    document.getElementById("scoreBar").style.width =
        `${worker.score}%`;
}


// ============================================================
// FETCH WORKERS
// ============================================================

async function fetchWorkers() {

    try {

        const response =
            await fetch(`${API}/api/workers`);

        const data =
            await response.json();

        const workers =
            data.workers || [];

        document.getElementById("workerCountBadge").textContent =
            `${workers.length} Workers`;

        const table =
            document.getElementById("workersTable");

        if (workers.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="4" class="loading">
                        No workers detected
                    </td>
                </tr>
            `;

            return;
        }


        table.innerHTML = workers.map(worker => {

            const level =
                worker.risk_level.toLowerCase();

            return `
                <tr>

                    <td>
                        <strong>
                            Worker ID ${worker.track_id}
                        </strong>
                    </td>

                    <td>
                        ${worker.zone}
                    </td>

                    <td>
                        <span class="risk-level risk-${level}">
                            ${worker.risk_level}
                        </span>
                    </td>

                    <td>
                        ${worker.score}/100
                    </td>

                </tr>
            `;

        }).join("");

    }

    catch (error) {

        console.error(
            "Workers API error:",
            error
        );

    }
}


// ============================================================
// FETCH EVENTS
// ============================================================

async function fetchEvents() {

    try {

        const response =
            await fetch(`${API}/api/events`);

        const data =
            await response.json();

        const events =
            data.events || [];

        const container =
            document.getElementById("eventsContainer");


        if (events.length === 0) {

            container.innerHTML = `
                <div class="loading">
                    No safety events detected
                </div>
            `;

            return;
        }


        const recent =
            events.slice(-10).reverse();


        container.innerHTML =
            recent.map(event => {

                return `
                    <div class="event">

                        <div>

                            <div class="event-type">
                                ${formatEventType(event.type)}
                            </div>

                            <div class="event-info">
                                Worker ID:
                                ${event.track_id ?? "--"}
                                ${event.zone ? ` • ${event.zone}` : ""}
                            </div>

                        </div>

                        <div class="event-risk">
                            ${event.worker_risk ?? ""}
                        </div>

                    </div>
                `;

            }).join("");

    }

    catch (error) {

        console.error(
            "Events API error:",
            error
        );

    }
}


// ============================================================
// EVENT NAME FORMATTER
// ============================================================

function formatEventType(type) {

    if (!type) {
        return "Safety Event";
    }

    return type
        .replaceAll("_", " ")
        .toLowerCase()
        .replace(/\b\w/g, char =>
            char.toUpperCase()
        );
}


// ============================================================
// MONITOR STATUS
// ============================================================

async function fetchMonitorStatus() {

    try {

        const response =
            await fetch(`${API}/api/monitor`);

        const data =
            await response.json();

        const indicator =
            document.querySelector(".live-indicator");

        if (data.running) {

            indicator.innerHTML = `
                <span></span>
                LIVE
            `;

        }

        else if (data.completed) {

            indicator.innerHTML = `
                <span></span>
                COMPLETE
            `;

        }

    }

    catch (error) {

        console.error(
            "Monitor API error:",
            error
        );

    }
}


// ============================================================
// INITIAL LOAD
// ============================================================

async function refreshDashboard() {

    await fetchStatus();
    await fetchWorkers();
    await fetchEvents();
    await fetchMonitorStatus();

}

refreshDashboard();


// ============================================================
// AUTO REFRESH
// ============================================================

setInterval(
    refreshDashboard,
    2000
);

async function loadCCTV() {

    const grid = document.getElementById("cctvGrid");

    if (!grid) return;

    try {

        const response = await fetch(`${API}/api/cctv`);

        const data = await response.json();

        grid.innerHTML = "";

        data.cameras.forEach(camera => {

            const card = document.createElement("div");

            card.className = "cctv-card";

            card.innerHTML = `
                <div class="cctv-header">

                    <span class="camera-name">
                        CAMERA ${String(camera.camera_id).padStart(2, "0")}
                    </span>

                    <span class="camera-status">
                        🔴 LIVE
                    </span>

                </div>

                <video
                    class="cctv-video"
                    autoplay
                    muted
                    playsinline
                >
                    <source
                        src="${API}${camera.video}"
                        type="video/mp4"
                    >
                </video>

                <div class="cctv-info">

                    <div class="cctv-alert">
                        🚨 ${camera.severity}
                    </div>

                    <div class="cctv-alert">
                        ${camera.title}
                    </div>

                    <div class="cctv-description">
                        ${camera.alert}
                    </div>

                    <div class="cctv-action">
                        <strong>Recommended:</strong>
                        ${camera.action}
                    </div>

                </div>
            `;

            grid.appendChild(card);

            const video = card.querySelector("video");

            video.addEventListener("ended", handleCameraEnded);

        });

    } catch (error) {

        console.error("CCTV error:", error);

    }
}

async function handleCameraEnded() {

    finishedCameras++;

    const totalCameras =
        document.querySelectorAll(".cctv-video").length;

    if (finishedCameras >= totalCameras) {

        finishedCameras = 0;

        try {

            await fetch(
                `${API}/api/cctv/next`,
                {
                    method: "POST"
                }
            );

            await loadCCTV();

        } catch (error) {

            console.error(
                "Failed to switch CCTV set:",
                error
            );

        }
    }
}


document.addEventListener("DOMContentLoaded", () => {
    loadCCTV();
});

async function loadCCTVResults() {

    try {

        const response =
            await fetch(`${API}/api/cctv/results`);

        const data =
            await response.json();

        updateCCTVResults(data);

    } catch (error) {

        console.error(
            "CCTV results error:",
            error
        );
    }
}

// ============================================================
// CCTV AI RESULTS
// ============================================================

function updateCCTVResults(data) {

    const cameras = data.cameras || [];
    const summary = data.summary || {};

    // --------------------------------------------------------
    // Update CCTV camera cards
    // --------------------------------------------------------

    const cards = document.querySelectorAll(".cctv-card");

    cameras.forEach((camera, index) => {

        const card = cards[index];

        if (!card) return;

        const info = card.querySelector(".cctv-info");

        if (!info) return;

        let riskClass = "low";

        if (camera.severity === "CRITICAL") {
            riskClass = "critical";
        }
        else if (camera.severity === "HIGH") {
            riskClass = "high";
        }
        else if (camera.severity === "MEDIUM") {
            riskClass = "medium";
        }

        info.innerHTML = `
            <div class="cctv-alert risk-${riskClass}">
                🚨 ${camera.severity}
            </div>

            <div class="cctv-alert">
                ${camera.incident}
            </div>

            <div class="cctv-description">
                ${camera.alert}
            </div>

            <div class="cctv-description">
                👷 Workers Visible:
                <strong>${camera.max_workers_visible}</strong>
            </div>

            <div class="cctv-description">
                🎯 Detection Coverage:
                <strong>${camera.detection_frames}</strong>
                frames
            </div>

            <div class="cctv-risk-score">
                Risk Score:
                <strong>${camera.risk_score}/100</strong>
            </div>

            <div class="cctv-action">
                <strong>Recommended Action:</strong><br>
                ${camera.recommended_action}
            </div>
        `;
    });

    // --------------------------------------------------------
    // Create overall CCTV intelligence panel
    // --------------------------------------------------------

    let panel = document.getElementById("cctvIntelligence");

    if (!panel) {

        panel = document.createElement("section");

        panel.id = "cctvIntelligence";

        panel.className = "cctv-intelligence";

        const cctvSection =
            document.querySelector(".camera-section");

        if (cctvSection) {
            cctvSection.appendChild(panel);
        }
    }

    if (!panel) return;

    panel.innerHTML = `

        <div class="section-header">

            <div>
                <h2>AI Safety Intelligence</h2>

                <p>
                    Cross-camera incident analysis
                </p>
            </div>

            <span class="live-badge">
                AI ANALYSIS
            </span>

        </div>

        <div class="ai-summary-grid">

            <div class="ai-stat">
                <span>Cameras Analyzed</span>
                <strong>${summary.cameras || 0}</strong>
            </div>

            <div class="ai-stat critical-stat">
                <span>Critical</span>
                <strong>${summary.critical || 0}</strong>
            </div>

            <div class="ai-stat high-stat">
                <span>High Risk</span>
                <strong>${summary.high || 0}</strong>
            </div>

            <div class="ai-stat">
                <span>Highest Risk</span>
                <strong>${summary.highest_risk || 0}/100</strong>
            </div>

        </div>

        ${
            summary.highest_camera
            ? `
                <div class="ai-alert-banner">

                    🚨
                    <strong>
                        Highest Risk: Camera
                        ${summary.highest_camera}
                    </strong>

                    <span>
                        ${summary.highest_incident}
                    </span>

                    <strong>
                        ${summary.highest_risk}/100
                    </strong>

                </div>
            `
            : ""
        }

    `;
}

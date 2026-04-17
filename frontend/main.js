const API_BASE = 'http://localhost:8000';

// App State
let state = {
    view: 'landing',
    user: null,
    matches: []
};

// DOM Elements
const appContainer = document.getElementById('app-container');
const hero = document.querySelector('.hero');
const stats = document.getElementById('statistics');

function init() {
    console.log('Hemohub initialized');
    setupEventListeners();
}

function setupEventListeners() {
    // Navigation Links
    document.querySelector('.nav-links a[href="#dashboard"]').addEventListener('click', (e) => { e.preventDefault(); renderDashboard(); });
    document.querySelector('.nav-links a[href="#request"]').addEventListener('click', (e) => { e.preventDefault(); renderRequestFlow(); });
    document.querySelector('.nav-links a[href="#trace"]').addEventListener('click', (e) => { e.preventDefault(); renderTraceView(); });
    
    // Buttons
    document.getElementById('login-btn').addEventListener('click', () => alert("Connect ID clicked! Future implementation for Web3/Auth flow."));
    document.querySelector('.btn-primary.large').addEventListener('click', renderBecomeDonor);
    document.querySelector('.btn-secondary.large').addEventListener('click', renderRequestFlow);

    // Stat Cards
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('click', () => {
            if (card.innerHTML.includes('Emergencies')) {
                renderEmergencies();
            } else if (card.innerHTML.includes('Live Donors')) {
                alert("Live Donors map view coming soon!");
            } else if (card.innerHTML.includes('Reliability')) {
                alert("Network reliability metrics detail view coming soon!");
            }
        });
        card.style.cursor = "pointer"; // Add pointer cursor
    });
}

function hideLanding() {
    hero.classList.add('hidden');
    stats.classList.add('hidden');
    appContainer.classList.remove('hidden');
}

function showLanding() {
    hero.classList.remove('hidden');
    stats.classList.remove('hidden');
    appContainer.classList.add('hidden');
    appContainer.innerHTML = '';
}

// --- VIEWS ---

function renderDashboard() {
    hideLanding();
    appContainer.innerHTML = `
        <div class="glass section-card">
            <h2 class="gradient-text">Donor Dashboard</h2>
            <div class="stats-grid mt-4">
                <div class="stat-card glass">
                    <h3>Your Reliability Score</h3>
                    <div class="value">100%</div>
                </div>
                <div class="stat-card glass">
                    <h3>Donations Made</h3>
                    <div class="value">0</div>
                </div>
                <div class="stat-card glass">
                    <h3>Status</h3>
                    <div class="value urgent" style="color: #4ade80;">Available</div>
                </div>
            </div>
            <button class="btn-primary mt-4" onclick="showLanding()">Back to Home</button>
        </div>
    `;
}

function renderTraceView() {
    hideLanding();
    appContainer.innerHTML = `
        <div class="glass section-card">
            <h2 class="gradient-text">Trace Blood Unit</h2>
            <p>Enter your unique Unit ID to view the lifecycle of the donated blood.</p>
            <div class="form-group mt-4">
                <input type="text" id="unit-id" placeholder="e.g., UNIT-A1B2C3D4" class="w-full">
            </div>
            <button class="btn-primary mt-2" onclick="alert('Unit tracking pipeline initializing...')">Track Unit</button>
        </div>
    `;
}

function renderBecomeDonor() {
    hideLanding();
    appContainer.innerHTML = `
        <div class="glass section-card">
            <h2 class="gradient-text">Become a Donor</h2>
            <p>Join the secure network. Your privacy is paramount.</p>
            <form id="donor-form" class="mt-4" onsubmit="event.preventDefault(); alert('Registration successful! You are now a donor.'); showLanding();">
                <div class="form-group">
                    <label>Blood Group</label>
                    <select required>
                        <option value="A+">A+</option><option value="A-">A-</option>
                        <option value="B+">B+</option><option value="B-">B-</option>
                        <option value="O+">O+</option><option value="O-">O-</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Phone Number (10 digits only)</label>
                    <input type="tel" required pattern="[0-9]{10}" title="Please enter exactly 10 digits" maxlength="10" placeholder="e.g. 9876543210">
                </div>
                <button type="submit" class="btn-primary mt-2">Register securely</button>
            </form>
        </div>
    `;
}

function renderEmergencies() {
    hideLanding();
    appContainer.innerHTML = `
        <div class="glass section-card">
            <h2 class="gradient-text">Active Emergencies (12)</h2>
            <p>High-reliability donors are prioritized in this list.</p>
            <div id="emergency-list" class="mt-4">
                <p class="loader">Fetching priority emergencies...</p>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        const emergencies = [
            { req_id: 101, bg: 'O-', distance: 5.2, priority: 'URGENT (Top Donor)' },
            { req_id: 102, bg: 'A+', distance: 12.1, priority: 'High' }
        ];
        
        document.getElementById('emergency-list').innerHTML = emergencies.map(e => `
            <div class="donor-card glass">
                <div class="donor-header">
                    <span class="id-badge urgent">Req #${e.req_id}</span>
                    <span class="distance">${e.bg} needed - ${e.distance} km away</span>
                </div>
                <p class="score mt-2">Status: <strong>${e.priority}</strong></p>
                <button class="btn-primary sm mt-2" onclick="renderRequestFlow()">Respond</button>
            </div>
        `).join('');
    }, 1000);
}

function renderRequestFlow() {
    hideLanding();
    appContainer.innerHTML = `
        <div class="glass section-card">
            <h2 class="gradient-text">Emergency Blood Request</h2>
            <p>Your privacy is protected. Donors will only see your Blood Group and Proximity.</p>
            
            <form id="request-form" class="mt-4">
                <div class="form-group">
                    <label>Blood Group Required</label>
                    <select id="blood-group" required>
                        <option value="A+">A+</option><option value="A-">A-</option>
                        <option value="B+">B+</option><option value="B-">B-</option>
                        <option value="O+">O+</option><option value="O-">O-</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Search Radius (km)</label>
                    <input type="number" id="radius" value="10" min="1" max="50">
                </div>
                <button type="submit" class="btn-primary mt-2">Search Nearby Donors</button>
            </form>

            <div id="matching-results" class="mt-4 hidden">
                <h3>Nearby Matches</h3>
                <div id="donor-list" class="donor-grid"></div>
            </div>
        </div>
    `;
    
    document.getElementById('request-form').addEventListener('submit', handleRequestSubmit);
}

async function handleRequestSubmit(e) {
    e.preventDefault();
    const resultsContainer = document.getElementById('matching-results');
    const listContainer = document.getElementById('donor-list');
    
    resultsContainer.classList.remove('hidden');
    listContainer.innerHTML = '<p class="loader">Scanning secure network...</p>';

    // Mocking the behavior for visual demo
    setTimeout(() => {
        const mockDonors = [
            { donor_id: 'DX982', distance: 1.2, reliability: 100, status: 'MATCHED' },
            { donor_id: 'BQ415', distance: 3.5, reliability: 95, status: 'MATCHED' }
        ];
        renderDonorList(mockDonors);
    }, 1500);
}

function renderDonorList(donors) {
    const listContainer = document.getElementById('donor-list');
    listContainer.innerHTML = donors.map(d => `
        <div class="donor-card glass" id="card-${d.donor_id}">
            <div class="donor-header">
                <span class="id-badge">ID: ${d.donor_id}</span>
                <span class="distance">${d.distance} km away</span>
            </div>
            <div class="reliability-bar">
                <div class="progress" style="width: ${d.reliability}%"></div>
            </div>
            <p class="score">Reliability: ${d.reliability}%</p>
            <p class="mt-2" id="phone-${d.donor_id}">Phone: ******** (Masked)</p>
            <button id="btn-${d.donor_id}" class="btn-primary sm mt-2" onclick="requestMutualConfirm('${d.donor_id}')">Request Connection</button>
        </div>
    `).join('');
}

function requestMutualConfirm(id) {
    const btn = document.getElementById(`btn-${id}`);
    btn.innerText = "Waiting for Donor...";
    btn.disabled = true;
    btn.style.background = "#94a3b8";

    // Simulate donor confirming on their end
    setTimeout(() => {
        const phoneField = document.getElementById(`phone-${id}`);
        phoneField.innerHTML = `Phone: <strong style="color: #4ade80;">+1 987 654 3210</strong> (Unmasked!)`;
        phoneField.style.color = "#4ade80";
        
        btn.innerText = "Connection Established!";
        btn.style.background = "#4ade80";
    }, 2000);
}

window.onload = init;

/* Main application logic */

const API_BASE_URL = '/api/v1';

/**
 * Session Display (optional - works without login)
 */
window.addEventListener('load', () => {
    const userDisplay = document.getElementById('userDisplay');
    const logoutBtn = document.getElementById('logoutBtn');
    const loginLink = document.getElementById('loginLink');
    const user = sessionStorage.getItem('user');
    
    if (user) {
        try {
            const userData = JSON.parse(user);
            if (userDisplay) userDisplay.innerHTML = userData.is_guest 
                ? `<i class="fas fa-user"></i> ${userData.username}` 
                : `<i class="fas fa-user"></i> ${userData.email}`;
            if (logoutBtn) { logoutBtn.classList.remove('d-none'); logoutBtn.classList.add('d-inline-block'); }
            if (loginLink) loginLink.classList.add('d-none');
        } catch (e) {
            if (userDisplay) userDisplay.textContent = 'Guest';
        }
    } else {
        if (userDisplay) userDisplay.textContent = 'Guest';
        if (loginLink) loginLink.classList.remove('d-none');
    }
});

function logout() {
    const sessionId = sessionStorage.getItem('sessionId');
    if (sessionId) {
        fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        }).catch(() => {});
    }
    sessionStorage.removeItem('sessionId');
    sessionStorage.removeItem('user');
    window.location.reload();
}

// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const uploadZone = document.getElementById('uploadZone');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const confidenceThreshold = document.getElementById('confidenceThreshold');
const thresholdValue = document.getElementById('thresholdValue');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorAlert = document.getElementById('errorAlert');

let selectedFile = null;

// Event Listeners
uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', handleDragOver);
uploadZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
confidenceThreshold.addEventListener('input', updateThresholdValue);
uploadForm.addEventListener('submit', handleAnalysis);

// File Selection Handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        loadAndDisplayImage(file);
    }
}

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadZone.style.backgroundColor = 'rgba(40, 167, 69, 0.2)';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadZone.style.backgroundColor = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        loadAndDisplayImage(files[0]);
    }
}

// Load and Display Image
function loadAndDisplayImage(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }

    selectedFile = file;
    fileInput.files = (() => {
        const dt = new DataTransfer();
        dt.items.add(file);
        return dt.files;
    })();

    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
        uploadZone.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Clear Image
function clearImage() {
    selectedFile = null;
    fileInput.value = '';
    previewContainer.style.display = 'none';
    uploadZone.style.display = 'block';
    resultsSection.style.display = 'none';
    errorAlert.style.display = 'none';
}

// Update Threshold Display
function updateThresholdValue() {
    thresholdValue.textContent = parseFloat(confidenceThreshold.value).toFixed(2);
}

// Main Analysis Handler
async function handleAnalysis(e) {
    e.preventDefault();

    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Show loading state
        analyzeBtn.disabled = true;
        loadingSpinner.style.display = 'block';
        errorAlert.style.display = 'none';
        resultsSection.style.display = 'none';

        // Make API request
        const response = await fetch(`${API_BASE_URL}/analyze?confidence_threshold=${parseFloat(confidenceThreshold.value)}`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            showError(data.error || 'Analysis failed');
            return;
        }

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Analysis error:', error);
        showError('Network error: ' + error.message);
    } finally {
        // Reset loading state
        analyzeBtn.disabled = false;
        loadingSpinner.style.display = 'none';
    }
}

// Display Results
function displayResults(data) {
    const analysis = data.analysis;
    const carePlan = data.care_plan;
    const isAI = data.analysis_type === 'ai';

    // ========== PLANT IDENTIFICATION (AI only) ==========
    const plantInfoCard = document.getElementById('plantInfoCard');
    if (isAI && data.plant_info && data.plant_info.common_name) {
        const pi = data.plant_info;
        plantInfoCard.style.display = 'block';
        document.getElementById('plantCommonName').textContent = pi.common_name || 'Unknown Plant';
        document.getElementById('plantScientificName').textContent = pi.scientific_name ? `(${pi.scientific_name})` : '';
        document.getElementById('plantDescription').textContent = pi.description || '';
        document.getElementById('plantFamily').textContent = pi.family || '-';
        document.getElementById('plantTypeInfo').textContent = pi.plant_type || '-';
        document.getElementById('plantOrigin').textContent = pi.origin || '-';
        document.getElementById('plantTypeBadge').textContent = `🌿 ${pi.plant_type || 'Plant'}`;

        const ic = pi.ideal_conditions || {};
        document.getElementById('idealSunlight').textContent = ic.sunlight || '-';
        document.getElementById('idealTemp').textContent = ic.temperature || '-';
        document.getElementById('idealHumidity').textContent = ic.humidity || '-';
        document.getElementById('idealSoil').textContent = ic.soil || '-';

        const gc = pi.general_care || {};
        document.getElementById('generalWatering').innerHTML = `💧 <strong>Watering:</strong> ${gc.watering || '-'}`;
        document.getElementById('generalFertilizing').innerHTML = `🧪 <strong>Fertilizing:</strong> ${gc.fertilizing || '-'}`;
        document.getElementById('generalPruning').innerHTML = `✂️ <strong>Pruning:</strong> ${gc.pruning || '-'}`;

        const issues = gc.common_issues || [];
        const issuesDiv = document.getElementById('commonIssuesDiv');
        const issuesList = document.getElementById('commonIssuesList');
        if (issues.length > 0) {
            issuesDiv.style.display = 'block';
            issuesList.innerHTML = issues.map(i => `<span class="issue-chip">${i}</span>`).join('');
        } else {
            issuesDiv.style.display = 'none';
        }
    } else {
        plantInfoCard.style.display = 'none';
    }

    // ========== DISEASE DETECTION ==========
    const disease = analysis.disease_detection;
    document.getElementById('diseaseName').textContent = isAI 
        ? disease.primary_disease 
        : formatDiseaseName(disease.primary_disease);
    document.getElementById('diseaseDescription').textContent = disease.description || 'No description available';
    
    // Disease type badge
    const dtBadge = document.getElementById('diseaseTypeBadge');
    const dtype = disease.disease_type || 'unknown';
    dtBadge.textContent = dtype.replace('_', ' ').toUpperCase();

    // Confidence
    const confidencePercent = (disease.confidence * 100);
    document.getElementById('confidenceText').textContent = `${confidencePercent.toFixed(1)}%`;
    const confidenceBarEl = document.getElementById('confidenceBar');
    confidenceBarEl.style.width = `${confidencePercent}%`;
    if (confidencePercent >= 75) confidenceBarEl.className = 'progress-bar bg-success';
    else if (confidencePercent >= 50) confidenceBarEl.className = 'progress-bar bg-warning';
    else confidenceBarEl.className = 'progress-bar bg-danger';

    // Severity Badge - beautiful pill
    const severityBadge = document.getElementById('severityBadge');
    const sev = disease.severity || 'unknown';
    severityBadge.textContent = sev.toUpperCase();
    severityBadge.className = 'sev-pill sev-' + sev;

    // Causes - styled items
    const causes = disease.common_causes || [];
    const causesList = document.getElementById('causesList');
    causesList.innerHTML = causes.length > 0
        ? causes.map(c => `<div class="cause-item"><i class="fas fa-arrow-right"></i><span>${c}</span></div>`).join('')
        : '<div class="cause-item"><i class="fas fa-info-circle"></i><span class="text-muted">No specific causes identified</span></div>';

    // Health Score Gauge (SVG circle)
    const healthScore = disease.health_score || 0;
    const gaugeCircle = document.getElementById('healthGaugeCircle');
    const circumference = 314; // 2 * PI * 50
    const offset = circumference - (healthScore / 100) * circumference;
    gaugeCircle.style.strokeDashoffset = offset;
    if (healthScore >= 70) gaugeCircle.style.stroke = '#10b981';
    else if (healthScore >= 40) gaugeCircle.style.stroke = '#f59e0b';
    else gaugeCircle.style.stroke = '#ef4444';
    
    document.getElementById('healthScoreNumber').textContent = healthScore;
    const healthText = document.getElementById('healthScoreText');
    if (healthScore >= 70) { healthText.textContent = '✅ Good condition'; healthText.style.color = '#10b981'; }
    else if (healthScore >= 40) { healthText.textContent = '⚠️ Needs attention'; healthText.style.color = '#f59e0b'; }
    else { healthText.textContent = '🚨 Critical!'; healthText.style.color = '#ef4444'; }

    // Symptoms - chips
    const symptoms = disease.symptoms_observed || [];
    const symptomsSection = document.getElementById('symptomsSection');
    const symptomsList = document.getElementById('symptomsList');
    if (symptoms.length > 0) {
        symptomsSection.style.display = 'block';
        symptomsList.innerHTML = symptoms.map(s => 
            `<span class="symptom-chip"><i class="fas fa-circle"></i> ${s}</span>`
        ).join('');
    } else {
        symptomsSection.style.display = 'none';
    }

    // Risk warning
    const risk = disease.risk_if_untreated || carePlan.risk_if_untreated || '';
    const riskSection = document.getElementById('riskSection');
    if (risk) {
        riskSection.style.display = 'block';
        document.getElementById('riskText').textContent = risk;
    } else {
        riskSection.style.display = 'none';
    }

    // Care Plan
    if (isAI) {
        displayAICarePlan(carePlan);
    } else if (carePlan.success) {
        displayCarePlan(carePlan);
    }

    // Hide detailed feature/ROI analysis for AI results
    const detailsCard = document.getElementById('detailsCard');
    if (isAI) {
        detailsCard.style.display = 'none';
    } else {
        detailsCard.style.display = 'block';
        document.getElementById('featureAnalysis').innerHTML = formatFeatureAnalysis(analysis.feature_analysis);
        document.getElementById('roiAnalysis').innerHTML = formatROIAnalysis(analysis.roi_analysis);
    }

    resultsSection.style.display = 'block';
    const scrollTarget = isAI && plantInfoCard.style.display !== 'none' 
        ? plantInfoCard : document.getElementById('diseaseCard');
    window.scrollTo({ top: scrollTarget.offsetTop - 100, behavior: 'smooth' });
}

// Display AI-powered Care Plan
function displayAICarePlan(carePlan) {
    // Urgency Alert
    const urgencyAlert = document.getElementById('urgencyAlert');
    const sev = carePlan.severity || 'moderate';
    if (sev === 'severe') {
        urgencyAlert.className = 'alert alert-danger';
        urgencyAlert.innerHTML = `<strong>🚨 CRITICAL — Immediate action required!</strong><br><small>This condition is severe and needs urgent treatment.</small>`;
    } else if (sev === 'moderate') {
        urgencyAlert.className = 'alert alert-warning';
        urgencyAlert.innerHTML = `<strong>⚠️ Moderate condition detected</strong><br><small>Treatment should begin within 2-3 days for best results.</small>`;
    } else if (sev === 'none' || carePlan.disease === 'Healthy') {
        urgencyAlert.className = 'alert alert-success';
        urgencyAlert.innerHTML = `<strong>✅ Plant looks healthy!</strong><br><small>Continue with regular care routine.</small>`;
    } else {
        urgencyAlert.className = 'alert alert-info';
        urgencyAlert.innerHTML = `<strong>ℹ️ Mild condition detected</strong><br><small>Monitor and treat within the next week.</small>`;
    }

    // Immediate Actions - styled steps
    const priorityActions = document.getElementById('priorityActions');
    const actions = carePlan.immediate_actions || [];
    priorityActions.innerHTML = actions.length > 0
        ? actions.map((a, i) => `<div class="action-step"><span class="action-num">${i+1}</span><span class="action-text">${a}</span></div>`).join('')
        : '<div class="action-step"><span class="action-num">—</span><span class="action-text text-muted">No specific actions needed</span></div>';

    // Watering Guide
    const wateringGuide = document.getElementById('wateringGuide');
    const watering = carePlan.watering_advice || {};
    wateringGuide.innerHTML = `
        <p><strong><i class="fas fa-tint text-primary"></i> Frequency:</strong> ${watering.frequency || 'N/A'}</p>
        <p><strong><i class="fas fa-hand-holding-water text-primary"></i> Method:</strong> ${watering.method || 'N/A'}</p>
        <p class="mb-0"><strong><i class="fas fa-fill-drip text-primary"></i> Amount:</strong> ${watering.amount || 'N/A'}</p>
    `;

    // Fertilizing
    const fertilizingGuide = document.getElementById('fertilizingGuide');
    fertilizingGuide.innerHTML = '<p class="mb-0 text-muted">See treatment options for specific recommendations.</p>';

    // Treatment Options - styled items
    const treatment = carePlan.treatment || {};
    
    document.getElementById('organicTreatment').innerHTML = (treatment.organic || []).length > 0
        ? treatment.organic.map(item => `<div class="treat-item"><i class="fas fa-leaf text-success"></i><span>${item}</span></div>`).join('')
        : '<div class="treat-item text-muted">No organic treatments specified</div>';

    document.getElementById('chemicalTreatment').innerHTML = (treatment.chemical || []).length > 0
        ? treatment.chemical.map(item => `<div class="treat-item"><i class="fas fa-flask text-info"></i><span>${item}</span></div>`).join('')
        : '<div class="treat-item text-muted">No chemical treatments specified</div>';

    document.getElementById('culturalTreatment').innerHTML = (treatment.cultural || []).length > 0
        ? treatment.cultural.map(item => `<div class="treat-item"><i class="fas fa-seedling text-success"></i><span>${item}</span></div>`).join('')
        : '<div class="treat-item text-muted">No cultural treatments specified</div>';

    // Recovery Timeline - beautiful steps
    const timeline = document.getElementById('timeline');
    const recovery = carePlan.recovery_timeline || {};
    timeline.innerHTML = `
        <div class="tl-step">
            <span class="tl-dot tl-1">1</span>
            <div><div class="tl-label">First Improvement</div><div class="tl-val">${recovery.first_improvement || 'N/A'}</div></div>
        </div>
        <div class="tl-step">
            <span class="tl-dot tl-2">2</span>
            <div><div class="tl-label">Significant Recovery</div><div class="tl-val">${recovery.significant_recovery || 'N/A'}</div></div>
        </div>
        <div class="tl-step">
            <span class="tl-dot tl-3">3</span>
            <div><div class="tl-label">Full Recovery</div><div class="tl-val">${recovery.full_recovery || 'N/A'}</div></div>
        </div>
    `;

    // Prevention - styled items
    const prevention = carePlan.prevention || [];
    const preventionSection = document.getElementById('preventionSection');
    const preventionList = document.getElementById('preventionList');
    if (prevention.length > 0) {
        preventionSection.style.display = 'block';
        preventionList.innerHTML = prevention.map(p => 
            `<div class="prev-item"><i class="fas fa-shield-alt"></i><span>${p}</span></div>`
        ).join('');
    } else {
        preventionSection.style.display = 'none';
    }

    // Tips
    const tipsList = document.getElementById('tipsList');
    const tips = carePlan.immediate_actions ? carePlan.immediate_actions.slice(0, 3) : [];
    tipsList.innerHTML = tips.length > 0
        ? tips.map(tip => `<div class="tip-item"><i class="fas fa-lightbulb"></i><span>${tip}</span></div>`).join('')
        : '<div class="tip-item text-muted">No additional tips</div>';
}

// Display Care Plan
function displayCarePlan(carePlan) {
    const care = carePlan.care_plan;

    // Urgency Alert
    const urgencyAlert = document.getElementById('urgencyAlert');
    urgencyAlert.innerHTML = `<strong>⚠️ ${care.urgency}</strong><br><small>${care.timeline}</small>`;

    // Priority Actions
    const priorityActions = document.getElementById('priorityActions');
    priorityActions.innerHTML = carePlan.priority_actions
        .map(action => `<li class="list-group-item"><i class="fas fa-check-circle text-success"></i> ${action}</li>`)
        .join('');

    // Watering Guide
    const wateringGuide = document.getElementById('wateringGuide');
    const watering = care.watering || {};
    wateringGuide.innerHTML = `
        <p><strong>Frequency:</strong> ${watering.frequency || 'N/A'}</p>
        <p><strong>Amount:</strong> ${watering.amount || 'N/A'}</p>
        <p class="mb-0"><strong>Tip:</strong> ${watering.tip || 'N/A'}</p>
    `;

    // Fertilizing Guide
    const fertilizingGuide = document.getElementById('fertilizingGuide');
    const fertilizing = care.fertilizing || {};
    fertilizingGuide.innerHTML = `
        <p><strong>Frequency:</strong> ${fertilizing.frequency || 'N/A'}</p>
        <p><strong>Type:</strong> ${fertilizing.type || 'N/A'}</p>
        <p class="mb-0"><strong>Tip:</strong> ${fertilizing.tip || 'N/A'}</p>
    `;

    // Treatment Options
    const treatment = care.treatment || {};
    const organicTreatment = document.getElementById('organicTreatment');
    const chemicalTreatment = document.getElementById('chemicalTreatment');

    organicTreatment.innerHTML = (treatment.organic || [])
        .map(item => `<li class="list-group-item">${item}</li>`)
        .join('');

    chemicalTreatment.innerHTML = (treatment.chemical || [])
        .map(item => `<li class="list-group-item">${item}</li>`)
        .join('');

    // Timeline
    const timeline = document.getElementById('timeline');
    const timelineData = carePlan.timeline || {};
    timeline.innerHTML = `
        <p><strong>Assessment:</strong> ${timelineData.assessment || 'N/A'}</p>
        <p><strong>Initial Treatment:</strong> ${timelineData.initial_treatment || 'N/A'}</p>
        <p><strong>First Improvement Signs:</strong> ${timelineData.first_signs_improvement || 'N/A'}</p>
        <p><strong>Significant Improvement:</strong> ${timelineData.significant_improvement || 'N/A'}</p>
        <p class="mb-0"><strong>Full Recovery:</strong> ${timelineData.full_recovery || 'N/A'}</p>
    `;

    // Tips
    const tipsList = document.getElementById('tipsList');
    tipsList.innerHTML = (carePlan.tips || [])
        .map(tip => `<li class="list-group-item"><i class="fas fa-lightbulb text-warning"></i> ${tip}</li>`)
        .join('');
}

// Format Disease Name
function formatDiseaseName(name) {
    return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

// Format Feature Analysis
function formatFeatureAnalysis(features) {
    return `
        <p><strong>Color Variance:</strong> ${features.color_variance.toFixed(2)}</p>
        <p><strong>Brightness:</strong> ${features.brightness.toFixed(2)}</p>
        <p><strong>Contrast:</strong> ${features.contrast.toFixed(2)}</p>
        <p><strong>Greenness:</strong> ${features.greenness.toFixed(2)}</p>
        <p><strong>Edge Density:</strong> ${features.edge_density.toFixed(4)}</p>
        <p class="mb-0"><strong>Damaged Pixels:</strong> ${(features.damaged_pixels_ratio * 100).toFixed(2)}%</p>
    `;
}

// Format ROI Analysis
function formatROIAnalysis(roi) {
    return `
        <p><strong>Total ROIs Analyzed:</strong> ${roi.total_rois}</p>
        <p><strong>Affected Regions:</strong> ${roi.affected_rois}</p>
        <p><strong>Healthy Regions:</strong> ${roi.healthy_rois}</p>
        <p class="mb-0"><strong>Affected Percentage:</strong> ${roi.affected_percentage}%</p>
    `;
}

// Error Display
function showError(message) {
    errorAlert.textContent = '❌ ' + message;
    errorAlert.style.display = 'block';
    resultsSection.style.display = 'none';
}

// Placeholder Functions for Quick Links
function showDiseaseInfo() {
    alert('Detectable Diseases:\n\n✓ Leaf Spot\n✓ Powdery Mildew\n✓ Rust\n✓ Blight\n✓ Yellowing\n✓ Wilting\n✓ Pest Damage\n✓ Healthy');
}

function showTips() {
    alert('Plant Care Tips:\n\n1. Water consistently but don\'t overwater\n2. Ensure good air circulation\n3. Keep leaves clean\n4. Remove diseased leaves immediately\n5. Isolate infected plants\n6. Use proper lighting\n7. Monitor regularly');
}

function showAbout() {
    alert('Smart Plant Health Assistant\n\nVersion 1.0.0\n\nThis AI-powered tool helps you:\n- Identify plant diseases from images\n- Get personalized care advice\n- Monitor plant health\n- Prevent disease spread\n\nPowered by advanced image analysis and plant science knowledge.');
}

// Initialize
console.log('Smart Plant Health Assistant - Frontend Loaded');

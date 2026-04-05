// ========== CONFIG ==========
const API_URL = window.location.protocol === 'file:' || window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000/api' : '/api';
let currentUser = null;
let userProfile = null;
let activeChatWith = null;

// ========== API HELPER ==========
async function apiCall(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('roomie_token');
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    
    let options = { method, headers };
    
    if (body) {
        if (body instanceof FormData) {
            options.body = body;
        } else {
            headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(body);
        }
    }
    
    const res = await fetch(`${API_URL}${endpoint}`, options);
    if (!res.ok) {
        if (res.status === 401 && endpoint !== '/auth/login') {
            signOut();
        }
        const err = await res.text();
        throw new Error(err);
    }
    
    const contentType = res.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        return res.json();
    }
    return res.blob();
}

// ========== INITIALIZATION ==========
async function init() {
    const token = localStorage.getItem('roomie_token');
    if (token) {
        try {
            currentUser = await apiCall('/auth/me');
            currentUser.name = currentUser.full_name;
            userProfile = currentUser.profile || {};
            showMainApp();
            return;
        } catch (e) {
            console.error("Session expired", e);
            signOut();
        }
    }
    showAuthModal();
}

// ========== AUTH ==========
async function login() {
    const email = document.getElementById('authEmail').value;
    const password = document.getElementById('authPassword').value;
    const errObj = document.getElementById('authError');
    if (!email || !password) return errObj.innerText = "Email and Password required", errObj.style.display = 'block';
    
    try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        
        const res = await apiCall('/auth/login', 'POST', formData);
        localStorage.setItem('roomie_token', res.access_token);
        errObj.style.display = 'none';
        
        await init(); // Reload user data
    } catch (e) {
        errObj.innerText = "Login failed: Incorrect credentials";
        errObj.style.display = 'block';
    }
}

async function register() {
    const name = document.getElementById('authName').value;
    const email = document.getElementById('authEmail').value;
    const password = document.getElementById('authPassword').value;
    const errObj = document.getElementById('authError');
    
    if (!name || !email || !password) return errObj.innerText = "Name, Email, and Password required", errObj.style.display = 'block';
    
    try {
        await apiCall('/auth/register', 'POST', { full_name: name, email, password });
        errObj.style.display = 'none';
        alert('Registration successful! Logging you in...');
        await login();
    } catch (e) {
        errObj.innerText = "Registration failed: " + e.message;
        errObj.style.display = 'block';
    }
}

function signOut() {
    currentUser = null;
    userProfile = null;
    localStorage.removeItem('roomie_token');
    showAuthModal();
}

function showMainApp() {
    document.getElementById('authModal').style.display = 'none';
    document.getElementById('mainApp').style.display = 'block';
    document.getElementById('userName').innerText = currentUser.name;
    loadProfileIntoForm();
    renderMatches();
    renderCommunityMessages();
}

function showAuthModal() {
    document.getElementById('authModal').style.display = 'flex';
    document.getElementById('mainApp').style.display = 'none';
}

// ========== PROFILE ==========
function loadProfileIntoForm() {
    document.getElementById('profileName').value = currentUser.name || '';
    if (!userProfile) return;
    
    if (userProfile.profession) document.getElementById('profileProfession').value = userProfile.profession;
    if (userProfile.sleep_pattern) document.getElementById('profileSleep').value = userProfile.sleep_pattern;
    if (userProfile.personality) document.getElementById('profilePersonality').value = userProfile.personality;
    if (userProfile.cleanliness) document.getElementById('profileCleanliness').value = userProfile.cleanliness;
    if (userProfile.noise_tolerance) document.getElementById('profileNoise').value = userProfile.noise_tolerance;
    
    const roomPrefRadios = document.querySelectorAll('input[name="roomType"]');
    roomPrefRadios.forEach(radio => {
        if (radio.value === userProfile.room_preference) {
            radio.checked = true;
        }
    });
}

async function saveUserProfile() {
    const selectedRoom = document.querySelector('input[name="roomType"]:checked');
    const updateData = {
        profession: document.getElementById('profileProfession').value,
        sleep_pattern: document.getElementById('profileSleep').value,
        personality: document.getElementById('profilePersonality').value,
        cleanliness: document.getElementById('profileCleanliness').value,
        noise_tolerance: document.getElementById('profileNoise').value,
        room_preference: selectedRoom ? selectedRoom.value : 'shared',
        bedtime: "10 PM", // Defaults
        wake_time: "7 AM",
        sleep_type: "Light Sleeper",
        social_energy_rating: 5
    };
    
    try {
        const updated = await apiCall('/profile', 'PUT', updateData);
        userProfile = updated;
        alert("✅ Profile saved! Your matches have been updated.");
        renderMatches();
    } catch (e) {
        alert("Failed to save profile: " + e.message);
    }
}

// ========== MATCHES ==========
async function renderMatches() {
    const grid = document.getElementById('matchesGrid');
    if (!grid) return;
    
    try {
        const matches = await apiCall('/matches?limit=10');
        grid.innerHTML = '';
        
        matches.forEach(roommate => {
            const score = roommate.compatibility_score ? Math.round(roommate.compatibility_score) : 85;
            const prof = roommate; // Attributes are flat on the RoommateRecord
            const roomPrefIcon = prof.room_preference === 'single-bedded' ? '🛏️ Single Bed' : (prof.room_preference === 'studio' ? '🏢 Studio' : '🏠 Shared');
            
            const card = document.createElement('div');
            card.className = 'match-card';
            card.innerHTML = `
                <div class="card-header">
                    <div>
                        <strong style="font-size: 1.1rem;">👤 ${roommate.full_name}</strong>
                        <div style="font-size: 0.8rem; color: #6b7280;">${prof.profession || 'N/A'}</div>
                    </div>
                    <div class="compatibility">${score}% Match</div>
                </div>
                <div class="detail-item">
                    <span class="detail-icon"><i class="fas fa-moon"></i></span>
                    <span>Sleep: ${prof.sleep_pattern || 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon"><i class="fas fa-smile"></i></span>
                    <span>${prof.personality || 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon"><i class="fas fa-volume-up"></i></span>
                    <span>Noise: ${prof.noise_tolerance || 'N/A'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon"><i class="fas fa-bed"></i></span>
                    <span>Prefers: ${roomPrefIcon}</span>
                </div>
                <button class="chat-btn" data-roommate-id="${roommate.id}" data-roommate-name="${roommate.full_name}">
                    <i class="fas fa-comment-dots"></i> Chat Privately
                </button>
            `;
            grid.appendChild(card);
        });
        
        document.querySelectorAll('.chat-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const roommateId = parseInt(btn.dataset.roommateId);
                const roommateName = btn.dataset.roommateName;
                openChat(roommateId, roommateName);
            });
        });
    } catch (e) {
        console.error("Failed to load matches", e);
    }
}

// ========== PRIVATE CHAT ==========
function openChat(roommateId, roommateName) {
    activeChatWith = { id: roommateId, name: roommateName };
    const chatModal = document.getElementById('chatModal');
    document.getElementById('chatPartnerName').innerText = `Chat with ${roommateName}`;
    chatModal.classList.add('active');
    renderPrivateChatMessages();
}

async function renderPrivateChatMessages() {
    if (!activeChatWith) return;
    const messagesDiv = document.getElementById('chatMessages');
    
    try {
        const msgs = await apiCall(`/chat/${activeChatWith.id}/messages`);
        messagesDiv.innerHTML = '';
        
        msgs.forEach(msg => {
            const isSent = msg.sender_id === currentUser.id;
            const msgDiv = document.createElement('div');
            msgDiv.className = `chat-message ${isSent ? 'sent' : 'received'}`;
            msgDiv.innerHTML = `
                <div style="font-size: 0.7rem; margin-bottom: 0.25rem;">${isSent ? 'You' : msg.sender_name}</div>
                <div>${escapeHtml(msg.text)}</div>
                <div style="font-size: 0.6rem; margin-top: 0.25rem; opacity: 0.7;">${new Date(msg.created_at).toLocaleTimeString()}</div>
            `;
            messagesDiv.appendChild(msgDiv);
        });
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (e) {
        console.error("Failed to fetch private chat", e);
    }
}

async function sendPrivateMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message || !activeChatWith) return;
    
    try {
        await apiCall(`/chat/${activeChatWith.id}/messages`, 'POST', { text: message });
        input.value = '';
        renderPrivateChatMessages();
    } catch (e) {
        alert("Failed to send message: " + e.message);
    }
}

// ========== COMMUNITY CHAT ==========
async function renderCommunityMessages() {
    const container = document.getElementById('communityMessages');
    if (!container) return;
    
    try {
        const msgs = await apiCall('/community/messages');
        container.innerHTML = '';
        
        msgs.forEach(msg => {
            const msgDiv = document.createElement('div');
            msgDiv.className = 'community-message';
            msgDiv.innerHTML = `
                <div class="message-author">
                    <i class="fas fa-user-circle"></i> ${escapeHtml(msg.sender_name)}
                </div>
                <div>${escapeHtml(msg.text)}</div>
                <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 0.25rem;">
                    ${new Date(msg.created_at).toLocaleString()}
                </div>
            `;
            container.appendChild(msgDiv);
        });
        container.scrollTop = container.scrollHeight;
    } catch (e) {
        console.error("Failed to load community chat", e);
    }
}

async function sendCommunityMessage() {
    const input = document.getElementById('communityInput');
    const message = input.value.trim();
    if (!message) return;
    
    try {
        await apiCall('/community/messages', 'POST', { text: message });
        input.value = '';
        renderCommunityMessages();
    } catch (e) {
        alert("Failed to send message: " + e.message);
    }
}

// ========== DOWNLOAD AGREEMENT ==========
async function downloadAgreement() {
    try {
        const blob = await apiCall('/agreement/download');
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Roommate_Agreement_${currentUser.name}_${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (e) {
        alert("Failed to download agreement: " + e.message);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== TABS MAP ==========
function switchTabs() {
    const tabs = document.querySelectorAll('.tab');
    const profilePanel = document.getElementById('profilePanel');
    const matchesPanel = document.getElementById('matchesPanel');
    const communityPanel = document.getElementById('communityPanel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            profilePanel.style.display = 'none';
            matchesPanel.style.display = 'none';
            communityPanel.style.display = 'none';
            
            if (tabName === 'profile') profilePanel.style.display = 'block';
            else if (tabName === 'matches') {
                matchesPanel.style.display = 'block';
                renderMatches();
            }
            else if (tabName === 'community') {
                communityPanel.style.display = 'block';
                renderCommunityMessages();
            }
        });
    });
}

// ========== EVENTS LISTENER HOOKUP ==========
document.getElementById('loginBtn').addEventListener('click', login);
document.getElementById('registerBtn').addEventListener('click', register);
document.getElementById('logoutBtn').addEventListener('click', signOut);
document.getElementById('downloadAgreementBtn').addEventListener('click', downloadAgreement);
document.getElementById('saveProfileBtn').addEventListener('click', saveUserProfile);
document.getElementById('sendCommunityBtn').addEventListener('click', sendCommunityMessage);
document.getElementById('closeChatBtn').addEventListener('click', () => {
    document.getElementById('chatModal').classList.remove('active');
    activeChatWith = null;
});
document.getElementById('sendChatBtn').addEventListener('click', sendPrivateMessage);
document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendPrivateMessage();
});
document.getElementById('communityInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendCommunityMessage();
});
document.getElementById('userAvatarBtn').addEventListener('click', () => {
    document.querySelector('.tab[data-tab="profile"]').click();
});

switchTabs();
init();

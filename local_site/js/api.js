// API Base URL - automatically detects environment
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000'  // Local development
  : 'https://bucksport-api.onrender.com';  // Production - UPDATE THIS with your Render API URL

async function fetchInventory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/inventory`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching inventory:', error);
        return [];
    }
}

async function fetchInventorySummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/inventory/summary`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching inventory summary:', error);
        return null;
    }
}

async function fetchCoaches() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/coaches`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching coaches:', error);
        return [];
    }
}

async function fetchBoardMembers() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/board-members`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching board members:', error);
        return [];
    }
}

async function fetchTeams() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/teams`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching teams:', error);
        return [];
    }
}

async function fetchCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/inventory/categories`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching categories:', error);
        return [];
    }
}

async function fetchStatuses() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/inventory/statuses`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching statuses:', error);
        return [];
    }
}

const fetchEvents = () => fetchData('/api/events');
const fetchConcessions = () => fetchData('/api/concessions');
const fetchEventUsage = (eventId) => fetchData(`/api/events/${eventId}/usage`);

async function postData(endpoint, data, method = 'POST') {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, body: ${errorBody}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Could not post data to ${endpoint}:`, error);
        throw error;
    }
}

const saveEventUsage = (eventId, usageData) => postData(`/api/events/${eventId}/usage`, usageData);
const syncEventInventory = (eventId) => postData(`/api/events/${eventId}/sync`, {});
const addConcessionItem = (itemData) => postData('/api/concessions', itemData);

const fetchSchedule = () => fetchData('/api/schedule');
const fetchLocations = () => fetchData('/api/locations');
const requestNewEvent = (eventData) => postData('/api/schedule/request', eventData);

async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching from ${endpoint}:`, error);
        return [];
    }
}

async function updateBoardMember(id, data) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/board-members/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, body: ${errorBody}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Could not update board member ${id}:`, error);
        throw error;
    }
}

async function updateCoach(id, data) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/coaches/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, body: ${errorBody}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Could not update coach ${id}:`, error);
        throw error;
    }
}

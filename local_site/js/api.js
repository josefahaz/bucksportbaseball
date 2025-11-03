const API_BASE_URL = '/api';

async function fetchInventory() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventory`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching inventory:', error);
        return [];
    }
}

async function fetchInventorySummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventory/summary`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching inventory summary:', error);
        return null;
    }
}

async function fetchCoaches() {
    try {
        const response = await fetch(`${API_BASE_URL}/coaches`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching coaches:', error);
        return [];
    }
}

async function fetchBoardMembers() {
    try {
        const response = await fetch(`${API_BASE_URL}/board-members`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching board members:', error);
        return [];
    }
}

async function fetchTeams() {
    try {
        const response = await fetch(`${API_BASE_URL}/teams`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching teams:', error);
        return [];
    }
}

async function fetchCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventory/categories`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching categories:', error);
        return [];
    }
}

async function fetchStatuses() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventory/statuses`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching statuses:', error);
        return [];
    }
}

const fetchEvents = () => fetchData('/events');
const fetchConcessions = () => fetchData('/concessions');
const fetchEventUsage = (eventId) => fetchData(`/events/${eventId}/usage`);

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

const saveEventUsage = (eventId, usageData) => postData(`/events/${eventId}/usage`, usageData);
const syncEventInventory = (eventId) => postData(`/events/${eventId}/sync`, {});
const addConcessionItem = (itemData) => postData('/concessions', itemData);

const fetchSchedule = () => fetchData('/schedule');
const fetchLocations = () => fetchData('/locations');
const requestNewEvent = (eventData) => postData('/schedule/request', eventData);

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

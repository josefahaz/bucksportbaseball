const STORAGE_KEYS = {
    inventory: 'bl_admin_inventory',
    teams: 'bl_admin_teams',
    coaches: 'bl_admin_coaches',
    schedule: 'bl_admin_schedule',
    locations: 'bl_admin_locations',
    categories: 'bl_admin_categories',
    statuses: 'bl_admin_statuses',
    concessions: 'bl_admin_concessions',
    eventUsage: 'bl_admin_event_usage',
    eventRequests: 'bl_admin_event_requests',
};

const LS = {
    get(key, fallback) {
        try {
            const v = localStorage.getItem(key);
            return v ? JSON.parse(v) : fallback;
        } catch (_) {
            return fallback;
        }
    },
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (_) {}
    },
};

(function seedIfEmpty() {
    if (!LS.get(STORAGE_KEYS.teams)) {
        LS.set(STORAGE_KEYS.teams, [
            { id: 1, name: 'Bucksport Blue Jays' },
            { id: 2, name: 'Softball Stars' },
            { id: 3, name: 'Minor League All-Stars' },
        ]);
    }
    if (!LS.get(STORAGE_KEYS.coaches)) {
        LS.set(STORAGE_KEYS.coaches, [
            { id: 1, name: 'Coach Bob' },
            { id: 2, name: 'Coach Sarah' },
            { id: 3, name: 'Coach Mike' },
        ]);
    }
    if (!LS.get(STORAGE_KEYS.schedule)) {
        LS.set(STORAGE_KEYS.schedule, [
            { id: 1, date: '2025-07-20', time: '18:00', type: 'game', title: 'Bucksport Blue Jays vs. Orland Orcas', location: 'Field A', team_id: 1, coach_id: 1, notes: 'Championship game!' },
            { id: 2, date: '2025-07-21', time: '17:30', type: 'practice', title: 'Softball Team Practice', location: 'Field B', team_id: 2, coach_id: 2, notes: 'Focus on fielding drills.' },
            { id: 3, date: '2025-07-20', time: '16:00', type: 'game', title: 'Minor League All-Stars', location: 'Field C', team_id: 3, coach_id: 3, notes: '' },
        ]);
    }
    if (!LS.get(STORAGE_KEYS.locations)) {
        LS.set(STORAGE_KEYS.locations, ['Field A', 'Field B', 'Field C', 'Community Park']);
    }
    if (!LS.get(STORAGE_KEYS.categories)) {
        LS.set(STORAGE_KEYS.categories, ['jersey', 'pants', 'hat', 'cleats', 'bat', 'ball', 'glove', 'helmet', 'other']);
    }
    if (!LS.get(STORAGE_KEYS.statuses)) {
        LS.set(STORAGE_KEYS.statuses, ['in-stock', 'low-stock', 'out-of-stock', 'needs-repair', 'retired']);
    }
    if (!LS.get(STORAGE_KEYS.inventory)) {
        LS.set(STORAGE_KEYS.inventory, []);
    }
    if (!LS.get(STORAGE_KEYS.concessions)) {
        LS.set(STORAGE_KEYS.concessions, []);
    }
    if (!LS.get(STORAGE_KEYS.eventUsage)) {
        LS.set(STORAGE_KEYS.eventUsage, {});
    }
    if (!LS.get(STORAGE_KEYS.eventRequests)) {
        LS.set(STORAGE_KEYS.eventRequests, []);
    }
})();

async function fetchInventory() {
    return LS.get(STORAGE_KEYS.inventory, []);
}

async function fetchInventorySummary() {
    const items = LS.get(STORAGE_KEYS.inventory, []);
    const summary = {
        total_items: items.reduce((a, i) => a + (Number(i.quantity) || 0), 0),
        available: items.filter(i => i.status === 'in-stock').reduce((a, i) => a + (Number(i.quantity) || 0), 0),
        checked_out: items.filter(i => i.status === 'checked-out').reduce((a, i) => a + (Number(i.quantity) || 0), 0),
        needs_repair: items.filter(i => i.status === 'needs-repair').reduce((a, i) => a + (Number(i.quantity) || 0), 0),
    };
    return summary;
}

async function fetchCoaches() {
    return LS.get(STORAGE_KEYS.coaches, []);
}

async function fetchTeams() {
    return LS.get(STORAGE_KEYS.teams, []);
}

async function fetchCategories() {
    const cats = LS.get(STORAGE_KEYS.categories, []);
    if (cats && cats.length) return cats;
    const items = LS.get(STORAGE_KEYS.inventory, []);
    return Array.from(new Set(items.map(i => i.category).filter(Boolean)));
}

async function fetchStatuses() {
    return LS.get(STORAGE_KEYS.statuses, []);
}

const fetchEvents = () => fetchData('/events');
const fetchConcessions = () => fetchData('/concessions');
const fetchEventUsage = (eventId) => fetchData(`/events/${eventId}/usage`);

async function postData(endpoint, data) {
    try {
        if (endpoint === '/concessions') {
            const list = LS.get(STORAGE_KEYS.concessions, []);
            const nextId = list.length ? Math.max(...list.map(i => i.id || 0)) + 1 : 1;
            const item = { id: nextId, ...data };
            list.push(item);
            LS.set(STORAGE_KEYS.concessions, list);
            return item;
        }
        if (endpoint.startsWith('/events/') && endpoint.endsWith('/usage')) {
            const id = endpoint.split('/')[2];
            const usage = LS.get(STORAGE_KEYS.eventUsage, {});
            usage[id] = data;
            LS.set(STORAGE_KEYS.eventUsage, usage);
            return { status: 'success' };
        }
        if (endpoint === '/schedule/request') {
            const reqs = LS.get(STORAGE_KEYS.eventRequests, []);
            reqs.push({ id: reqs.length + 1, ...data, created_at: new Date().toISOString() });
            LS.set(STORAGE_KEYS.eventRequests, reqs);
            return { status: 'success', message: 'Event request stored locally.' };
        }
        return { status: 'ok' };
    } catch (error) {
        console.error(`Local post failed for ${endpoint}:`, error);
        throw error;
    }
}

const saveEventUsage = (eventId, usageData) => postData(`/events/${eventId}/usage`, usageData);
const syncEventInventory = async (eventId) => ({ status: 'ok' });
const addConcessionItem = (itemData) => postData('/concessions', itemData);

const fetchSchedule = () => fetchData('/schedule');
const fetchLocations = () => fetchData('/locations');
const requestNewEvent = (eventData) => postData('/schedule/request', eventData);

async function fetchData(endpoint) {
    try {
        if (endpoint === '/schedule' || endpoint === '/events') {
            return LS.get(STORAGE_KEYS.schedule, []);
        }
        if (endpoint === '/locations') {
            return LS.get(STORAGE_KEYS.locations, []);
        }
        if (endpoint === '/concessions') {
            return LS.get(STORAGE_KEYS.concessions, []);
        }
        if (endpoint.startsWith('/events/') && endpoint.endsWith('/usage')) {
            const id = endpoint.split('/')[2];
            const usage = LS.get(STORAGE_KEYS.eventUsage, {});
            return usage[id] || [];
        }
        return [];
    } catch (error) {
        console.error(`Local fetch failed for ${endpoint}:`, error);
        return [];
    }
}

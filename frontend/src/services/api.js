const BASE_URL = "/api";

export const api = {
  async createRequest(data) {
    const res = await fetch(`${BASE_URL}/requests/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getRequest(code) {
    const res = await fetch(`${BASE_URL}/requests/${code}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async listRequests(params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${BASE_URL}/requests/?${query}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async updateRequestStatus(code, status, resourceInfo = "") {
    const res = await fetch(`${BASE_URL}/requests/${code}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, resource_info: resourceInfo }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getMapResources(params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${BASE_URL}/resources/map?${query}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getBloodBanks() {
    const res = await fetch(`${BASE_URL}/resources/blood-banks`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getHospitals() {
    const res = await fetch(`${BASE_URL}/resources/hospitals`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getAmbulances() {
    const res = await fetch(`${BASE_URL}/resources/ambulances`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getPharmacies() {
    const res = await fetch(`${BASE_URL}/resources/pharmacies`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async registerVolunteer(data) {
    const res = await fetch(`${BASE_URL}/volunteers/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getVolunteers() {
    const res = await fetch(`${BASE_URL}/volunteers/all`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async toggleVolunteerAvailability(id, isAvailable) {
    const res = await fetch(`${BASE_URL}/volunteers/${id}/availability?is_available=${isAvailable}`, {
      method: "PATCH",
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async volunteerRespond(id, requestCode, action) {
    const res = await fetch(`${BASE_URL}/volunteers/${id}/respond?request_code=${requestCode}&action=${action}`, {
      method: "POST",
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getHospitalDashboard() {
    const res = await fetch(`${BASE_URL}/hospital/dashboard`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async updateInventory(bankId, group, component, delta) {
    const res = await fetch(`${BASE_URL}/hospital/inventory/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        blood_bank_id: bankId,
        blood_group: group,
        component: component,
        units_delta: delta,
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};

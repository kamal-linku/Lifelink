export class EmergencySocket {
  constructor(category = "requesters", clientId = "client_" + Math.random().toString(36).substring(2, 8)) {
    this.category = category;
    this.clientId = clientId;
    this.listeners = [];
    this.ws = null;
    this.reconnectTimer = null;
    this.init();
  }

  init() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.host;
    // Connect directly or via proxy
    const url = `${protocol}//${host}/ws/${this.category}/${this.clientId}`;

    try {
      this.ws = new WebSocket(url);

      this.ws.onopen = () => {
        console.log("[WebSocket] Connected to LifeLink Emergency Hub");
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.listeners.forEach((callback) => callback(data));
        } catch (e) {
          console.error("WS Parse error", e);
        }
      };

      this.ws.onclose = () => {
        console.log("[WebSocket] Closed. Attempting reconnect in 3s...");
        clearTimeout(this.reconnectTimer);
        this.reconnectTimer = setTimeout(() => this.init(), 3000);
      };

      this.ws.onerror = (err) => {
        console.warn("[WebSocket] Connection error", err);
      };
    } catch (e) {
      console.error("[WebSocket] Exception opening socket", e);
    }
  }

  subscribe(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter((cb) => cb !== callback);
    };
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(typeof data === "string" ? data : JSON.stringify(data));
    }
  }

  close() {
    clearTimeout(this.reconnectTimer);
    if (this.ws) {
      this.ws.close();
    }
  }
}

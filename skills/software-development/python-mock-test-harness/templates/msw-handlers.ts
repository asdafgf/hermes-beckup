/**
 * MSW (Mock Service Worker) Handler Şablonu
 * 
 * React Native/Jest testlerinde Python backend API'sini taklit etmek için.
 * 
 * Kullanım:
 *   1. Bu dosyayı tests/ui/mocks/handlers.ts olarak kopyala
 *   2. API endpoint'lerini kendi projene göre düzenle
 *   3. Test dosyasında server.listen/resetHandlers/close kullan
 * 
 * Test şablonu:
 *   beforeAll(() => server.listen());
 *   afterEach(() => server.resetHandlers());
 *   afterAll(() => server.close());
 */

import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Python backend API base URL — .env'den alınabilir
const API_BASE = 'http://localhost:8000/api';

/**
 * Handler tanımları:
 * Her endpoint için bir rest.get/post/put/delete handler'ı.
 * Handler'lar sırayla denenir, ilk eşleşen kullanılır.
 * server.use() ile test içinde override edilebilir.
 */
export const handlers = [
  // ── BIST Verileri ──────────────────────────────
  rest.get(`${API_BASE}/bist/latest`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        status: 'ok',
        data: {
          XU100: { price: 9850.45, change_pct: 1.23 },
          XU030: { price: 11230.20, change_pct: 0.87 },
          'X Banks': { price: 17250.00, change_pct: 2.10 },
        },
        timestamp: new Date().toISOString(),
      }),
    );
  }),

  // ── XAUUSD Verileri ────────────────────────────
  rest.get(`${API_BASE}/xauusd/latest`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        status: 'ok',
        data: {
          price: 2345.60,
          high: 2360.15,
          low: 2338.40,
          change_pct: -0.32,
        },
        timestamp: new Date().toISOString(),
      }),
    );
  }),

  // ── OSINT DNS ──────────────────────────────────
  rest.get(`${API_BASE}/osint/dns`, (req, res, ctx) => {
    const domain = req.url.searchParams.get('domain') || 'example.com';
    return res(
      ctx.status(200),
      ctx.json({
        domain,
        records: [
          { type: 'A', value: '93.184.216.34', ttl: 3600 },
          { type: 'AAAA', value: '2606:2800:220:1:248:1893:25c8:1946', ttl: 3600 },
        ],
        queried_at: new Date().toISOString(),
      }),
    );
  }),

  // ── OSINT Port Tarama ──────────────────────────
  rest.get(`${API_BASE}/osint/ports`, (req, res, ctx) => {
    const target = req.url.searchParams.get('target') || 'example.com';
    return res(
      ctx.status(200),
      ctx.json({
        target,
        open_ports: [
          { port: 80, service: 'http', state: 'open' },
          { port: 443, service: 'https', state: 'open' },
        ],
        scan_time: '2.34s',
      }),
    );
  }),

  // ── Hata Senaryosu ─────────────────────────────
  rest.get(`${API_BASE}/error`, (req, res, ctx) => {
    return res(
      ctx.status(503),
      ctx.json({ error: 'Service Unavailable', code: 'UPSTREAM_TIMEOUT' }),
    );
  }),
];

/**
 * MSW Server instance — test lifecyle'ında kullanılır.
 * 
 * Dışa aktar: import { server } from './mocks/handlers';
 */
export const server = setupServer(...handlers);

/**
 * Tip tanımları (opsiyonel — TypeScript kullanıyorsanız):
 */
export interface BistResponse {
  status: string;
  data: {
    XU100: { price: number; change_pct: number };
    XU030: { price: number; change_pct: number };
    'X Banks': { price: number; change_pct: number };
  };
  timestamp: string;
}

export interface XauusdResponse {
  status: string;
  data: {
    price: number;
    high: number;
    low: number;
    change_pct: number;
  };
  timestamp: string;
}

export interface DnsResponse {
  domain: string;
  records: Array<{ type: string; value: string; ttl: number }>;
  queried_at: string;
}

export interface PortResponse {
  target: string;
  open_ports: Array<{ port: number; service: string; state: string }>;
  scan_time: string;
}

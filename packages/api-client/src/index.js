// Central API client shared by web + mobile. Single place for base URL, auth token injection,
// error normalization, and Zod response validation. No duplicated fetch logic elsewhere.

import { apiErrorSchema } from './schemas.js';

export class ApiError extends Error {
  constructor(code, message, status, details) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

/**
 * Create an API client.
 * @param {object} opts
 * @param {string} opts.baseUrl                e.g. http://localhost:8000/api/v1
 * @param {() => Promise<string|null>} [opts.getToken]  returns a fresh Firebase ID token or null
 */
export function createApiClient({ baseUrl, getToken }) {
  if (!baseUrl) throw new Error('createApiClient: baseUrl is required');

  async function request(path, { method = 'GET', body, schema, auth = false, signal } = {}) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth && getToken) {
      const token = await getToken();
      if (token) headers.Authorization = `Bearer ${token}`;
    }

    let res;
    try {
      res = await fetch(`${baseUrl}${path}`, {
        method,
        headers,
        body: body != null ? JSON.stringify(body) : undefined,
        signal,
      });
    } catch (networkErr) {
      throw new ApiError('network_error', networkErr.message, 0);
    }

    const text = await res.text();
    const json = text ? safeJson(text) : null;

    if (!res.ok) {
      const parsed = apiErrorSchema.safeParse(json);
      if (parsed.success) {
        const { code, message, details } = parsed.data.error;
        throw new ApiError(code, message, res.status, details);
      }
      throw new ApiError('http_error', `Request failed (${res.status})`, res.status, json);
    }

    if (schema) {
      const parsed = schema.safeParse(json);
      if (!parsed.success) {
        throw new ApiError(
          'invalid_response',
          'Response did not match expected schema',
          res.status,
          parsed.error.issues
        );
      }
      return parsed.data;
    }
    return json;
  }

  return {
    request,
    get: (path, opts) => request(path, { ...opts, method: 'GET' }),
    post: (path, body, opts) => request(path, { ...opts, method: 'POST', body }),
    patch: (path, body, opts) => request(path, { ...opts, method: 'PATCH', body }),
    put: (path, body, opts) => request(path, { ...opts, method: 'PUT', body }),
    del: (path, opts) => request(path, { ...opts, method: 'DELETE' }),
  };
}

function safeJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

export * from './schemas.js';

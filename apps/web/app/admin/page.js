'use client';

import { useState } from 'react';

import { useAuth } from '../../providers/AuthProvider';
import {
  useAuditLogs,
  useCatalog,
  useChangeVisibility,
  useCreateContent,
  useCreateGenre,
  useGenres,
} from '../../features/admin/hooks';

const VIS_ACTIONS = {
  draft: [
    ['publish', 'Publish'],
    ['archive', 'Archive'],
  ],
  published: [
    ['unpublish', 'Unpublish'],
    ['archive', 'Archive'],
  ],
  archived: [['publish', 'Publish']],
};

export default function AdminDashboard() {
  const { user, role, signOut } = useAuth();
  const catalog = useCatalog();
  const genres = useGenres();
  const [showAudit, setShowAudit] = useState(false);
  const audit = useAuditLogs(showAudit && role === 'admin');

  const createContent = useCreateContent();
  const changeVis = useChangeVisibility();
  const createGenre = useCreateGenre();

  const [title, setTitle] = useState('');
  const [type, setType] = useState('movie');
  const [genreCsv, setGenreCsv] = useState('');
  const [newGenre, setNewGenre] = useState('');

  function submitContent(e) {
    e.preventDefault();
    if (!title.trim()) return;
    const list = genreCsv
      .split(',')
      .map((g) => g.trim())
      .filter(Boolean);
    createContent.mutate(
      { type, title: title.trim(), genres: list },
      { onSuccess: () => setTitle('') }
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-6 py-6">
      <header className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Catalog Admin</h1>
        <div className="flex items-center gap-3 text-sm text-muted">
          <span>
            {user.email} · {role}
          </span>
          <button onClick={signOut} className="rounded bg-surfaceAlt px-3 py-1">
            Sign out
          </button>
        </div>
      </header>

      {/* Create content */}
      <section className="mb-8 rounded bg-surface p-4">
        <h2 className="mb-3 font-semibold">Add title</h2>
        <form onSubmit={submitContent} className="flex flex-wrap items-center gap-2">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Title"
            className="flex-1 rounded bg-bg px-3 py-2 ring-1 ring-border"
          />
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="rounded bg-bg px-3 py-2 ring-1 ring-border"
          >
            <option value="movie">Movie</option>
            <option value="series">Series</option>
          </select>
          <input
            value={genreCsv}
            onChange={(e) => setGenreCsv(e.target.value)}
            placeholder="genres, comma-separated"
            className="rounded bg-bg px-3 py-2 ring-1 ring-border"
          />
          <button
            type="submit"
            disabled={createContent.isPending}
            className="rounded bg-primary px-4 py-2 font-semibold disabled:opacity-60"
          >
            Create draft
          </button>
        </form>
        {createContent.isError && (
          <p className="mt-2 text-sm text-danger">{createContent.error.message}</p>
        )}
      </section>

      {/* Catalog table */}
      <section className="mb-8">
        <h2 className="mb-3 font-semibold">Catalog</h2>
        {catalog.isLoading && <p className="text-muted">Loading…</p>}
        {catalog.isError && <p className="text-danger">{catalog.error.message}</p>}
        {catalog.data && catalog.data.items.length === 0 && (
          <p className="text-muted">No content yet. Add one above.</p>
        )}
        {catalog.data && catalog.data.items.length > 0 && (
          <div className="overflow-x-auto rounded ring-1 ring-border">
            <table className="w-full text-left text-sm">
              <thead className="bg-surface text-muted">
                <tr>
                  <th className="p-2">Title</th>
                  <th className="p-2">Type</th>
                  <th className="p-2">Status</th>
                  <th className="p-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {catalog.data.items.map((c) => (
                  <tr key={c.id} className="border-t border-border">
                    <td className="p-2">{c.title}</td>
                    <td className="p-2 text-muted">{c.type}</td>
                    <td className="p-2">
                      <span className="rounded bg-surfaceAlt px-2 py-0.5 text-xs">
                        {c.visibility}
                      </span>
                    </td>
                    <td className="p-2">
                      <div className="flex gap-2">
                        {(VIS_ACTIONS[c.visibility] || []).map(([action, label]) => (
                          <button
                            key={action}
                            onClick={() => changeVis.mutate({ id: c.id, action })}
                            disabled={changeVis.isPending}
                            className="rounded bg-surfaceAlt px-2 py-1 text-xs hover:bg-border"
                          >
                            {label}
                          </button>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Genres */}
      <section className="mb-8 rounded bg-surface p-4">
        <h2 className="mb-3 font-semibold">Genres</h2>
        <div className="mb-3 flex flex-wrap gap-2">
          {(genres.data?.items || []).map((g) => (
            <span key={g.id} className="rounded bg-surfaceAlt px-2 py-1 text-xs">
              {g.name}
            </span>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            value={newGenre}
            onChange={(e) => setNewGenre(e.target.value)}
            placeholder="New genre"
            className="rounded bg-bg px-3 py-2 ring-1 ring-border"
          />
          <button
            onClick={() =>
              newGenre.trim() &&
              createGenre.mutate(newGenre.trim(), { onSuccess: () => setNewGenre('') })
            }
            className="rounded bg-surfaceAlt px-4 py-2"
          >
            Add
          </button>
        </div>
      </section>

      {/* Audit log (admin only) */}
      {role === 'admin' && (
        <section className="rounded bg-surface p-4">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="font-semibold">Audit log</h2>
            <button
              onClick={() => setShowAudit((s) => !s)}
              className="rounded bg-surfaceAlt px-3 py-1 text-sm"
            >
              {showAudit ? 'Hide' : 'Show'}
            </button>
          </div>
          {showAudit && audit.isLoading && <p className="text-muted">Loading…</p>}
          {showAudit && audit.data && (
            <ul className="space-y-1 text-sm text-muted">
              {audit.data.items.map((a) => (
                <li key={a.id}>
                  <span className="text-text">{a.action}</span> · {a.entityType} · {a.entityId} ·{' '}
                  {a.actorUid}
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  );
}

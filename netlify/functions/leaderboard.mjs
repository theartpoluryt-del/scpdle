import { getStore } from "@netlify/blobs";

const headers = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store"
};

export default async (request) => {
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }

  try {
    const url = new URL(request.url);
    const store = getStore("scpdle-leaderboard");

    if (request.method === "GET") {
      const date = normalizeDate(url.searchParams.get("date"));
      if (!date) return json({ error: "Bad date" }, 400);
      const entries = await readEntries(store, date);
      return json({ date, entries: rankEntries(entries) });
    }

    if (request.method === "POST") {
      const body = await request.json();
      const entry = normalizeEntry(body);
      if (!entry) return json({ error: "Bad score" }, 400);

      const entries = await readEntries(store, entry.date);
      const existingIndex = entries.findIndex((item) => item.playerId === entry.playerId);

      if (existingIndex === -1) {
        entries.push(entry);
      } else if (isBetterEntry(entry, entries[existingIndex])) {
        entries[existingIndex] = entry;
      } else {
        entries[existingIndex].playerName = entry.playerName;
      }

      const ranked = rankEntries(entries).slice(0, 100);
      await store.setJSON(entry.date, ranked);
      return json({ date: entry.date, entries: ranked });
    }

    if (request.method === "DELETE") {
      const body = await request.json();
      const date = normalizeDate(body?.date);
      const playerId = String(body?.playerId ?? "").slice(0, 80);
      if (!date || !playerId) return json({ error: "Bad delete" }, 400);

      const entries = await readEntries(store, date);
      const ranked = rankEntries(entries.filter((item) => item.playerId !== playerId)).slice(0, 100);
      await store.setJSON(date, ranked);
      return json({ date, entries: ranked });
    }

    return json({ error: "Method not allowed" }, 405);
  } catch {
    return json({ error: "Leaderboard error" }, 500);
  }
};

async function readEntries(store, date) {
  return (await store.get(date, { type: "json" })) ?? [];
}

function rankEntries(entries) {
  return [...entries].sort((a, b) => {
    if (b.streak !== a.streak) return b.streak - a.streak;
    if (a.totalMistakes !== b.totalMistakes) return a.totalMistakes - b.totalMistakes;
    return String(a.solvedAt).localeCompare(String(b.solvedAt));
  });
}

function isBetterEntry(next, current) {
  return rankEntries([next, current])[0] === next;
}

function normalizeDate(date) {
  return /^\d{4}-\d{2}-\d{2}$/.test(String(date)) ? String(date) : null;
}

function normalizeEntry(body) {
  const date = normalizeDate(body?.date);
  const playerId = String(body?.playerId ?? "").slice(0, 80);
  const playerName = String(body?.playerName ?? "Игрок").trim().replace(/\s+/g, " ").slice(0, 18) || "Игрок";
  const streak = clampNumber(body?.streak, 0, 10000);
  const totalMistakes = clampNumber(body?.totalMistakes, 0, 999);
  const solvedAt = Number.isNaN(Date.parse(body?.solvedAt)) ? new Date().toISOString() : new Date(body.solvedAt).toISOString();
  const levels = Array.isArray(body?.levels) ? body.levels.slice(0, 5) : [];

  if (!date || !playerId || levels.length !== 5) return null;

  return {
    date,
    playerId,
    playerName,
    streak,
    totalMistakes,
    solvedAt,
    levels: levels.map((level) => ({
      mode: String(level?.mode ?? "").slice(0, 32),
      scp: String(level?.scp ?? "").slice(0, 16),
      mistakes: clampNumber(level?.mistakes, 0, 99)
    }))
  };
}

function clampNumber(value, min, max) {
  const number = Number(value);
  if (!Number.isFinite(number)) return min;
  return Math.max(min, Math.min(max, Math.round(number)));
}

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers });
}

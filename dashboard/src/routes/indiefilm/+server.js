import { json } from '@sveltejs/kit';
import { addEvent } from '$lib/datastore.js';

export async function POST({ request, cookies }) {
  const { description } = await request.json();
  addEvent("indiefilm");
  return json({ status: 200 });
}

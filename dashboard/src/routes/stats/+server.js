import { json } from '@sveltejs/kit';
import { calculateRates } from "$lib/datastore";

export function GET() {
  return json(calculateRates());
}

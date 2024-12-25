const url = `http://${import.meta.env.VITE_ROTTENEGGS_HOST}:${import.meta.env.VITE_ROTTENEGGS_PORT}`

export async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export async function getMovieIds() {
  const response = await fetch(`${url}/movies`);
  const movieIds = await response.json();
  return movieIds.ids;
}

export async function generateReview(movieId) {
  const stars = Math.floor(Math.random() * 10);
  const response = await fetch(`${url}/ratings`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({movie_id: movieId, stars: stars, review: "some review"})
  });
  const res = await response.json();
}

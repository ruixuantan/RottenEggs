<script>
  import { onMount } from "svelte";
  import { getMovieIds, generateReview, sleep } from "$lib/utils";

  let generating = $state(false);
  let rate = $state(1);
  let movieIds = [];

  onMount(async () => { movieIds = await getMovieIds(); });

  export async function generateReviews() {
    generating = true;
    const sleepTime = 1 / rate;
    while (generating) {
      const movieId = movieIds[Math.floor(Math.random() * movieIds.length)];
      generateReview(movieId);
      await sleep(sleepTime * 1000);
    }
  }

  export function stopGeneration() {
    generating = false;
  }
</script>

<div class="rotteneggs">
  <h1 class="text-primary">RottenEggs</h1>

  <div class="rotteneggs-content">
    <div class="review-generation">
      <input type="text" bind:value={rate} placeholder="Generation Rate/s" class="input input-bordered w-full max-w-xs" />
      {#if generating}
        <button class="btn btn-active btn-secondary" onclick={stopGeneration}>Stop</button>
      {:else}
        <button class="btn btn-primary" onclick={generateReviews}>Generate Reviews</button>
      {/if}
    </div>

    <div class="rate-monitor">
      <div class="card bg-base-100 w-96 shadow-xl">
        <div class="card-body">
          <h3 class="card-title">Documentary Analytics: 1.0/s</h3>
        </div>
      </div>

      <div class="card bg-base-100 w-96 shadow-xl">
        <div class="card-body">
          <h3 class="card-title">Indiefilm Recommender: 1.0/s</h3>
        </div>
      </div>

      <div class="card bg-base-100 w-96 shadow-xl">
        <div class="card-body">
          <h3 class="card-title">Consume All: 1.0/s</h3>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .rotteneggs {
    margin: auto;
    width: 80%;
    height: 30em;
  }

  .rotteneggs {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: auto;
  }

  .rotteneggs-content {
    margin: auto;
    width: 60%;
    height: 10em;
    padding: auto;
  }

  .rotteneggs-content {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin: auto;
    gap: 30px;
  }

  .review-generation {
    margin: auto;
    padding: auto;
  }

  .review-generation {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    margin: auto;
    gap: 10px;
  }

  .rate-monitor {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  h1 {
    font-size: 3rem;
    font-weight: 1000;
  }
</style>

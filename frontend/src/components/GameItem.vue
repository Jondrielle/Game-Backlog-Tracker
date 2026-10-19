<script setup>

const props = defineProps({
	game: Object
})

const emit = defineEmits(['delete','edit'])

function deleteGame(){
	emit('delete',props.game.id)
}

function editGame(){
	emit('edit',props.game)
}
</script>

<template>
<div class="container">
	<img
		v-if="game.cover_url"
		:src="game.cover_url"
		:alt="`${game.name} cover`"
		class="game-cover"
	/>
	<div class="title-row">
		<h3>{{game.name}}</h3>
		<span class="status-badge">{{game.status}}</span>
		{{ game.genres?.join(", ") || "None" }}
		<span>
			<button @click="deleteGame">X</button>
			<button @click="editGame">Edit</button>
		</span>
	</div>
</div>
</template>


<style scoped>
.container {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 12px;
  margin-bottom: 12px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  background-color: #ffffff;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.container:hover {
  border-color: #72ff72;
  box-shadow: 0 3px 10px rgba(0, 184, 0, 0.1);
}

/* Game cover */
.game-cover {
  display: block;
  flex-shrink: 0;
  width: 100px;
  aspect-ratio: 3 / 4;
  object-fit: cover;
  border-radius: 8px;
  }

/* Game details */
.stats {
  flex: 1;
  min-width: 0;
}

/* Game title and status */
.title-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.stats h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #222222;
  overflow-wrap: anywhere;
}

/* Small status badge */
.status-badge {
  display: inline-block;
  padding: 3px 8px;
  font-size: 0.7rem;
  font-weight: 600;
  line-height: 1.4;
  color: #167a16;
  background-color: #d9ffd9;
  border: 1px solid #a3e6a3;
  border-radius: 999px;
  white-space: nowrap;
}

/* Genres and other game details */
.stats p {
  margin: 6px 0;
  padding: 6px 9px;
  overflow-wrap: anywhere;
  color: #333333;
  background-color: #f5fff5;
  border: 1px solid #d9ffd9;
  border-radius: 8px;
  font-size: 0.85rem;
}

/* Action buttons */
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.actions button:first-child {
  color: #ffffff;
  background-color: #dc3545;
}

.actions button:first-child:hover {
  background-color: #b02a37;
}

.actions button:last-child {
  color: #166b16;
  background-color: #d9ffd9;
  border: 1px solid #a3e6a3;
}

.actions button:last-child:hover {
  background-color: #b8f5b8;
}

/* Mobile layout */
@media (max-width: 600px) {
  .container {
    gap: 10px;
    padding: 9px;
  }

  .game-cover {
    width: 80px;
  }

  .stats h3 {
    font-size: 1rem;
  }

  .status-badge {
    font-size: 0.65rem;
    padding: 2px 7px;
  }

  .stats p {
    font-size: 0.8rem;
  }
}
</style>

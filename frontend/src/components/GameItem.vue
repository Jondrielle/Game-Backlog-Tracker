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
	<div class="stats">
		<label>{{game.name}}</label>
		Status:{{game.status}}
		Genres: {{ game.genres?.join(", ") || "None" }}
		Rating:{{game.rating}}
		Platform:{{game.platform}}
		Notes:{{game.notes}}
		Release Date:{{game.release_date}}
		Game Completion:{{game.date_completed}}

		<span>
			<button @click="deleteGame">X</button>
			<button @click="editGame">Edit</button>
		</span>
	</div>
</div>
</template>

<style scoped>
	.container{
		display:flex;
		padding-bottom:10px;
		border: 2px solid gray;
		border-radius:10px;
		height: 20vh;
		justify-content: center; 
  		align-items: center; 
	}

	.stats{
		
	}
</style>
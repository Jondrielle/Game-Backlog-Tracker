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
<h1>{{game.name}}</h1>
<div>
	Status:{{game.status}}
	Genre:{{game.genre}}
	Rating:{{game.rating}}
	Platform:{{game.platform}}
	Notes:{{game.notes}}
	Release Date:{{game.release_date}}
	Game Completion:{{game.date_completed}}
	-------------------

	<button @click="deleteGame">Delete</button>
	<button @click="editGame">Edit</button>
</div>
</template>
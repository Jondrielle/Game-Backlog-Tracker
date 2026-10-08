<script setup>

const props = defineProps({
	isEditing:Boolean,
	game:Object
})

const emit = defineEmits(["submit","cancel"])

function cancel(){
	emit('cancel')
}

function submit(){
	emit('submit',props.game)
}

</script>

<template>
	<h2>Form</h2>

	<form @submit.prevent="submit" class="form">
		<label for="name">Game Title</label>
			<input
				v-model="game.name"
				placeholder="Game Title"
				type="text"
			/>

		<div class="form-row">
			<div class="form-group">
				<label for="status">Status</label>
				<select 
				id="status"
				v-model="game.status">
					<option disabled value="">Select status</option>
					<option value="Backlog">Backlog</option>
					<option value="Playing">Playing</option>
					<option value="Completed">Completed</option>
					<option value="Dropped">Dropped</option>
				</select>
			</div>

			<div class="form-group">
				<label for="platform">Platform</label>
				<select 
				id="platform"
				v-model="game.platform">
					<option disabled value="">Select Platform</option>
					<option value="PC">PC</option>
					<option value="PlayStation">PlayStation</option>
					<option value="Xbox">Xbox</option>
					<option value="Switch">Switch</option>
				</select>
			</div>

			<div class="form-group">
				<label for="genre">Genres</label>
				<select 
				id="genre"
				v-model="game.genres"
				multiple>
					<option value="Action">Action</option>
					<option value="Adventure">Adventure</option>
					<option value="RPG">RPG</option>
					<option value="Strategy">Strategy</option>
					<option value="Simulation">Simulation</option>
					<option value="Sports">Sports</option>
					<option value="Racing">Racing</option>
					<option value="Puzzle">Puzzle</option>
					<option value="Horror">Horror</option>
					<option value="Platformer">Platformer</option>
					<option value="Shooter">Shooter</option>
					<option value="Fighting">Fighting</option>
				</select>
			</div>

		</div>

		<label for="rating"> Rating</label>
		<input
			v-model="game.rating"
			placeholder="Rating"
			type="number"
			min="1"
			max="5"
		>

		<label for="notes">Notes</label>
		<textarea 
			v-model="game.notes"
			type="text"
			placeholder="Notes">
		</textarea>

		<label for="releaseDate">Release Date</label>
		<input
			v-model="game.release_date"
			type="date"
		>

		<label for="completeDate">Complete Date</label>
		<input
			v-model="game.date_completed"
			type="date"
		>

		<button type="submit"> {{isEditing ? "Save Edit" : "Add"}}</button>

		<button type="button" @click="cancel">Cancel</button>

	</form>
</template>

<style scoped>

	.form{
		display:flex;
		flex-direction:column;
		gap:15px;
	}

	.form-row {
	  display: flex;
	  gap: 10px;
	}

	.form-group {
	  display: flex;
	  flex-direction: column;
	  gap: 0.4rem;
	  flex: 1;
	}
</style>
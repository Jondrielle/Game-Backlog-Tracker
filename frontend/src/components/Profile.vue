<script setup>
const emit = defineEmits(["signout","delete"])

function signOut(){
	emit("signout")
}

function deleteAccount(){
	emit("delete")
}
</script>

<template>
	<div class="profile">
		<div class="picture">
		</div>
		<div class="account">
			<button @click="signOut">Sign Out</button>
			<button>Edit Profile</button>
			<button @click="delete">Delete Account</button>
		</div>
	</div>
</template>

<style scoped>
	.profile{
		display:flex;
		flex-direction:column;
	}

	.picture{
		border:2px solid red;
		border-radius: 100px;
		padding:20px;
		width: 50px;
  		height: 50px;
	}

	.account{
		display:flex;
		gap:10px;
		
	}
</style>
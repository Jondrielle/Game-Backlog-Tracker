import {ref} from "vue"

<script setup>

const userEmail = ref("")
const userPassword = ref("")

const emit = DefineEmits({login,signup,reset})

function login(){
	emit("login")
}

function signUp(){
	emit("signup")	
}

function reset(){
	emit("reset")
}



</script>

<template>
	<div class="auth">
		<div class="login">
			<h3>Login</h3>

			Enter email:
		    <input
		      v-model="userEmail"
		      placeholder="Email"/>

		    Enter Password:
		    <input
		      v-model="password"
		      placeholder="Password"/>

		    <button @click="login">Login</button>

		    <button @click="resetPassword">Forgot Password</button>
		</div>

		<div class="signup">
			<h2>Create Account</h2>
		    Enter Email:
		    <input 
		      v-model="userEmail"
		      placeholder="Email"/>

		    Enter Password:
		    <input 
		      v-model="password"
		      placeholder="Password"/>

		    <button @click="signUp">Sign Up</button>
		</div>
	</div>
</template>

<style scoped>

	.auth{
		display:flex;
		gap:50px;
		width:max-screen-width;
		border:2px solid green;
	}

	.login{
  		border: 1px solid red;
		border-radius:5px;
		border-color:red;
		padding: 30px 40px 40px;
		width: max-screen-width/2;
	}

	.signup{
		border: 1px solid red;
		border-radius:5px;
		border-color:red;
		padding: 30px 40px 40px;
		width: max-screen-width/2;
	}

	.signup > input{
		display:flex;
		flex-direction:column;
		gap:45px;
	}

	.login > input{
		display:flex;
		flex-direction:column;
		gap:15px;
	}
</style>
<script setup>
import {ref} from "vue"


const email = ref("")
const password = ref("")

const props = defineProps({
	
})

const emit = defineEmits(["login","signup","reset"])

function login(){
	emit("login",email,password)
}

function signUp(){
	emit("signup",email,password)	
}

function reset(){
	emit("reset")
}



</script>

<template>
	<div class="auth">
		<div class="login">
			<h3>Login</h3>

		    <input
		      v-model="email"
		      placeholder="Enter your email"/>

		    <input
		      v-model="password"
		      placeholder="Enter your password"/>

		    <button @click="login">Login</button>

		    <button @click="reset">Forgot password?</button>
		    
		</div>

		<div class="signup">
			<h2>Create Account</h2>
		    <input 
		    	v-model="email"
		    	placeholder="Enter your email"/>

		    <input 
		    	type="password"
		    	v-model="password"
		    	placeholder="Create password"/>

		    <input
		    	type="password"
		    	v-model="password"
		    	placeholder="Confirm your password"
		    	hidden="true"/>

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
		display:flex;
		flex-direction:column;
  		border: 1px solid red;
		border-radius:5px;
		border-color:red;
		gap:10px;
	}

	.signup{
		display:flex;
		flex-direction:column;
		border: 1px solid red;
		border-radius:5px;
		border-color:red;
		gap:10px;
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
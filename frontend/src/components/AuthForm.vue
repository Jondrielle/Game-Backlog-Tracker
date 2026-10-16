<script setup>
import {ref} from "vue"


const loginEmail = ref("")
const loginPassword = ref("")

const signUpEmail = ref("")
const signUpPassword = ref("")
const signUpConfirmPassword = ref("")

const props = defineProps({
	
})

const emit = defineEmits(["login","signup","reset"])

function login(){
	emit("login",{
		email: loginEmail.value,
		password: loginPassword.value,})
}

function signUp(){
	if(signUpConfirmPassword.value !== signUpPassword.value){
		alert("Passwords do not match.")
		return
	}

	emit("signup",{
		email: signUpEmail.value,
		password: signUpPassword.value
	})
	
}

function reset(){
	emit("reset",loginEmail.value)
} 


</script>

<template>
	<div class="auth">
		<div class="login">
			<h3>Login</h3>

		    <input
		      v-model="loginEmail"
		      placeholder="Enter your email"/>

		    <input
		      v-model="loginPassword"
		      placeholder="Enter your password"/>

		    <button @click="login">Login</button>

		    <button @click="reset">Forgot password?</button>
		    
		</div>

		<div class="signup">
			<h2>Create Account</h2>
		    <input 
		    	v-model="signUpEmail"
		    	placeholder="Enter your email"/>

		    <input 
		    	type="password"
		    	v-model="signUpPassword"
		    	placeholder="Create password"/>

		    <input
		    	type="password"
		    	v-model="signUpConfirmPassword"
		    	placeholder="Confirm your password"
		    	/>

		    <button @click="signUp">Sign Up</button>
		</div>
	</div>
</template>

<style scoped>

	.auth{
		display:flex;
		gap:50px;
		width:max-screen-width;
		justify-content:center;
		align-items:center;
		height:80vh;
	}

	.login{
		display:flex;
		flex-direction:column;
		border-radius:5px;
		width: calc(100% / 2);
		height:calc(100% / 1);
		justify-content:center;
		align-items:center;
		gap:10px;
	}

	.signup{
		display:flex;
		flex-direction:column;
		border-radius:5px;
		width: calc(100% / 2);
		height:calc(100% / 1);
		justify-content:center;
		align-items:center;

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
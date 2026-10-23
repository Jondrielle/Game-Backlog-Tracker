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

	.auth {
	  display: flex;
	  gap: 50px;
	  justify-content: center;
	  align-items: center;
	  min-height: 100vh;
	  padding: 40px;
	  box-sizing: border-box;

	  background-image:
	    linear-gradient(
	      rgba(16, 19, 27, 0.65),
	      rgba(16, 19, 27, 0.85)
	    ),
	    url('/auth-background.jpg');

	  background-size: cover;
	  background-position: center;
	  background-repeat: no-repeat;
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

	.login,
	.signup {
	  background: #10131b;
	  color: #e8eaf2;
	  padding: 32px;
	  border-radius: 16px;
	  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
	}
</style>
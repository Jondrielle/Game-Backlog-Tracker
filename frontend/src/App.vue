<script setup>
import {ref} from 'vue'

const games = ref([])

async function getGames(){
  try{
    const response = await fetch("http://127.0.0.1:8000/")

    if(!response.ok){
      throw new Error(`Response status: ${response.status}`)
    }

    const result = await response.json()

    console.log(result)

    games.value = result
  }catch(err){
    console.error(err)
  }
}
</script>

<template>
  <h1>Game Backlog Tracker</h1>

  <button @click="getGames">Show List</button>
</template>

<style scoped></style>

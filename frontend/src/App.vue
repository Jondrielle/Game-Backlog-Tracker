<script setup>
import {ref} from 'vue'
import GameItem from "./components/GameItem.vue"

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

async function getGame(id){
  try{
    const response = await fetch(`http://127.0.0.1:8000/game/${id}`)

    if(!response.ok){
      throw new Error(`Response Error:${response.status}`)
    }

    result = await response.json()

    console.log(result)
  }catch(err){
    console.error(err)
  }
}

async function deleteGame(id){
  try{
    const response = await fetch(`http://127.0.0.1:8000/game/${id}`,{
        method:"DELETE"
      }
    )

    if(!response.ok){
      throw new Error(`Response Error:${response.status}`)
    }

    const result = await response.json()

    games.value = games.value.filter(game => game.id != id)


  }catch(err){
    console.error(err)
  }
}

async function clear(){
  try{
    const response = await fetch("http://127.0.0.1:8000/game",{
      method:"DELETE"
    })

    if(!response.ok){
      throw new Error(`Response Error: ${response.status}`)
    }

    console.log("List cleared")

    getGames()
  }catch(err){
    console.error(err)
  }
}

async function updateGame(){
  
}
</script>

<template>
  <h1>Game Backlog Tracker</h1>

  <button @click="getGames">Show List</button>

  <button 
    @click="getGame"
  >Display Game</button>

  <div
      v-for="game in games"
      :key="game.id"
  >
    {{game.name}}
    <button 
      @click="deleteGame(game.id)"
    >Delete Game</button>
  </div>

  <button @click="clear">Clear List</button>

</template>

<style scoped></style>

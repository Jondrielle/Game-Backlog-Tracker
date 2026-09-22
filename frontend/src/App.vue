<script setup>
import {ref} from 'vue'
import GameItem from "./components/GameItem.vue"

const games = ref([])

//filter params
const selectedGenre = ref(null)
const selectedStatus = ref(null)
const selectedPlatform = ref(null)
const searchName = ref("")

async function getGames(){
  try{

    const params = new URLSearchParams()

    if(selectedGenre.value){
      params.append("genre",selectedGenre.value)
    }

    if(selectedStatus.value){
      params.append("status",selectedStatus.value)
    }

    if(selectedPlatform.value){
      params.append("platform",selectedPlatform.value)
    }

    if(searchName.value){
      params.append("name",searchName.value)
    }

    const response = await fetch(`http://127.0.0.1:8000/?${params.toString()}`)

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

    const result = await response.json()

    console.log(result)
  }catch(err){
    console.error(err)
  }
}

async function addGame(game){
  try{
    const response = await fetch("http://127.0.0.1:8000/",
    {
      method:"POST",
      headers:{
        "Content-Type":
        "application/json"
      },
      body: JSON.stringify({
        name:game.name,
        status:game.status,
        rating:game.rating,
        notes:game.notes,
        platform:game.platform,
        genre:game.genre,
        release_date:game.release_date,
        date_completed:game.date_completed
      })
    })

    if(!response.ok){
      throw new Error(`Response Error: ${response.status}`)
    }

    const result = await response.json()

    games.value.push(result)

  }catch(err){
    console.log(err)
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

    games.value = games.value.filter(game => game.id !== id)


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

async function updateGame(id,updatedGame){
  try{
    const response = await fetch(`http://127.0.0.1:8000/${id}`,{
      method:"PATCH",
      headers:{
        "Content-Type":
        "application/json"
      },
      body: JSON.stringify(updatedGame)
    })

    if(!response.ok){
      throw new Error(`Response status: ${response.status}`)
    }

    await response.json()
  
    await getGames()
  }catch(err){
    console.error(err)
  }
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

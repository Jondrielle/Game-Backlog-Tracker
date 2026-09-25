<script setup>
import {ref,onMounted} from 'vue'
import GameItem from "./components/GameItem.vue"
import GameForm from "./components/GameForm.vue"

//data
const games = ref([])

//filter params
const selectedGenre = ref(null)
const selectedStatus = ref(null)
const selectedPlatform = ref(null)
const searchName = ref("")

//edit game
const formGame = ref({
  id: null,
  name: "",
  status: "",
  rating: null,
  notes: "",
  platform: "",
  genre: "",
  release_date: "",
  date_completed: null
})

//booleans
const isEditing = ref(false)
const showForm = ref(false)

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

    console.log(params.toString())
    
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
      if (response.status === 422) {
        throw new Error("Please check required fields.")
      }

      throw new Error("Failed to add game");

    }

    const result = await response.json()

    games.value.push(result)

    formGame.value={
      name:"",
      status:"",
      rating:null,
      notes:"",
      platform:"",
      genre:"",
      release_date:"",
      date_completed:null
    }

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

async function updateGame(updatedGame){
  try{
    const response = await fetch(`http://127.0.0.1:8000/game/${updatedGame.id}`,{
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

    isEditing.value = false

    formGame.value = ({
    id: null,
    name: "",
    status: "",
    rating: null,
    notes: "",
    platform: "",
    genre: "",
    release_date: "",
    date_completed: null
  })

  closeForm()

  }catch(err){
    console.error(err)
  }
}

function startEdit(game){
  formGame.value = {...game}
  
  isEditing.value = true
  showForm.value = true
}

function closeForm(){
  showForm.value = false
  isEditing.value = false
}

function openForm(){
  isEditing.value = false

    formGame.value = {
    id: null,
    name: "",
    status: "",
    rating: null,
    notes: "",
    platform: "",
    genre: "",
    release_date: "",
    date_completed: null
  }

  showForm.value = true
}

function handleSubmit(game){
  if(isEditing.value){
    updateGame(game)
  }else{
    addGame(game)
  }

  closeForm()
}

onMounted(()=>{
  getGames()
})

</script>

<template>
  <h1>Game Backlog Tracker</h1>

    <input v-model="searchName">
    <button @click="getGames">Search</button>

    <GameItem
      v-for="game in games"
      :key="game.id"
      :game="game"
      @edit="startEdit"
      @delete="deleteGame"
    />

  <button @click="clear">Clear List</button>

  <button @click="openForm">Open Add Form</button>

  <GameForm
    v-if="showForm"
    :isEditing="isEditing"
    :game="formGame"
    @cancel="closeForm"
    @submit="handleSubmit"
  />

</template>

<style scoped></style>

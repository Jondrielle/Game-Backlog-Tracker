<script setup>
import {ref} from 'vue'
import GameItem from "./components/GameItem.vue"

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

</script>

<template>
  <h1>Game Backlog Tracker</h1>


  <div
      v-for="game in games"
      :key="game.id"
  >
    Name:{{game.name}}
    Status:{{game.status}}
    Rating:{{game.rating}}
    Notes:{{game.notes}}
    Genre:{{game.genre}}
    Platform: {{game.platform}}
    Release Date: {{game.release_date}}
    Completed: {{game.date_completed}}
    <button 
      @click="deleteGame(game.id)"
    >Delete Game</button>
    <button @click="startEdit(game)">Edit</button>
  </div>
  <button @click="clear">Clear List</button>
  <button @click="openForm">Open Add Form</button>

  <form v-if="showForm" @submit.prevent="isEditing? updateGame(formGame):addGame(formGame)">
  
    <input
      v-model="formGame.name"
      type="text"
      placeholder="Game title"
    >

    <select v-model="formGame.status">
      <option disabled value="">Select status</option>
      <option value="Backlog">Backlog</option>
      <option value="Playing">Playing</option>
      <option value="Completed">Completed</option>
      <option value="Dropped">Dropped</option>
    </select>

    <select v-model="formGame.platform">
      <option disabled value>Select Platform</option>
      <option value="PC">PC</option>
      <option value="PlayStation">PlayStation</option>
      <option value="Xbox">Xbox</option>
      <option value="Switch">Switch</option>
    </select>

    <select v-model="formGame.genre">
      <option disabled value>Select genre</option>
      
      <option 
      value="Action">Action</option>
      
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

    <input
      v-model="formGame.rating"
      type="number"
      min="1"
      max="5"
      placeholder="Rating"
    >

    <textarea
      v-model="formGame.notes"
      type="text"
      placeholder="Notes"
    ></textarea>

    <input 
      v-model="formGame.release_date"
      type="date"
    >

    <input
      v-model="formGame.date_completed"
      type="date"
    >

    <button type="submit">{{ isEditing ? "Save Edit" : "Add Game"}}</button>

    <button type="button" @click="closeForm">Cancel</button>
  </form>

</template>

<style scoped></style>

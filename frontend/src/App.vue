<script setup>
import {ref,onMounted} from 'vue'

import GameItem from "./components/GameItem.vue"
import GameForm from "./components/GameForm.vue"
import AuthForm from "./components/AuthForm.vue"
import Profile from "./components/Profile.vue"

import {auth} from "./firebase"
import {createUserWithEmailAndPassword, signInWithEmailAndPassword,signOut,sendPasswordResetEmail,sendEmailVerification,deleteUser} from "firebase/auth";

//data
const games = ref([])

//igdb data
const igdbSearch = ref("")
const igdbResults = ref([])
const selectedIGDBGame = ref(null)

//authenication 
const userSignedIn = ref(false)

//pagination
const currentPage = ref(1)
const pageSize = 2
const totalGames = ref(0)

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
  genres: [],
  release_date: "",
  date_completed: null
})

//booleans
const isEditing = ref(false)
const showForm = ref(false)

async function searchIGDB() {
  const query = igdbSearch.value.trim()

  if (!query) {
    igdbResults.value = []
    return
  }

  const user = auth.currentUser

  if (!user) {
    console.error("Please sign in first.")
    return
  }

  try {
    const token = await user.getIdToken()

    const response = await fetch(
      `http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!response.ok) {
      throw new Error(await response.text())
    }

    igdbResults.value = await response.json()
  } catch (err) {
    console.error("IGDB search failed:", err)
    igdbResults.value = []
  }
}

async function getGames(){
  try{

    const user = auth.currentUser

    if (!user) {
      games.value = []
      totalGames.value = 0
      return
    }

    const token = await user.getIdToken()

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

    params.append("skip",(currentPage.value-1) * pageSize)

    params.append("limit", pageSize)

    console.log(params.toString())

    const response = await fetch(`http://127.0.0.1:8000/?${params.toString()}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if(!response.ok){
      throw new Error(`Response status: ${response.status}`)
    }

    const result = await response.json()

    console.log(result)

    games.value = result.games
    totalGames.value=result.total

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

    const user = auth.currentUser

    if (!user) {
      throw new Error("You must be signed in to add a game.")
    }

    const token = await user.getIdToken()

    const response = await fetch("http://127.0.0.1:8000/",
    {
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name:game.name,
        status:game.status,
        rating:game.rating,
        notes:game.notes,
        platform:game.platform,
        genres:game.genres,
        release_date:game.release_date,
        date_completed:game.date_completed
      })
    })

    if(!response.ok){
      if (response.status === 422) {
        throw new Error("Please check required fields.")
      }

      const errors = await response.json()
      console.log(errors)
      throw new Error("Failed to add game");

    }

    const result = await response.json()

    games.value.push(result)
    
    formGame.value={
          id:null,
          name:"",
          status:"",
          rating:null,
          notes:"",
          platform:"",
          genres:[],
          release_date:"",
          date_completed:null
    }

  }catch(err){
    console.log(err)
  }
}

async function deleteGame(id){
  try{

    const user = auth.currentUser


    if(!user){
      throw new Error("You must be signed in first before deleting a game")
    }

    const token = await user.getIdToken()
    const response = await fetch(`http://127.0.0.1:8000/game/${id}`,{
        method:"DELETE",
        headers:{
          Authorization: `Bearer ${token}`
        },
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

    const user = auth.currentUser

    if(!user){
      throw new Error("You must be signed in to clear a list")
    }

    const token = await user.getIdToken()

    const response = await fetch("http://127.0.0.1:8000/game",{
      method:"DELETE",
      headers:{
        Authorization: `Bearer ${token}`,
      },
    })

    if(!response.ok){
      throw new Error(`Response Error: ${response.status}`)
    }

    console.log("List cleared")

    await getGames()
  }catch(err){
    console.error(err)
  }
}

async function updateGame(updatedGame){
  try{

    const user = auth.currentUser

    if (!user) {
      throw new Error("You must be signed in to add a game.")
    }

    const token = await user.getIdToken()

    const response = await fetch(`http://127.0.0.1:8000/game/${updatedGame.id}`,{
      method:"PATCH",
      headers:{
        "Content-Type":"application/json",
        Authorization: `Bearer ${token}`,
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
    genres: [],
    release_date: "",
    date_completed: null
  })

  }catch(err){
    console.error(err)
  }
}

function startEdit(game){
  formGame.value = {
    ...game,
    genres: [...(game.genres ?? [])],
  }

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
    genres: [],
    release_date: "",
    date_completed: null
  }

  showForm.value = true
}

async function handleSubmit(game){
  if(isEditing.value){
    await updateGame(game)
  }else{
    await addGame(game)
  }

  closeForm()
}

async function clearFilters(){
  searchName.value = ""
  selectedStatus.value = null
  selectedGenre.value = null
  selectedPlatform.value = null

  currentPage.value = 1

  await getGames()
}

async function nextPage(){
  if(currentPage.value * pageSize < totalGames.value){
    currentPage.value++
    await getGames()
  }
}

async function previousPage(){
  if(currentPage.value > 1){
    currentPage.value--
    await getGames()
  }
}

async function signUp(credentials) {
  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      credentials.email,
      credentials.password
    );

    await sendEmailVerification(userCredential.user);

    const token = await userCredential.user.getIdToken(true);


    const response = await fetch("http://127.0.0.1:8000/auth/signup", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Backend status:", response.status);
      console.error("Backend response:", errorText);
      return;
    }

    userSignedIn.value = true

    console.log("User created and backend user registered");
  } catch (err) {
    console.error(err);
  } finally {
  }
}

async function login(credentials) {
  try {
    const userCredential = await signInWithEmailAndPassword(
      auth,
      credentials.email,
      credentials.password
    );

    const token = await userCredential.user.getIdToken(true);

    const response = await fetch("http://127.0.0.1:8000/auth/me", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const user = await response.json();
    userSignedIn.value = true

    console.log("Login successful", user);
  } catch (err) {
    console.error(err);
  } finally {
  }
}

async function logOut(){
  try{
    await signOut(auth)
    console.log("Sign out successful")

    userSignedIn.value = false
  }catch(err){
    console.error(err)
  }
}

async function resetPassword(email){
  try{
    await sendPasswordResetEmail(auth,email)
    console.log("Password reset sent")
  }catch(err){
    console.error(err)
  }
}

async function deleteAccount(){
  const user = auth.currentUser;

  if (!user) {
    throw new Error("No user is signed in");
  }

  const token = await user.getIdToken();

  const response = await fetch(
    "http://127.0.0.1:8000/auth/deleteAccount",
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  console.log("User Account Deleted Successfully")

  if (!response.ok) {
    throw new Error(await response.text());
  }

  await signOut(auth);

  userSignedIn.value = false
}

function selectIGDBGame(game) {
  selectedIGDBGame.value = game

  igdbResults.value = []
  igdbSearch.value = ""
  selectedIGDBGame.value = null

  formGame.value = {
    id: null,
    name: game.name,
    status: "Backlog",
    rating: null,
    notes: "",
    platform: game.platforms?.[0] || "",
    genres: game.genres || [],
    release_date: game.release_date || "",
    date_completed: null,
  }

  isEditing.value = false
  showForm.value = true
}

onMounted(()=>{
})

</script>

<template>
  <h1 class="title">Game Backlog Tracker</h1>
  <AuthForm
    v-if="!userSignedIn"
    @login="login"
    @signup="signUp"
    @reset="resetPassword"
  />

  <Profile
    @signout="logOut"
    @delete="deleteAccount"
    v-if="userSignedIn"
  /> 

  <div class="container" v-if="userSignedIn">

    <input v-model="searchName" placeholder="Search games...">
    <div class="igdb-search">
  <label>Find Games</label>

  <form @submit.prevent="searchIGDB">
    <input
      v-model="igdbSearch"
      placeholder="Search IGDB for a game..."
    />

    <button type="submit">
      Search IGDB
    </button>

  </form>

  <hr class="horizontal-line">
  <p v-if="igdbResults.length === 0 && igdbSearch">
    No results displayed yet. Search for a game to find matches.
  </p>

  <div
    v-for="game in igdbResults"
    :key="game.igdb_id ?? game.id"
    class="igdb-result"
  >
    <h3>{{ game.name }}</h3>

    <p v-if="game.release_date">
      Release date: {{ game.release_date }}
    </p>

    <p v-if="game.genres?.length">
      Genres: {{ game.genres.join(", ") }}
    </p>

    <p v-if="game.platforms?.length">
      Platforms: {{ game.platforms.join(", ") }}
    </p>

    <button @click="selectIGDBGame(game)">
      Use This Game
    </button>
  </div>
</div>
  <div class="userGames">
    <label>My Games</label>
    <div class="filters">
      <span>
        <select v-model="selectedStatus">
          <option :value="null">All Statuses</option>
          <option value="Backlog">Backlog</option>
          <option value="Playing">Playing</option>
          <option value="Completed">Completed</option>
          <option value="Dropped">Dropped</option>
        </select>
      </span>

      <span>
        <select v-model="selectedGenre">
          <option :value="null">All Genres</option>
          <option value="Action">Action</option>
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
      </span>

      <span>
        <select v-model="selectedPlatform">
          <option :value="null">All Platforms</option>
          <option value="PC">PC</option>
          <option value="PlayStation">PlayStation</option>
          <option value="Xbox">Xbox</option>
          <option value="Switch">Switch</option>
        </select>
      </span>
    </div>
      <GameItem
        v-for="game in games"
        :key="game.id"
        :game="game"
        @edit="startEdit"
        @delete="deleteGame"
      />
      <button @click="getGames">
        Apply Filters
      </button>

      <button @click="clearFilters">
        Clear Filters
      </button>

    </div>
  </div>


  <div class="functions" v-if="userSignedIn">
    <span>
      <button @click="clear">Clear List</button>
    </span>
  </div>

  <GameForm
    v-if="showForm"
    :isEditing="isEditing"
    :game="formGame"
    @cancel="closeForm"
    @submit="handleSubmit"
  />

  <div class="pagination" v-if="userSignedIn">
    <span>
      <button
        @click="previousPage"
        :disabled="currentPage === 1"
      >
        Previous
      </button>
    </span>

    <span>Page {{ currentPage }}</span>

    <span>
      <button 
        @click="nextPage"
        :disabled="currentPage * pageSize >= totalGames"
      >
        Next
      </button>
    </span>
  </div>
</template>

<style scoped>
  
/* Overall page */
:global(body) {
  margin: 0;
  background: #10131b;
  color: #e8eaf2;
  font-family: Inter, system-ui, -apple-system, sans-serif;
}

:global(*) {
  box-sizing: border-box;
}

:global(button),
:global(input),
:global(select) {
  font: inherit;
}

:global(button) {
  padding: 10px 16px;
  border: 1px solid #49415f;
  border-radius: 8px;
  background: #29243a;
  color: #f4f0ff;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

:global(button:hover:not(:disabled)) {
  background: #443663;
  transform: translateY(-1px);
}

:global(button:disabled) {
  opacity: 0.4;
  cursor: not-allowed;
}

:global(input),
:global(select) {
  min-width: 0;
  padding: 11px 12px;
  border: 1px solid #353b4b;
  border-radius: 8px;
  background: #191e29;
  color: #e8eaf2;
}

:global(input:focus),
:global(select:focus) {
  outline: 2px solid #a78bfa;
  outline-offset: 1px;
}

.title {
  margin: 0 0 28px;
  padding: 28px 16px;
  text-align: center;
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  letter-spacing: 0.04em;
  color: #c4b5fd;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: min(1100px, calc(100% - 32px));
  margin: 0 auto;
  padding: 24px;
  background: #191e29;
  border: 1px solid #2b3242;
  border-radius: 16px;
}

.container > input {
  width: 100%;
}

.igdb-search {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.igdb-search label,
.userGames > label {
  font-size: 1.2rem;
  font-weight: 700;
  color: #c4b5fd;
}

.igdb-search form {
  display: flex;
  gap: 10px;
  width: 100%;
}

.igdb-search input {
  flex: 1;
}

.horizontal-line {
  width: 100%;
  border: 0;
  border-top: 1px solid #353b4b;
  margin: 8px 0;
}

.igdb-result {
  padding: 16px;
  border: 1px solid #353b4b;
  border-radius: 12px;
  background: #202635;
}

.igdb-result h3 {
  margin-top: 0;
  margin-bottom: 8px;
}

.igdb-result p {
  color: #b8bfd0;
  margin: 6px 0;
}

.igdb-result button {
  margin-top: 8px;
}

.userGames {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.filters span {
  flex: 1 1 160px;
}

.filters select {
  width: 100%;
}

/* GameItem components will need their own styling
   in GameItem.vue if they contain the game cards. */

.functions {
  display: flex;
  justify-content: center;
  width: min(1100px, calc(100% - 32px));
  margin: 20px auto;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 24px 16px;
}

@media (max-width: 600px) {
  .container {
    width: calc(100% - 20px);
    padding: 16px;
  }

  .igdb-search form {
    flex-direction: column;
  }

  .filters {
    flex-direction: column;
  }

  .pagination {
    gap: 10px;
  }
}
</style>

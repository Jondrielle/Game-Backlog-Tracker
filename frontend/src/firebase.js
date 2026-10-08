import { initializeApp } from 'firebase/app';
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyA8dSlipYe3c3i0tzadgwa1_tnhLgClKso",
  authDomain: "game-backlog-bcecb.firebaseapp.com",
  projectId: "game-backlog-bcecb",
  storageBucket: "game-backlog-bcecb.firebasestorage.app",
  messagingSenderId: "783112078083",
  appId: "1:783112078083:web:81d254f439466bcad89f36"
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);

export{auth};
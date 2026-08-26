// Konfigurasi Firebase HANYA AKAN BEKERJA SETELAH ANDA MEMBUAT PROYEK DI FIREBASE CONSOLE
// Silakan buat proyek di firebase.google.com, aktifkan Firestore dan Authentication (Email/Password)
// Lalu ganti nilai-nilai di bawah ini dengan konfigurasi dari Firebase Anda.

const firebaseConfig = {
    apiKey: "GANTI_DENGAN_API_KEY_ANDA",
    authDomain: "GANTI_DENGAN_PROJECT_ID.firebaseapp.com",
    projectId: "GANTI_DENGAN_PROJECT_ID",
    storageBucket: "GANTI_DENGAN_PROJECT_ID.appspot.com",
    messagingSenderId: "GANTI_DENGAN_SENDER_ID",
    appId: "GANTI_DENGAN_APP_ID"
};

// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}
const auth = firebase.auth();
const db = firebase.firestore();

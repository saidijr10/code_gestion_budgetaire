<template>
    <form @submit.prevent="handleSubmit" class="form-container">
        <h2>Créer un RIB</h2>

        <label for="rib">RIB :</label>
        <input id="rib" v-model="rib.rib" type="text" />
        <p v-if="errors.rib" class="error">{{ errors.rib }}</p>

        <label for="prestataire">Prestataire :</label>
        <select id="prestataire" v-model="rib.prestataire">
            <option value="">-- Choisir un prestataire --</option>
            <option v-for="p in prestataires" :key="p.id" :value="p.id">
                {{ p.nom || p.raison_sociale }}
            </option>
        </select>
        <p v-if="errors.prestataire" class="error">{{ errors.prestataire }}</p>

        <button type="submit" class="btn-primary">Créer RIB</button>
    </form>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const rib = reactive({
    rib: '',
    prestataire: '',
})

const errors = reactive({})
const prestataires = ref([])
const codesBanqueValid = ref([])
const codesLocaliteValid = ref([])

const router = useRouter()

function clearErrors() {
    Object.keys(errors).forEach(k => delete errors[k])
}

// Validation RIB marocain
function verifierRIBMarocain(ribValue, codesBanqueValid, codesLocaliteValid) {
    const rib = ribValue.replace(/\s+/g, '')
    if (rib.length !== 24) return 'Invalide (Longueur)'
    if (!/^\d+$/.test(rib)) return 'Invalide (Non Numérique)'

    const codeBanque = rib.slice(0, 3)
    const codeLocalite = rib.slice(3, 6)
    const numeroCompte = rib.slice(6, 22)
    const cleRIB = rib.slice(22)

    if (!codesBanqueValid.includes(codeBanque)) return 'Invalide (Code Banque)'
    if (!codesLocaliteValid.includes(codeLocalite)) return 'Invalide (Code Localité)'

    const nombreAVerifier = codeBanque + codeLocalite + numeroCompte + '00'

    let reste = 0
    for (let i = 0; i < nombreAVerifier.length; i++) {
        const tempDiv = '' + reste + nombreAVerifier[i]
        reste = parseInt(tempDiv, 10) % 97
    }
    const cleCalculee = reste === 0 ? 97 : 97 - reste
    const cleCalculeeFormatee = cleCalculee < 10 ? '0' + cleCalculee : '' + cleCalculee

    return cleCalculeeFormatee === cleRIB ? 'Valide' : 'Invalide (Clé RIB)'
}

function validate() {
    clearErrors()
    if (!rib.rib) errors.rib = 'Le RIB est obligatoire.'
    if (!rib.prestataire) errors.prestataire = 'Le prestataire est obligatoire.'
    if (rib.rib) {
        const resultat = verifierRIBMarocain(rib.rib, codesBanqueValid.value, codesLocaliteValid.value)
        if (resultat !== 'Valide') {
            errors.rib = 'RIB ' + resultat
        }
    }
    return Object.keys(errors).length === 0
}

async function loadPrestataires() {
    try {
        const res = await fetch('/api/prestataires/')
        if (!res.ok) throw new Error('Erreur API prestataires')
        prestataires.value = await res.json()
    } catch {
        alert('Erreur lors du chargement des prestataires.')
    }
}

async function loadCodesBanques() {
    try {
        const res = await fetch('/api/codebanques/')
        if (!res.ok) throw new Error('Erreur API codes banques')
        const data = await res.json()
        codesBanqueValid.value = data.map(item => item.code)
    } catch {
        alert('Erreur lors du chargement des codes banques.')
    }
}

async function loadCodesLocalites() {
    try {
        const res = await fetch('/api/codelocalites/')
        if (!res.ok) throw new Error('Erreur API codes localités')
        const data = await res.json()
        codesLocaliteValid.value = data.map(item => item.code)
    } catch {
        alert('Erreur lors du chargement des codes localités.')
    }
}

async function createRib(payload) {
    const res = await fetch('/api/ribs/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
    const data = await res.json()
    if (!res.ok) {
        // Gestion des erreurs retournées sous forme {"rib": ["..."], "prestataire": ["..."]}
        if (data.rib) throw new Error(data.rib.join(', '))
        if (data.prestataire) throw new Error(data.prestataire.join(', '))
        throw new Error(data.detail || 'Erreur lors de la création du RIB')
    }
    return data
}

async function handleSubmit() {
    if (!validate()) return
    try {
        await createRib({
            rib: rib.rib,
            prestataire: parseInt(rib.prestataire),
        })
        alert('RIB créé avec succès !')
        router.push('/ribs')
    } catch (err) {
        const message = err.message || ''
        clearErrors()

        // Vérifie le message exact retourné par l'API
        if (message.toLowerCase().includes('rib with this rib already exists')) {
            errors.rib = ' Ce RIB existe déjà. Veuillez saisir un RIB différent.'
        } else if (message.toLowerCase().includes('prestataire')) {
            errors.prestataire = message
        } else {
            errors.rib = message
        }
    }
}


onMounted(() => {
    loadPrestataires()
    loadCodesBanques()
    loadCodesLocalites()
})
</script>

<style scoped>
.form-container {
    max-width: 500px;
    margin: 2rem auto;
    padding: 2rem;
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

h2 {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.3rem;
    font-weight: bold;
    color: #333;
}

input,
select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    margin-bottom: 1rem;
    border: 1.5px solid #ccc;
    border-radius: 5px;
    font-size: 1rem;
    font-family: inherit;
    box-sizing: border-box;
}

input:focus,
select:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 4px rgba(0, 123, 255, 0.4);
}

.error {
    color: #d93025;
    font-size: 0.85rem;
    margin-top: -0.8rem;
    margin-bottom: 1rem;
}

.btn-primary {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.5rem 1.25rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
}

.btn-primary:hover {
    background-color: #0056b3;
}
</style>

<template>
    <form @submit.prevent="handleSubmit" class="form-container">
        <h2>Modifier RIB</h2>

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

        <button type="submit" class="btn-submit">Enregistrer</button>
    </form>
</template>

<script setup>
import '@/assets/styles/Form.css'
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getRibById, updateRib } from '@/Services/RibServices.js'
import { getPrestataires } from '@/Services/PrestaServices.js'

const route = useRoute()
const router = useRouter()

const rib = reactive({
    rib: '',
    prestataire: '',
})

const errors = reactive({})
const prestataires = ref([])
const codesBanqueValid = ref([])
const codesLocaliteValid = ref([])

function clearErrors() {
    Object.keys(errors).forEach(k => delete errors[k])
}

function verifierRIBMarocain(ribValue, codesBanqueValid, codesLocaliteValid) {
    const ribClean = ribValue.replace(/\s+/g, '')
    if (ribClean.length !== 24) return 'Invalide (Longueur)'
    if (!/^\d+$/.test(ribClean)) return 'Invalide (Non Numérique)'

    const codeBanque = ribClean.slice(0, 3)
    const codeLocalite = ribClean.slice(3, 6)
    const numeroCompte = ribClean.slice(6, 22)
    const cleRIB = ribClean.slice(22)

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
        prestataires.value = await getPrestataires()
    } catch {
        alert('Erreur lors du chargement des prestataires.')
    }
}

async function loadCodesBanques() {
    try {
        const response = await fetch('/api/codebanques/')
        if (!response.ok) throw new Error('Erreur API codes banques')
        const data = await response.json()
        codesBanqueValid.value = data.map(item => item.code)
    } catch {
        alert('Erreur lors du chargement des codes banques.')
    }
}

async function loadCodesLocalites() {
    try {
        const response = await fetch('/api/codelocalites/')
        if (!response.ok) throw new Error('Erreur API codes localités')
        const data = await response.json()
        codesLocaliteValid.value = data.map(item => item.code)
    } catch {
        alert('Erreur lors du chargement des codes localités.')
    }
}

async function loadRib() {
    try {
        const data = await getRibById(route.params.id)
        rib.rib = data.rib
        rib.prestataire = data.prestataire
    } catch {
        alert('Erreur de chargement du RIB.')
    }
}

async function handleSubmit() {
    if (!validate()) return
    try {
        await updateRib(route.params.id, {
            rib: rib.rib,
            prestataire: typeof rib.prestataire === 'object' ? rib.prestataire.id : rib.prestataire,
        })
        alert('RIB mis à jour avec succès !')
        router.push('/ribs')
    } catch (err) {
        alert('Erreur lors de la mise à jour du RIB.')
        console.error(err)
    }
}

onMounted(() => {
    loadPrestataires()
    loadCodesBanques()
    loadCodesLocalites()
    loadRib()
})
</script>

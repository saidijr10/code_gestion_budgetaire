<template>
    <div v-if="formLoaded" class="form-container">
        <h2>Modifier Prestataire</h2>
        <form @submit.prevent="handleSubmit" novalidate>
            <label>Type :</label>
            <select v-model="form.type">
                <option disabled value="">-- Sélectionnez un type --</option>
                <option value="morale">Morale</option>
                <option value="physique">Physique</option>
            </select>
            <p v-if="errors.type" class="error">{{ errors.type }}</p>

            <div v-if="form.type === 'physique'">
                <label>Nom :</label>
                <input type="text" v-model="form.nom" />
                <p v-if="errors.nom" class="error">{{ errors.nom }}</p>

                <label>Prénom :</label>
                <input type="text" v-model="form.prenom" />
                <p v-if="errors.prenom" class="error">{{ errors.prenom }}</p>

                <label>CIN :</label>
                <input type="text" v-model="form.cin" />
                <p v-if="errors.cin" class="error">{{ errors.cin }}</p>
            </div>

            <div v-else-if="form.type === 'morale'">
                <label>Raison Sociale :</label>
                <input type="text" v-model="form.raison_sociale" />
                <p v-if="errors.raison_sociale" class="error">{{ errors.raison_sociale }}</p>

                <label>Adresse :</label>
                <input type="text" v-model="form.adresse" />
                <p v-if="errors.adresse" class="error">{{ errors.adresse }}</p>
            </div>

            <label>Téléphone :</label>
            <input type="text" v-model="form.tel" />
            <p v-if="errors.tel" class="error">{{ errors.tel }}</p>

            <label v-if="form.type === 'morale'">Contact :</label>
            <input v-if="form.type === 'morale'" type="text" v-model="form.contact" />

            <button type="submit" class="btn-submit">Modifier</button>
            <p v-if="generalError" class="error">{{ generalError }}</p>
        </form>
    </div>
    <p v-else>Chargement...</p>
</template>

<script setup>
import '@/assets/styles/Form.css'
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const form = reactive({
    type: '',
    nom: '',
    prenom: '',
    cin: '',
    raison_sociale: '',
    adresse: '',
    tel: '',
    contact: '',
})

const errors = reactive({})
const generalError = ref('')
const formLoaded = ref(false)

function clearErrors() {
    Object.keys(errors).forEach((k) => delete errors[k])
}

function validate() {
    clearErrors()
    let valid = true

    if (!form.type) {
        errors.type = 'Le type est obligatoire.'
        valid = false
    }
    if (form.type === 'physique') {
        if (!form.nom?.trim()) {
            errors.nom = 'Le nom est obligatoire.'
            valid = false
        }
        if (!form.prenom?.trim()) {
            errors.prenom = 'Le prénom est obligatoire.'
            valid = false
        }
        if (!form.cin?.trim()) {
            errors.cin = 'Le CIN est obligatoire.'
            valid = false
        }
    } else if (form.type === 'morale') {
        if (!form.raison_sociale?.trim()) {
            errors.raison_sociale = 'La raison sociale est obligatoire.'
            valid = false
        }
        if (!form.adresse?.trim()) {
            errors.adresse = 'L’adresse est obligatoire.'
            valid = false
        }
    }

    if (!form.tel?.trim()) {
        errors.tel = 'Le téléphone est obligatoire.'
        valid = false
    }

    return valid
}

async function loadPrestataire() {
    try {
        const id = route.params.id
        const res = await fetch(`/api/prestataires/${id}/`)
        if (!res.ok) throw new Error('Prestataire introuvable')
        const data = await res.json()

        Object.assign(form, data)
        formLoaded.value = true
    } catch (e) {
        generalError.value = 'Erreur lors du chargement du prestataire.'
        console.error(e)
    }
}

async function handleSubmit() {
    if (!validate()) return

    try {
        const id = route.params.id
        const res = await fetch(`/api/prestataires/${id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form),
        })
        if (!res.ok) {
            const err = await res.json()
            generalError.value = err.detail || 'Erreur lors de la modification.'
            return
        }
        alert('Prestataire modifié avec succès.')
        router.push('/liste')
    } catch (e) {
        generalError.value = 'Erreur lors de la soumission.'
        console.error(e)
    }
}

onMounted(() => {
    loadPrestataire()
})
</script>

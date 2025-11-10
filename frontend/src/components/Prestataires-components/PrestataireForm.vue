<template>
    <form @submit.prevent="handleSubmit" class="form-container">
        <h2>Créer un Prestataire</h2>
        <label for="type">Type :</label>
        <select id="type" v-model="prestataire.type">
            <option disabled value="">-- Sélectionnez un type --</option>
            <option value="physique">Physique</option>
            <option value="morale">Morale</option>
        </select>
        <p v-if="errors.type" class="error">{{ errors.type }}</p>

        <template v-if="prestataire.type === 'physique'">
            <label for="nom">Nom :</label>
            <input id="nom" v-model="prestataire.nom" type="text" />
            <p v-if="errors.nom" class="error">{{ errors.nom }}</p>

            <label for="prenom">Prénom :</label>
            <input id="prenom" v-model="prestataire.prenom" type="text" />
            <p v-if="errors.prenom" class="error">{{ errors.prenom }}</p>

            <label for="cin">CIN :</label>
            <input id="cin" v-model="prestataire.cin" type="text" />
            <p v-if="errors.cin" class="error">{{ errors.cin }}</p>

            
        <label for="telephone">Téléphone :</label>
        <input id="telephone" v-model="prestataire.telephone" type="text" />
        <p v-if="errors.telephone" class="error">{{ errors.telephone }}</p>
        </template>

        <template v-else-if="prestataire.type === 'morale'">
            <label for="raison_sociale">Raison sociale :</label>
            <input id="raison_sociale" v-model="prestataire.raison_sociale" type="text" />
            <p v-if="errors.raison_sociale" class="error">{{ errors.raison_sociale }}</p>

            <label for="adresse">Adresse :</label>
            <input id="adresse" v-model="prestataire.adresse" type="text" />
            <p v-if="errors.adresse" class="error">{{ errors.adresse }}</p>

            <label for="contact">Contact :</label>
            <input id="contact" v-model="prestataire.contact" type="text" />
            <p v-if="errors.contact" class="error">{{ errors.contact }}</p>

            
        <label for="telephone">Téléphone :</label>
        <input id="telephone" v-model="prestataire.telephone" type="text" />
        <p v-if="errors.telephone" class="error">{{ errors.telephone }}</p>
        </template>


        <button type="submit" class="btn-primary">Ajouter</button>
    </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createPrestataire } from '@/Services/PrestaServices'

const router = useRouter()

const prestataire = reactive({
    type: '',
    nom: '',
    prenom: '',
    cin: '',
    raison_sociale: '',
    adresse: '',
    contact: '',
    telephone: '',
})

const errors = reactive({})

function validateTelephone(tel) {
    const regex = /^0\d{9}$/
    return regex.test(tel)
}

function validate() {
    Object.keys(errors).forEach((key) => delete errors[key])

    if (!prestataire.type) errors.type = 'Le type est requis.'

    if (prestataire.type === 'physique') {
        if (!prestataire.nom) errors.nom = 'Le nom est requis.'
        if (!prestataire.prenom) errors.prenom = 'Le prénom est requis.'
        if (!prestataire.cin) errors.cin = 'Le CIN est requis.'
    }

    if (prestataire.type === 'morale') {
        if (!prestataire.raison_sociale) errors.raison_sociale = 'La raison sociale est requise.'
        if (!prestataire.adresse) errors.adresse = 'L’adresse est requise.'
        if (!prestataire.contact) errors.contact = 'Le contact est requis.'
    }

    if (!prestataire.telephone) {
        errors.telephone = 'Le téléphone est requis.'
    } else if (!validateTelephone(prestataire.telephone)) {
        errors.telephone = 'Le téléphone doit commencer par 0 et contenir exactement 10 chiffres.'
    }

    return Object.keys(errors).length === 0
}
async function handleSubmit() {
    if (!validate()) return

    let payload = {
        type: prestataire.type,
        tel: prestataire.telephone,  // correction ici
    }

    if (prestataire.type === 'physique') {
        payload.nom = prestataire.nom
        payload.prenom = prestataire.prenom
        payload.cin = prestataire.cin
    } else if (prestataire.type === 'morale') {
        payload.raison_sociale = prestataire.raison_sociale
        payload.adresse = prestataire.adresse
        payload.contact = prestataire.contact
    }

    try {
        await createPrestataire(payload)
        alert('Prestataire créé avec succès !')
        router.push('/liste')
    } catch (err) {
        if (typeof err === 'object') {
            const message = Object.values(err).flat().join(', ')
            alert('Erreur lors de la création du prestataire : ' + message)
        } else {
            alert('Erreur inconnue.')
        }
    }
}

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

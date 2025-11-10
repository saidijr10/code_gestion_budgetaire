
<template>
    <form @submit.prevent="handleSubmit" class="form-container" v-if="form">
        <h2>Modifier Ligne Budgétaire</h2>

        <label for="budget">Budget (dépenses uniquement) :</label>
        <select id="budget" v-model="form.budget" required>
            <option disabled value="">-- Sélectionnez un budget --</option>
            <option v-for="budget in budgets" :key="budget.id" :value="budget.id">
                {{ budget.annee }} - {{ budget.type }}
            </option>
        </select>
        <p v-if="errors.budget" class="error">{{ errors.budget }}</p>

        <label for="prestataire">Prestataire :</label>
        <select id="prestataire" v-model="form.prestataire" required>
            <option disabled value="">-- Sélectionnez un prestataire --</option>
            <option v-for="presta in prestataires" :key="presta.id" :value="presta.id">
                {{ presta.nom || presta.raison_sociale || ('Prestataire #' + presta.id) }}
            </option>
        </select>
        <p v-if="errors.prestataire" class="error">{{ errors.prestataire }}</p>

        <label for="rubrique">Rubrique :</label>
        <input id="rubrique" type="text" v-model="form.rubrique" placeholder="Rubrique (facultatif)" />

        <label for="sous_rubrique">Sous-rubrique :</label>
        <input id="sous_rubrique" type="text" v-model="form.sous_rubrique" placeholder="Sous-rubrique (facultatif)" />


        <label for="montant">Montant TTC :</label>
        <input
            id="montant"
            type="number"
            step="0.01"
            v-model.number="form.montant_budget_ttc"
            placeholder="Exemple : 1500.00"
            required
        />
        <p v-if="errors.montant_budget_ttc" class="error">{{ errors.montant_budget_ttc }}</p>
        <label>Montant en lettres :</label>
        <textarea readonly rows="2" class="readonly-textarea" :value="montantEnLettres"></textarea>

        <button type="submit" class="btn-submit">Modifier</button>

        <p v-if="error" class="error">{{ error }}</p>
    </form>
</template>


<script setup>
import { reactive, ref, onMounted,computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const form = reactive({
    budget: '',
    prestataire: '',
    montant_budget_ttc: '',
    rubrique: '',         
    sous_rubrique: '', 
})

const errors = reactive({})
const error = ref('')
const budgets = ref([])
const prestataires = ref([])

async function loadBudgets() {
    try {
        const res = await fetch('/api/budgets-depenses/')
        if (!res.ok) throw new Error('Erreur chargement budgets')
        budgets.value = await res.json()
    } catch (e) {
        error.value = "Erreur lors du chargement des budgets 'dépenses'."
    }
}

async function loadPrestataires() {
    try {
        const res = await fetch('/api/prestataires/')
        if (!res.ok) throw new Error('Erreur chargement prestataires')
        prestataires.value = await res.json()
    } catch (e) {
        error.value = 'Erreur lors du chargement des prestataires.'
    }
}
async function loadLigne() {
    try {
        const res = await fetch(`/api/ligne-budgetaire/${route.params.id}/`)
        if (!res.ok) throw new Error('Erreur chargement ligne budgétaire')
        const data = await res.json()

        // Ici tu récupères les id
        form.budget = data.budget.id
        form.prestataire = data.prestataire.id
        form.montant_budget_ttc = parseFloat(data.montant_budget_ttc)
        form.rubrique = data.rubrique || ''         
        form.sous_rubrique = data.sous_rubrique || '' 
    } catch (e) {
        error.value = 'Erreur lors du chargement des données.'
        console.error(e)
    }
}


function convertirEnLettres(montant) {
    const unites = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf']
    const dizaines = ['', '', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante', 'quatre-vingt', 'quatre-vingt']

    function enLettres(n) {
        if (n === 0) return 'zéro'
        if (n < 20) return unites[n]
        if (n < 100) {
            const d = Math.floor(n / 10), u = n % 10
            let str = dizaines[d]
            if (d === 7 || d === 9) str += '-' + unites[10 + u]
            else if (u === 1 && d !== 8) str += ' et un'
            else if (u > 0) str += '-' + unites[u]
            return str
        }
        if (n < 1000) {
            const c = Math.floor(n / 100), r = n % 100
            let str = (c === 1 ? 'cent' : unites[c] + ' cent')
            if (r > 0) str += ' ' + enLettres(r)
            return str
        }
        if (n < 1000000) {
            const mil = Math.floor(n / 1000), r = n % 1000
            let str = (mil === 1 ? 'mille' : enLettres(mil) + ' mille')
            if (r > 0) str += ' ' + enLettres(r)
            return str
        }
        if (n < 1000000000) {
            const million = Math.floor(n / 1000000), r = n % 1000000
            let str = (million === 1 ? 'un million' : enLettres(million) + ' millions')
            if (r > 0) str += ' ' + enLettres(r)
            return str
        }
        return 'nombre trop grand'
    }

    const entier = Math.floor(montant)
    const centimes = Math.round((montant - entier) * 100)
    let texte = entier === 0 ? 'zéro dirham' : enLettres(entier) + ' dirham' + (entier > 1 ? 's' : '')
    if (centimes > 0) texte += ' et ' + enLettres(centimes) + ' centime' + (centimes > 1 ? 's' : '')
    return texte
}

const montantEnLettres = computed(() => {
    return convertirEnLettres(form.montant_budget_ttc || 0)
})

function validate() {
    Object.keys(errors).forEach((key) => delete errors[key])

    if (!form.budget) errors.budget = 'Le budget est requis.'
    if (!form.prestataire) errors.prestataire = 'Le prestataire est requis.'
    if (form.montant_budget_ttc === '' || form.montant_budget_ttc === null) {
        errors.montant_budget_ttc = 'Le montant est requis.'
    } else if (form.montant_budget_ttc <= 0) {
        errors.montant_budget_ttc = 'Le montant doit être positif.'
    }

    return Object.keys(errors).length === 0
}
async function handleSubmit() {
    if (!validate()) return

    try {
        const res = await fetch(`/api/ligne-budgetaire/${route.params.id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                budget_id: form.budget,
                prestataire_id: form.prestataire,
                montant_budget_ttc: form.montant_budget_ttc,
                rubrique: form.rubrique,              
                sous_rubrique: form.sous_rubrique,  
                
            }),
        })
        if (!res.ok) {
            const errData = await res.json()
            throw new Error(JSON.stringify(errData))
        }
        alert('Ligne budgétaire modifiée avec succès !')
        router.push('/LigneBudgetaire')
    } catch (e) {
        error.value = "Erreur lors de la modification de la ligne budgétaire."
        console.error(e)
    }
}


onMounted(() => {
    loadBudgets()
    loadPrestataires()
    loadLigne()
})
</script>
<style scoped src="@/assets/styles/Form.css"></style>
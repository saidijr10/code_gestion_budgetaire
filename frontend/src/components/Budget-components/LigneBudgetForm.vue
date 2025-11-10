<template>
    <form @submit.prevent="handleSubmit" class="form-container">
        <h2>Créer une Ligne Budgétaire</h2>
        <label for="budget">Budget (dépenses uniquement) :</label>
        <select id="budget" v-model="form.budget">
            <option disabled value="">-- Sélectionnez un budget --</option>
            <option v-for="budget in budgets" :key="budget.id" :value="budget.id">
                {{ budget.annee }} - {{ budget.type }}
            </option>
        </select>
        <p v-if="errors.budget" class="error">{{ errors.budget }}</p>

        <label for="prestataire">Prestataire :</label>
        <select id="prestataire" v-model="form.prestataire">
            <option disabled value="">-- Sélectionnez un prestataire --</option>
            <option v-for="presta in prestataires" :key="presta.id" :value="presta.id">
                {{ presta.nom || presta.raison_sociale || "Prestataire #" + presta.id }}
            </option>
        </select>
        <p v-if="errors.prestataire" class="error">{{ errors.prestataire }}</p>
        <label for="rubrique">Rubrique :</label>
        <input id="rubrique" v-model="form.rubrique" placeholder="Exemple : Communication" />

        <label for="sous_rubrique">Sous-rubrique :</label>
        <input id="sous_rubrique" v-model="form.sous_rubrique" placeholder="Exemple : Com presse" />

        <label for="montant">Montant TTC :</label>
        <input id="montant" type="number" step="0.01" v-model.number="form.montant_budget_ttc"
            placeholder="Exemple : 1500.00" />
        <p v-if="errors.montant_budget_ttc" class="error">{{ errors.montant_budget_ttc }}</p>

        <label>Montant en lettres :</label>
        <textarea readonly rows="2" class="readonly-textarea" :value="montantEnLettres"></textarea>

        <button type="submit" class="btn-submit">Créer</button>
        <p v-if="error" class="error">{{ error }}</p>
    </form>
</template>

<script setup>
import { reactive, ref, onMounted,computed } from 'vue'
import { useRouter } from 'vue-router'

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
const router = useRouter()

async function loadBudgets() {
    try {
        const res = await fetch('/api/budgets-depenses/')
        if (!res.ok) throw new Error('Erreur lors du chargement des budgets')
        budgets.value = await res.json()
    } catch (e) {
        error.value = "Erreur lors du chargement des budgets 'dépenses'."
        console.error(e)
    }
}

async function loadPrestataires() {
    try {
        const res = await fetch('/api/prestataires/')
        if (!res.ok) throw new Error('Erreur lors du chargement des prestataires')
        prestataires.value = await res.json()
    } catch (e) {
        error.value = "Erreur lors du chargement des prestataires."
        console.error(e)
    }
}

function validate() {
    Object.keys(errors).forEach(key => delete errors[key])

    if (!form.budget) errors.budget = 'Le budget est requis.'
    if (!form.prestataire) errors.prestataire = 'Le prestataire est requis.'
    if (form.montant_budget_ttc === '' || form.montant_budget_ttc === null) {
        errors.montant_budget_ttc = 'Le montant est requis.'
    } else if (form.montant_budget_ttc <= 0) {
        errors.montant_budget_ttc = 'Le montant doit être positif.'
    }

    return Object.keys(errors).length === 0
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

async function handleSubmit() {
    if (!validate()) return

    try {
        const res = await fetch('/api/ligne-budgetaire/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                budget_id: form.budget,
                prestataire_id: form.prestataire,
                montant_budget_ttc: form.montant_budget_ttc,
                rubrique: form.rubrique,
                sous_rubrique: form.sous_rubrique
            }),
        })
        if (!res.ok) {
            const errData = await res.json()
            throw errData
        }
        alert('Ligne budgétaire créée avec succès !')
        router.push('/LigneBudgetaire') // adapte la route selon ton projet
    } catch (e) {
        error.value = 'Erreur lors de la création de la ligne budgétaire.'
        console.error(e)
    }
}

onMounted(() => {
    loadBudgets()
    loadPrestataires()
})
</script>

<style scoped>
.form-container {
    max-width: 500px;
    margin: 2rem auto;
    background-color: #f9fafb;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1f2937;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

h2 {
    font-size: 1.6rem;
    font-weight: 700;
    color: #2563eb;
    text-align: center;
    margin-bottom: 1rem;
}

label {
    font-weight: 600;
    display: block;
    margin-bottom: 0.3rem;
}

input,
select,
textarea {
    width: 100%;
    padding: 0.6rem 0.75rem;
    border: 1.8px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    resize: vertical;
}

input:focus,
select:focus,
textarea:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    outline: none;
}

.readonly-textarea {
    background-color: #f3f4f6;
    color: #374151;
    resize: none;
}

.btn-submit {
    background-color: #2563eb;
    color: white;
    font-weight: 600;
    padding: 0.7rem 1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
    margin-top: 1rem;
}

.btn-submit:hover {
    background-color: #1e40af;
}

.error {
    color: #dc2626;
    font-size: 0.875rem;
    font-weight: 600;
}
</style>

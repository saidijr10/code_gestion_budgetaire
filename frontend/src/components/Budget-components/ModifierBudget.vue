<template>
    <form @submit.prevent="handleSubmit" class="form-container">
        <h2>Modifier le Budget</h2>

        <label>Année :</label>
        <input v-model="form.annee" type="number" />
        <p v-if="errors.annee" class="error">{{ errors.annee }}</p>

        <label for="type">Type :</label>
        <select id="type" v-model="form.type">
            <option disabled value="">-- Sélectionnez un type --</option>
            <option value="depenses">Dépenses</option>
            <option value="recette">Recette</option>
        </select>
        <p v-if="errors.type" class="error">{{ errors.type }}</p>

        <label>Date de création :</label>
        <input v-model="form.date_creation" type="date" />
        <p v-if="errors.date_creation" class="error">{{ errors.date_creation }}</p>

        <button type="submit" class="btn-submit">Modifier</button>
        <p v-if="error" class="error">{{ error }}</p>
    </form>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getBudgetById, updateBudget, getBudgets } from '@/Services/BudgetServices.js'

const router = useRouter()
const route = useRoute()

const form = reactive({
    annee: '',
    type: '',
    date_creation: '',
})

const errors = reactive({})
const error = ref('')
const budgetsExistants = ref([])

async function loadBudget() {
    try {
        const data = await getBudgetById(route.params.id)
        form.annee = data.annee
        form.type = data.type
        form.date_creation = data.date_creation
    } catch (e) {
        error.value = "Erreur lors du chargement du budget."
        console.error(e)
    }
}

async function loadBudgets() {
    try {
        budgetsExistants.value = await getBudgets()
    } catch (err) {
        console.error("Erreur lors du chargement des budgets :", err)
    }
}

function validate() {
    Object.keys(errors).forEach(key => delete errors[key])

    if (!form.annee) errors.annee = "L’année est requise."
    if (!form.type) errors.type = "Le type est requis."
    else if (!['depenses', 'recette'].includes(form.type))
        errors.type = 'Le type doit être "Dépenses" ou "Recette".'

    if (!form.date_creation) errors.date_creation = "La date de création est requise."

    // Vérification unicité année + type sauf pour le budget actuel
    const existe = budgetsExistants.value.some(
        b => b.id !== Number(route.params.id) &&
            Number(b.annee) === Number(form.annee) &&
            b.type === form.type
    )

    if (existe) {
        errors.type = `Un budget pour l'année ${form.annee} et le type "${form.type}" existe déjà.`
    }

    return Object.keys(errors).length === 0
}

async function handleSubmit() {
    if (!validate()) return

    try {
        await updateBudget(route.params.id, form)
        alert('Budget modifié avec succès !')
        router.push('/budgets')
    } catch (e) {
        error.value = "Erreur lors de la modification du budget."
        console.error(e)
    }
}

onMounted(async () => {
    await loadBudget()
    await loadBudgets()
})
</script>

<style scoped src="@/assets/styles/Form.css"></style>

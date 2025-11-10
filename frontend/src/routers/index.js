import { createRouter, createWebHistory } from 'vue-router'
import HomeVue from '@/components/HomeVue.vue'


//Budget
import BudgetForm from '@/components/Budget-components/BudgetForm.vue'
import ModifierBudget from '@/components/Budget-components/ModifierBudget.vue'
import BudgetList from '@/components/Budget-components/BudgetList.vue'
import LigneBudgetForm from '@/components/Budget-components/LigneBudgetForm.vue'
import LigneBudgetList from '@/components/Budget-components/LigneBudgetList.vue'
import ModifierLigne from '@/components/Budget-components/ModifierLigne.vue'
// Prestataires
import Formulaire from '@/components/Prestataires-components/PrestataireForm.vue'
import Liste from '@/components/Prestataires-components/PrestataireList.vue'
import Modifier from '@/components/Prestataires-components/ModifierPrestataire.vue'

// RIBs
import RibList from '@/components/Rib-Components/RibList.vue'
import RibForm from '@/components/Rib-Components/RibForm.vue'
import ModifierRib from '@/components/Rib-Components/ModifierRib.vue'

// Ordonnancements
import OrdonnancementList from '@/components/Ordonnancement-components/OrdonnancementList.vue'
import OrdonnancementForm from '@/components/Ordonnancement-components/OrdonnancementForm.vue'
import ModifierOrdonnancement from '@/components/Ordonnancement-components/ModifierOrdonnancement.vue'
import OrdonnancementDetail from '@/components/Ordonnancement-components/OrdonnancementDetail.vue'

// Reglements
import ReglementList from '@/components/Reglement-components/ReglementList.vue'
import ReglementForm from '@/components/Reglement-components/ReglementForm.vue'
import ModifierReglement from '@/components/Reglement-components/ModifierReglement.vue'
import ReglementDetail from '@/components/Reglement-components/ReglementDetail.vue'

const routes = [
    { path: '/', name: 'HomeVue', component: HomeVue },
    { path: '/ajout-pres', name: 'Formulaire', component: Formulaire },
    { path: '/liste', name: 'Liste', component: Liste },
    { path: '/modifier/:id', name: 'Modifier', component: Modifier, props: true },

    // Routes pour RIBs
    { path: '/ribs', name: 'RibList', component: RibList },
    { path: '/ribs/add', name: 'RibAdd', component: RibForm },
    { path: '/rib/modifier/:id', name: 'ModifierRib', component: ModifierRib, props: true },

    { path: '/budgets', component: BudgetList },
    { path: '/ajouter-budget', component: BudgetForm },
    { path: '/modifier-budget/:id', name: 'ModifierBudget', component: ModifierBudget, props: true },
    { path: '/LigneBudgetaire/add', name: 'AjouterLigne', component: LigneBudgetForm, props: true },
    { path: '/LigneBudgetaire', name: 'Liste Ligne', component: LigneBudgetList, props: true },
    { path: '/ligne-budgetaire/modifier/:id', component: ModifierLigne, props: true },

    { path: '/ordonnancements', name: 'OrdonnancementList', component: OrdonnancementList },
    { path: '/ordonnancements/ajouter', name: 'AjouterOrdonnancement', component: OrdonnancementForm },
    { path: '/ordonnancements/:id/edit', name: 'ModifierOrdonnancement', component: ModifierOrdonnancement, props: true },
    { path: '/ordonnancements/:id', name: 'AfficherOrdonnancement', component: OrdonnancementDetail, props: true },

    { path: '/reglements', name: 'ReglementList', component: ReglementList },
    { path: '/reglements/ajouter', name: 'ReglementAdd', component: ReglementForm },
    { path: '/reglements/modifier/:id', name: 'ReglementEdit', component: ModifierReglement, props: true },
    { path: '/reglements/:id', name: 'ReglementDetail', component: ReglementDetail, props: true },



]




export default createRouter({
    history: createWebHistory(),
    routes,
})

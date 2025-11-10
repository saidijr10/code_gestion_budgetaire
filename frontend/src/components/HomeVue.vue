<template>
    <div class="home-container">
        <h1>Bienvenue sur l'application de Gestion de buget</h1>
        <p>Choisissez une action :</p>
        <ul class="nav-list">
            <li><router-link to="/liste">Gérer les Prestataires</router-link></li>
            <li><router-link to="/ribs">Gérer les RIBs</router-link></li>
            <li><router-link to="/budgets">Gérer les Budgets</router-link></li>
            <li><router-link to="/LigneBudgetaire">Lignes Budgetaires</router-link></li>
            <li><router-link to="/ordonnancements">Ordonnancements</router-link></li>
            <li><router-link to="/reglements">Règlements</router-link></li>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'HomeVue'
}
</script>


<style scoped>
.home-container {
    text-align: center;
    margin-top: 50px;
}
.nav-list {
    list-style: none;
    padding: 0;
    margin-top: 20px;
}
.nav-list li {
    margin: 10px 0;
}
.nav-list a {
    color: #2563eb;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.1rem;
}
.nav-list a:hover {
    text-decoration: underline;
}
</style>

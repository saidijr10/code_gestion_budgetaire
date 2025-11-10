const API_BUDGET = '/api/budgets/'

export async function getBudgets() {
    const res = await fetch(API_BUDGET)
    if (!res.ok) throw await res.json()
    return await res.json()
}

export async function createBudget(data) {
    const res = await fetch(API_BUDGET, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    if (!res.ok) throw await res.json()
    return await res.json()
}

export async function getBudgetById(id) {
    const res = await fetch(`${API_BUDGET}${id}/`)
    if (!res.ok) throw await res.json()
    return await res.json()
}

export async function updateBudget(id, data) {
    const res = await fetch(`${API_BUDGET}${id}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
    if (!res.ok) throw await res.json()
    return await res.json()
}

export async function deleteBudget(id) {
    const res = await fetch(`${API_BUDGET}${id}/`, {
        method: 'DELETE',
    })
    if (!res.ok) throw await res.json()
    return true
}

setTimeout(() => {

    const alerts = document.querySelectorAll(".toast")

    alerts.forEach(alert => {
        alert.style.display = "none"
    })

}, 4000)
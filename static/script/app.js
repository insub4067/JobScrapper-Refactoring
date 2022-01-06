table = document.getElementById('table')

if (table){
    jobs = table.getElementsByClassName('job')

    jobs = Array.from(jobs)

    jobs.forEach(job => {
        job.addEventListener("click", (event) => {
        url = event.target.parentNode.getAttribute("link"); 
        window.open(url)
    })
    });
};


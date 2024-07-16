
async function fetchData(event){

    try{
        const movie_id = event.target.getAttribute('data-movie_id');
        const response = await fetch(`[BASE URI GOES HERE]/ords/admin/mymovies/movie-single/${movie_id}`);
        console.log(response);
        if(!response.ok){
            throw new Error("Could not fetch resource");
        }
        const data = await response.json();
        const formatter = Intl.NumberFormat('en-US', {
            style:  'currency',
            currency: 'USD'
        });
        
        grossSales = formatter.format(Number(data.gross));

        document.querySelector(".modal-title").innerHTML = data.title;
        document.querySelector(".modal-body").innerHTML = 
       `<div class="container">
            <h6>Summary</h6>
            <div class="row">
                <p class="fw-light">${data.summary}</p>
            </div>
            <h6>Gross Sales</h6>
            <div class="row">
                <p class="fw-light">${grossSales}</p>
            </div>
        </div>`
    }
    catch(error){
        console.error(error);
        
    };
};

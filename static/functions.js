// The fetchData function can be found in the movieresults.html page. It is an "onclick" function. 
// And
async function fetchData(event){

    try{

        const movie_id = event.target.getAttribute('data-movie_id');
        // This looks for the data-movie_id attribute's value. 
        // It knows to look for the correct value, because it associates the 
        // "event" with whichever plus sign that was clicked. The plus sign is the 
        // "bi bi-plus" that you see in the code.

        const response = await fetch(`[ORDS URI for /movie_single/:id]${movie_id}`);

        // When you add your ORDS URI above, you'll need to remove the :id portion. 
        // You DO want to keep the ${movie_id} portion though. That will allow you 
        // to pass the movie_id as a route parameter to ORDS.

        console.log(response);
        if(!response.ok){
            throw new Error("Could not fetch resource");
        }
        const data = await response.json();

        // The below code formats the Gross Sales value so it appears a currency. 
        // It also makes the assumption that null is 0. Technically, they are not the same,
        // so you may want to pay attention to that, if you decide to extend this application.

        const formatter = Intl.NumberFormat('en-US', {
            style:  'currency',
            currency: 'USD'
        });
        
        grossSales = formatter.format(Number(data.gross));

        // The below line takes the json response, "const data = ...." and passes it back to the
        // movieresults.html page to display in the Modal's title field.
        document.querySelector(".modal-title").innerHTML = data.title;

        // Here you'll see more templating. These are Template Literals. They allow you to pass this html
        // and expressions - ${expression} - back to the html template. In this case, we are passing back
        // the Summary and Gross Sales information. See the notes.md page for a Template Literal reference.
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
